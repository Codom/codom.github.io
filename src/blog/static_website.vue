<template>
<h1>Easy way to make your own static website generator</h1>
<p>My personal website started out as a kind of joke. I learned how
to use gnu make in university as a minimal build system to compile
some notes I had into html. I showed this off to my roommate and then
he showed me how to actually host this stuff on github pages with
a custom domain. This make script comprised of patsubst macros that
automatically generated the rules based off of the md files in my src/
directory and fed them all into the <code>markdown</code> program.</p>
<pre><code class="language-make">PAGES := $(patsubst src/%.md,  docs/%.html, $(wildcard src/*.md))
MARKC := markdown
all: $(PAGES)

docs/%.html : src/%.md
    touch $@ &amp;&amp; $(MARKC) $&lt; &gt; $@ &amp;&amp; cat src/global &gt;&gt; $@
</code></pre>
<p>In addition to the above rule, I also threw in some rules to build my
resume and some wasm modules just for fun:</p>
<pre><code class="language-make">TEX   := $(patsubst src/%.tex, docs/%.pdf, $(wildcard src/*.tex))
TEXC  := pdflatex

CC      := emcc
CFLAGS  := -Wall -Isrc/wasm-canvas/include


docs/%.pdf : src/%.tex
    TEXINPUTS=&quot;.:./src:&quot; $(TEXC) $&lt;
    mv *.pdf docs/

docs/page.wasm : src/wasm_main.c
    $(CC) $(CFLAGS) --shell-file template.html src/wasm_main.c -o docs/wasm.html
</code></pre>
<p>As good as the make
system was, it wasn't particularly great when it comes to generating
a full navigable site with a standard global html elements. This <em>could</em> be
(and was) achieved using some file concatenation, but it ended up being
kind of a hack.</p>
<p>Now the static site generation is embedded in a python script that wraps
around the markdown module. Not only can I easily have all of the
html post-processing in one place, but the python-markdown module provides
an extension system in order to extend the syntax in useful ways. The best part?
It's so easy to get started. Below is all of the python needed to manually build
a couple of webpages in order to get started.</p>
<pre><code class="language-python">import markdown
header = &quot;&quot;&quot;
&lt;DOCTYPE html&gt;
&lt;-- etc --&gt;
&quot;&quot;&quot;
footer = &quot;&lt;-- etc --&gt;&quot;

def main():
    process_markdown(&quot;index&quot;)
    process_markdown(&quot;blog&quot;)
    # etc.

def process_markdown(page: str):
    with open(f&quot;src/{page}.md&quot;, &quot;r&quot;, encoding=&quot;utf-8&quot;) as in_file:
        text = in_file.read()

    html = &quot;&quot;.join([header, &quot;\n&quot;, markdown.markdown(text, extensions=['']), &quot;\n&quot;, footer])

    print(f&quot;outputting to docs/{page}.html&quot;)
    with open(f&quot;docs/{page}.html&quot;, &quot;w&quot;, encoding=&quot;utf-8&quot;) as out_file:
        out_file.write(html)

if __name__ == &quot;__main__&quot;:
    main()
</code></pre>
<p>Of particular note is the header and footer concatenation. This makes it possible
to embed a global header into all of your pages, but also to embed script tags
and stylesheet links. I use this in order to apply my stylesheet and to setup
some js to run a Mandelbrot zoom frag shader in the background of my pages.</p>
<pre><code class="language-python">header = &quot;&quot;&quot;
&lt;link rel=&quot;stylesheet&quot; type=&quot;text/css&quot; href=&quot;style.css&quot;&gt;
&quot;&quot;&quot;

footer = &quot;&quot;&quot;
&lt;script src=&quot;js/three.js&quot;&gt;&lt;/script&gt;
&lt;script src=&quot;animation.js&quot;&gt;&lt;/script&gt;
&quot;&quot;&quot;
</code></pre>
<p>And voila! Your very own static site generator.</p>
<p>However, that's not quite the extent of what can actually be done. This is
simply wrapping the output of the compiler. The python-markdown module provides
a way to extend the actual markdown syntax. I haven't explored what is possible
with that, but I do have some ideas for the future of this website, particularly
when it comes to more elegant page transitions by overriding how markdown <code>[]()</code> links
are handled. Perhaps more on that later :^)</p>
<p>I will likely port the rest of the makefile's functionality into the build.py script
for my personal website using some process spawning hacks since I'm not really using
the dependency graph features of make anyway. This will make the latex stuff a bit
more complicated, but it's worth it just to get rid of the make dependency. Other
than that, I am very happy with how this latest overhaul turned out.</p>

</template>
