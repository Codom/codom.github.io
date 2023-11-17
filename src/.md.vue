<template><h1>Vue port</h1>
<p>I have spent the past few days porting my website into vue. I've done this
to try and understand a modern web development framework instead of some system
I've duct-taped and zip-tied together in Python.</p>
<p>At the moment, the site doesn't differ much from the default scaffold that vue
provides. This is because I'm not a designer, and don't pretend to be. However, 
I do think some things can be done in order to shape this site to more closely
match the style I had previously.</p>
<h2>Porting three.js</h2>
<p>My old website had a Mandelbrot zoom shader running in the background. I put 
some effort into making sure that this shader doesn't use too much GPU, but since
it runs without any sort of routing framework, every page navigation resets
this animation.</p>
<p>With Vue, I want to make use of the router to prevent this from happening
while navigating the site. Once this <em>is</em> implemented, I can potentially
integrate the shader bindings into the page and have better animation
capabilities.</p>
<p>To get started, I simply imported animation.js and copied over the shaders.
I initially put these into the <code>assets/</code>directory. I didn't realize
that this directory is only used for Webpack purposes and isn't exposed
on the network. I learned that these sorts of assets should be in the <code>public</code>
directory instead.</p>
<p>The next step was to provide the <code>animConatiner</code> div that this
script uses as a render target into the dom. To do this, I just added this div
to the <code>App.vue</code> Component, and manually edited the CSS to have it placed
as a background.</p>
<p>App.vue:</p>
<pre><code class="language-vue">&lt;script setup&gt;
// Other component imports here...
import * as anim from './assets/animations.js'
&lt;/script&gt;

&lt;template&gt;
    &lt;!-- Blah blah blah--&gt;
    &lt;!-- While we are here, let's setup the router-view --&gt;
    &lt;main&gt;
       &lt;router-view&gt;&lt;/router-view&gt;
    &lt;/main&gt;
    &lt;!-- My animation script needs this element in the dom to work --&gt;
    &lt;div id = &quot;animContainer&quot;&gt;&lt;/div&gt;
&lt;/template&gt;
</code></pre>
<p>assets/base.css</p>
<pre><code class="language-css">canvas {
    width: 100%;
    height: 100%;
    display: block;
    position: fixed;
    top: 0;
    left: 0;
    z-index: -9999;
    opacity: 0.3;
}
</code></pre>
<p>While editing this, I also setup the router-view ahead of time. More on that
below.</p>
<h2>Manually porting over pages</h2>
<p>If you're unfamiliar with my old website, I had these pages generated from
markdown files based on a Python script that manually styles the pages.</p>
<p>I will eventually port this system over, however, to turn this
default scaffold project into something I can call my own, I want to iterate
off of some manually imported pages first. To do this, I started copying
over the generated HTML pages as vue components wrapped in <code>&lt;template&gt;</code>
tags.</p>
<h2>Setting up the router</h2>
<p>When initializing the project, I didn't setup the Router. This was somewhat intentional
since I'm largely unfamiliar with modern web frameworks and want to learn rather
than scaffold. To set up this router,
I had to install the router package using npm and configure it using some javascript.</p>
<p>router.js</p>
<pre><code class="language-javascript">import { createRouter, createWebHistory } from 'vue-router';
import About from './components/TheWelcome.vue';
/* import blah blah blah ... */

const routes = [
    {
        path: '/',
        component: About,
    },
    /* ... */
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
</code></pre>
<p>I find this routing system pretty easy to use, however whenever I need
to add in pages I have to start editing the router. Also, since
I'm still a bit new to modern systems like this, I encountered an issue.
I'd like to organize the blog into a separate web directory, such as <code>/blog/static_website_blog</code>.
Unfortunately, this system breaks the mendelbrot zoom, since this changes the
pathing for the <code>fetch</code> functions that get them. I think there's an easy enough
fix, but I decided to just have blogs be on the website root since there are
not enough of them to cause namespace issues.</p>
<h2>Some issues</h2>
<p>For larger blog pages, the wide page view doesn't have the title
follow the screen as it scrolls. This isn't great since longer blogs
will. Additionally, the styling of code segments that come from the
generated html isn't styled in a way that looks nice. And finally,
the text isn't always super readable.</p>
<p><img alt="To see the header, I have to scroll" src="./title_not_centerred.png" /></p>
<p>The first thing I tackled was the code blocks. Using CSS, I simply added a subtle
white background with a low opacity.</p>
<p><img alt="" src="./looks_a_bit_better.png" /></p>
<p>Next, to center the header div, I just added the following CSS to the
component:</p>
<pre><code class="language-css"> .greetings {
    position: fixed;
    top: 50%;
    transform: translate(0, -50%);
  }
</code></pre>
<p>And then finally, making the text more readable just requires the Mandelbrot effect to have a lower opacity. The net result is the following:</p>
<p><img alt="" src="./final_blog_view.png" /></p>
<h1>Integrating the old website build</h1>
<p>So far, I like how this site looks. While there's still some work to do
on the style, I want to now try to port my old website's blog generator
into the system. There are a few things that I need to figure out to
effectively do this:</p>
<ol>
<li>Generate blog pages as Single File Components</li>
<li>Automatically hook detected blogs into the router</li>
<li>Place all images that might be linked into the public directory</li>
<li>Integrate this into npm for better builds</li>
</ol>
<h2>Generate blog pages as SFC's</h2>
<p>To start, let's look at what I had for the build script:</p>
<pre><code class="language-python">import markdown
import subprocess
import os

def main():
    process_markdown(&quot;blog&quot;)
    process_markdown(&quot;static_website&quot;)


def process_markdown(page: str):
    with open(f&quot;src/{page}.md&quot;, &quot;r&quot;, encoding=&quot;utf-8&quot;) as in_file:
        text = in_file.read()

    html = &quot;&quot;.join([
        markdown.markdown(text, extensions=['markdown.extensions.fenced_code'])
    ])

    print(f&quot;outputting to docs/{page}.html&quot;)
    with open(f&quot;docs/{page}.html&quot;, &quot;w&quot;, encoding=&quot;utf-8&quot;) as out_file:
        out_file.write(html)
</code></pre>
<p>I can easily render the html out to SFC's by simply wrapping the output
of process_markdown in <code>&lt;template&gt;</code> tags, </p>
<pre><code class="language-python">html = &quot;&quot;.join([
    &quot;&lt;template&gt;&quot;,
    markdown.markdown(text, extensions=['markdown.extensions.fenced_code'])
    &quot;&lt;/template&gt;&quot;,
])
</code></pre>
<p>With the markdown Python package, we can do much deeper component integration
than this by overriding the parsing tree emitter, however, for an MVP I think this will do.</p>
<p>We then take this and place the SFC's into the <code>src/blog</code> directory of the
project.</p>
<pre><code class="language-python">with open(f&quot;src/blog/{page}.vue&quot;, &quot;w&quot;, encoding=&quot;utf-8&quot;) as out_file:
    out_file.write(html)
</code></pre>
<p>Now we add another directory that contains the markdown source files for
the blog. Since <code>src/blog</code> contains autogenerated components, I will use
<code>/blog</code> instead.</p>
<pre><code>mkdir blog
</code></pre>
<p>After pointing the script to glob this directory for markdown files,
component generation is now <em>mostly</em> automated. However, these pages
are inaccessible by the single-page application.</p>
<h2>Integrating with the router</h2>
<p>The way to expose these autogenerated pages is to emit entries into
the BlogIndex component which itself references the router. This means
that we need to figure out a way to generate routes into the blog.</p>
<h2>Images</h2>
<h2>Integrating with npm</h2>
<p>For this, we simply install the <code>build.py</code> as a pre-script for both
dev and build.</p>
<pre><code class="language-json">  &quot;scripts&quot;: {
    &quot;predev&quot;:   &quot;./build.py&quot;,
    &quot;dev&quot;:      &quot;vite&quot;,
    &quot;prebuild&quot;: &quot;./build.py&quot;,
    &quot;build&quot;:    &quot;vite build&quot;,
    &quot;preview&quot;:  &quot;vite preview&quot;
  },
</code></pre>
<p>However, this approach does have a drawback; blog page generation is no longer
interactive. For now, this will work since markdown files can be interactively
written using modern text editors, but it <em>is</em> something I'd like to have in
the future.</p>
<h1>Deploying</h1>
<p>So far I simply deploy things on GithbPages. I've developed this
entire thing in a different directory from the current repo checkout,
but simply nuking the checkout and checking in the new files will
work fine. Nobody else uses it so there should be no complaints in
PRs  :^)</p>
<p>From there, I can update my github actions and simply push. Once done,
the whole project will be live in 5 minutes or less.</p></template>