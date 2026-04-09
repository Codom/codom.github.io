<!-- date: 2026-01-15 -->
# SimpleGuitarAmp

[Source Code](https://github.com/Codom/SimpleGuitarAmp)

## Introduction

I started this project out in reaction to this incredible video I found
on YouTube about three years ago.
[Tested: Where Does The Tone Come From In A Guitar Amplifier?](https://www.youtube.com/watch?v=wcBEOcPtlYk)

To give some background here, let me just say that music is an incredibly
important aspect of my life. I have a personal, and sentimental attachment
to the guitar largely due to how I was raised. And I remember growing up
and wanting to try out all sorts of expensive guitars hooked up to expensive
amplifiers.

I always thought that I could never quite sound like Van Halen without the
Peavy 5150, or Jimi Hendrix without a Marshall Super Lead. Instead, I had
to cope with my dingy little Fender Mustang which only ever emulated the
sounds of these incredibly famous amplifiers.

I remember reading on all sorts of forums, and hearing from music producer
interviews that there was something totally unique to the sound that these
amplifiers made. That without them, there was no possible way to truly capture
all of the subtle flaws that the vacuum tubes and analogue filters added into
the signal.

*All of that was completely wrong.*

In that tested video, Jim Lill creates the Tacklebox. It features:

 - No vacuum tubes
 - No rectifiers
 - No biases
 - Only EQ and Distortion guitar pedals

That's it. And it sounded *exactly* like all those classic amplifiers that
I as a kid always wanted but could never afford.

And this got me thinking... if he could do it with pedals, I could do it
with code.

## Getting things up and running

At the time, I was really into the Zig programming language. I still love
this language, and hope that it continues to see support going forward,
even in the age of llms. But the tricky thing about using Zig for this
sort of project is the fact that the most popular API for making audio
plugins is a bit of a pain in the butt if you're not using C++.

I want to take a moment and clarify that agentic programming really wasn't
a thing when I was initially writing this project. And sure, while I could
have tried to figure out the vst C api and created my own bindings in Zig, I
really wanted this project to just be a short week-long endeavor where I
could focus primarily on the DSP code rather than figuring out how to
translate the C++-focused documentation into C code, then Ziggifying the
whole thing.

So I used CLAP instead. CLAP isn't super well supported, but at least Bitwig
supports CLAP. Much more importantly, CLAP is a C API instead of C++,
and as such importing it into Zig and getting to work was much, *much* easier
than trying to figure out VST.

## The CLAP Tutorial

[Source Code](https://github.com/Codom/clap-tutorial)

To get things started, I followed
[Nakst's clap tutorial](https://nakst.gitlab.io/tutorial/clap-part-1.html).
It was fairly straightforward, and it taught me the basics of
defining the entrypoint for the plugin and using the API to communicate
to the host exactly what features would be needed by the plugin.

For this writeup, I won't focus too much on the API, and instead
focus on the DSP, but just to give you an idea of what this interop
looks like, have a look at how I instantiate the `c.clap_plugin_t`
for this tutorial.

```zig

// C api
pub const PluginClass = c.clap_plugin_t {
    .desc = &@import("root").PluginDescriptor,
    .plugin_data = null,

    .init = init_plugin,
    .destroy = destroy_plugin,
    .activate = activate_plugin,
    .deactivate = deactivate_plugin,
    .start_processing = start_processing,
    .stop_processing = stop_processing,
    .reset = reset,
    .process = process,
    .get_extension = get_extension,
    .on_main_thread = on_main_thread,
};
```

Again, having all of this be simple C makes this whole thing
a lot easier to use in Zig.

The tutorial plugin itself is quite simple, and is mostly contained
within the `process` callback.

```zig
fn process(_plugin: [*c]const c.clap_plugin_t, _process: [*c]const c.clap_process)
callconv(.c) c.clap_process_status {
    const plugin = get_plugin(_plugin);

    // I cut out a bunch of code getting frame_count, input_frame_count, event_i, etc.
    // just for brevity.

    var i: u32 = 0;
    while(i < frame_count) {
        while(event_i < input_event_count and next_event_frame == i) {
            const event = _process.*.in_events.*.get.?(_process.*.in_events, event_i);

            if(event.*.time != i) {
                next_event_frame = event.*.time;
                break;
            }

            plugin.process_event(event);
            event_i += 1;

            if(event_i == input_event_count) {
                next_event_frame = frame_count;
                break;
            }
        }

        plugin.render_audio(i, next_event_frame, _process.*.audio_outputs[0].data32[0], _process.*.audio_outputs[0].data32[1]);
        i = next_event_frame;
    }
```

The key observation to make here is that this is just an event loop.
We have to query the host for specific timing information regarding
the frame, but once we have that information, we can just call
`plugin.process_event(event)` for each event and then once
all events are accounted for, `plugin.render_audio`.

When in `process_event`, all we need to do is to keep track of the
what event came in, and if that event is a `CLAP_EVENT_NOTE_ON`
we append a voice to an internal ArrayList of voices corresponding
to the requested note. If we get `CLAP_EVENT_NOTE_CHOKE`, we remove
that voice from the ArrayList. This effectively gives us a complete
state of what our virtual keyboard should be, and from there it's
just a matter of generating tones based off of standard 12-tone
equal temperament equations. Here's what that tone-generation
algorithm looks like:

```zig
pub fn render_audio(plugin: *Plugin, start: u32, end: u32, outputL: [*c]f32, outputR: [*c]f32) void {
    var index: usize = start;
    while(index < end) : (index += 1) {
        var sum: f32 = 0.0;

        for(plugin.voices.items) |*voice| {
            if(!voice.held) continue;

            sum += std.math.sin(voice.phase * 2.0 * std.math.pi) * 0.2;
            voice.phase += @floatCast(440.0 * std.math.exp2((@as(f32, @floatFromInt(voice.key)) - 57.0) / 12.0) / plugin.sample_rate);
            voice.phase -= std.math.floor(voice.phase);
        }

        outputL[index] = sum;
        outputR[index] = sum;
    }
}
```

And voilà! A beautiful sounding sine wave generator in just a few hundred
lines of Zig!

## Understanding the filter equations

I had just followed in someone's footsteps, but now it was time to venture
out into uncharted (for me) waters. The tacklebox in that youtube video
only made use of eq and distortion pedals.

First, we'll tackle the eq.

The most important resource for this, by far was the
[EQ Cookbook](https://www.w3.org/TR/audio-eq-cookbook/). This cookbook outlines
the math behind what's known as the biquad transfer function.

I'm not going to sit here and pretend to understand everything about this function,
or DSP in general.
However, the key thing to understand about this function is that it is able
to adjust the gain of an audio sample based upon it's relation to a defined center
frequency, and it's able to do so by analyzing three total samples, and without
needing to convert anything to the frequency domain by using relatively slow
fourier transform functions. This is extremely important for real-time audio
plugins, as audio tends to have even stricter timing requirements than most video
games. I've actually experienced this in DAWs where my playing became awkward
and inaccurate with a measly 5ms frame time, which is about three times faster
than most video games.

*note:* I also took a peek at [CALF Audio's implementation](https://github.com/calf-studio-gear/calf/blob/master/src/calf/biquad.h)
to get a better understanding of how this function worked. Specifically, I
was confused at converting a human-understandable bandpass parameter to
the biquad parameters.

Once I got the biquad up and running, the only other thing I needed was distortion.
Luckily, this was a lot easier to understand and implement. I looked around
on the internet and found the [FAUST Library's](https://github.com/grame-cncm/faustlibraries/blob/master/misceffects.lib)
`cubicnl` implementation and ported it over to Zig.

Both of these implementations exist in the [effects.zig](https://github.com/Codom/SimpleGuitarAmp/blob/master/src/effects.zig)
module.

## Assembling the tone stack

Once I had these filters implemented, the final step was to assemble
the tone stack. In the original video, I saw that Jim made use of a tool
called the Tone Stack Calculator, of which a web version of can be found
[here](https://tonestack.yuriturov.com/).

I decided to replicate a pretty standard fender tone, as that was what
I'm most familiar with.

While I couldn't replicate the knob response directly, I got the filters
broadly where I observed them to be and implemented them with some biquads.

```zig
pub fn activate(plugin: *Plugin, sample_rate: f64, min_frames_count: u32, max_frames_count: u32) bool {
    _ = max_frames_count;
    _ = min_frames_count;
    plugin.sample_rate = sample_rate;
    plugin.filters = std.ArrayList(ef.biquad_d2){};

    plugin.filters.append(c_allocator, ef.biquad_d2.init_peak(20, 2.3, 0.25, plugin.sample_rate)) catch unreachable;
    plugin.filters.append(c_allocator, ef.biquad_d2.init_peak(520, 0.1, 1.00, plugin.sample_rate)) catch unreachable;
    plugin.filters.append(c_allocator, ef.biquad_d2.init_peak(6000, 2.3, 0.05, plugin.sample_rate)) catch unreachable;
    return true;
}

// ...

fn clap_process(_plugin: [*c]const c.clap_plugin_t, _process: [*c]const c.clap_process) callconv(.c) c.clap_process_status {
    const plugin = ptr_as(*Plugin, _plugin.*.plugin_data);

    plugin.sync_main_to_audio(_process.*.out_events);

    if (plugin.param_changed()) {
        const bass_v = plugin.params[@intFromEnum(P.Bass)];
        const mid_v = plugin.params[@intFromEnum(P.Mid)];
        const treb_v = plugin.params[@intFromEnum(P.Treble)];

        plugin.filters.items[0].set_peak(20, bass_v, 0.25, plugin.sample_rate);
        plugin.filters.items[1].set_peak(520, mid_v, 1.00, plugin.sample_rate);
        plugin.filters.items[2].set_peak(6000, treb_v, 0.05, plugin.sample_rate);
    }

// ...
}
```

With the frequency response dialed in, then it's just a matter
of setting the gain and then `render_audio`

```zig
pub fn render_audio(plugin: *Plugin, start: u32, end: u32, inputL: [*c]f32, inputR: [*c]f32, outputL: [*c]f32, outputR: [*c]f32) void {
    var index: usize = start;
    while (index < end) : (index += 1) {
        var inL: f32 = inputL[index];
        var inR: f32 = inputR[index];

        // params
        const gain = plugin.params[@intFromEnum(P.Gain)];
        const output_gain = plugin.params[@intFromEnum(P.OutputGain)];

        // Filters
        for (plugin.filters.items) |*filter| {
            inL = filter.process(inL);
            inR = filter.process(inR);
        }
        const eqL = inL;
        const eqR = inR;

        // Distortion
        const distortionL: f32 = ef.cub_nonl_distortion(eqL, gain, 0.0) * output_gain;
        const distortionR: f32 = ef.cub_nonl_distortion(eqR, gain, 0.0) * output_gain;

        const outL = distortionL;
        const outR = distortionR;

        outputL[index] = outL;
        outputR[index] = outR;
    }
}
```

The final plugin architecture ends up being fairly modular. Since the
biquad filters are in an ArrayList, it's fairly easy to just append
more filters to it in order to implement more tone stacks. Additionally,
one could create a `union` of different filter types and make use of
this ArrayList in order to chain arbitrary effects, though this would
likely not scale all that well.

The final sound was surprisingly good. It's likely not one hundred
percent faithful, but I'm extremely happy with the final result.

# Final plugin overview

## 1. Architecture & Entry Point
The plugin is built using the CLAP (Clever Audio Plugin) standard and written in Zig.

**Entry Point:** The plugin exposes the `clap_entry` symbol in `src/main.zig`, which provides the host with a factory to create the plugin instance.

**Descriptor:** It defines itself as a "HelloCLAP" plugin with features including audio-effect, distortion, and stereo.

**State Management:** The core logic resides in `src/plugin.zig`. It uses a `Plugin` struct to hold the CLAP host pointer, current sample rate, filter states, and parameter values.

## 2. Signal Processing Pipeline
The audio processing logic is contained within the `render_audio` function in `src/plugin.zig`. The signal chain processes stereo audio in the following order:

**Input Acquisition:** It reads the left and right input samples.

**Tone Stack (EQ):** The signal passes through a series of filters defined in `effects.zig`.

These are Biquad IIR filters (Direct Form 2 implementation) defined in `src/effects.zig`.

The plugin initializes three "peaking" filters to emulate a tone stack:

*   Bass: ~20 Hz
*   Mid: ~520 Hz
*   Treble: ~6000 Hz.

**Distortion:** The filtered signal is fed into a cubic nonlinear distortion algorithm (`cub_nonl_distortion`).

This algorithm approximates solid-state distortion using the equation `f(x) = x - x^3 / 3` (with clipping), ported from the FAUST standard library.

**Output Gain:** Finally, an output gain factor is applied before writing to the output buffer.

## 3. Parameter Handling & Thread Safety
The plugin manages 5 parameters: Gain, OutputGain, Bass, Mid, and Treble.

**Synchronization:** It employs a manual synchronization strategy between the main thread (UI/Host) and the audio thread.

*   `sync_main_to_audio` pushes parameter changes from the main thread to the audio processing loop.
*   `sync_audio_to_main` pushes changes back (e.g., from automation) to the main thread.

A mutex (`plugin.mut`) is used to protect shared state during these syncs.

**Extensions:** The plugin implements several CLAP extensions:

*   **Audio Ports:** Configures a single Stereo Input and Stereo Output.
*   **Params:** Exposes the parameters as automatable and modulatable.
*   **State:** Allows saving and loading the parameter state to a stream.

## 4. DSP Implementation Details
**Sanitization:** The biquad filters include a `bi_sanitize` function that checks for and cleans up denormal numbers (extremely small floating-point values) to prevent CPU performance degradation.

**Filter Updates:** When Bass, Mid, or Treble parameters change, the plugin recalculates the coefficients for the respective peak filters during the processing call.
