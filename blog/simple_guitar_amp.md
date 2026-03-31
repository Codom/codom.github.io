<!-- date: 2026-01-15 -->
# SimpleGuitarAmp

[Source Code](https://github.com/Codom/SimpleGuitarAmp)

## 1. Architecture & Entry Point
The plugin is built using the CLAP (Clever Audio Plugin) standard and written in Zig.

**Entry Point:** The plugin exposes the `clap_entry` symbol in `src/main.zig`, which provides the host with a factory to create the plugin instance.

**Descriptor:** It defines itself as a "HelloCLAP" plugin with features including audio-effect, distortion, and stereo.

**State Management:** The core logic resides in `src/plugin.zig`. It uses a `Plugin` struct to hold the CLAP host pointer, current sample rate, filter states, and parameter values.

## 2. Signal Processing Pipeline
The audio processing logic is contained within the `render_audio` function in `src/plugin.zig`. The signal chain processes stereo audio in the following order:

**Input Acquisition:** It reads the left and right input samples.

**Tone Stack (EQ):** The signal passes through a series of filters defined in filters.

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
