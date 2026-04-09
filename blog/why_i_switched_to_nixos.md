<!-- date: 2026-04-09-->

# Introduction

For a while, I've been extremely annoyed at how I've
been managing my dotfiles. The main point of contention
that I've had is the divergence in the desired features
on my laptop versus my desktop.

The way I did this was by using git and syncing off of
a remote repo, which was self-hosted on my old laptop
because these configs contained things like private keys
and whatnot that I don't want the internet knowing about.

Moreover, because it was a git repo, I had these diverging
configs in different branches and had to constantly rebase
the diffs on top of a main trunk branch. And since I rarely
edit my dotfiles, I always ran into a weird caveats that forced
me to merge changes from my desktop branch onto my laptop
in a way that wasn't clean, introduced errors, and
was just plain annoying to deal with.

So when I first heard about nixos's home manager, I was
immediately intrigued. However, to use home manager,
I would have to go through the painful process of porting all
my configs over to nix. Moreover, NixOS by it's very nature
is a very *strange* distribution, so I held off an actually
switching over until I had a good excuse to do so.

And then, one day, for no reason at all, my Arch install broke.

*classic*

Well... now I have a good excuse.

# First impressions

So far, I feel like a noob all over again. About ten years
of intuition built up from duct taping my arch linux config
together had to be relearned from the ground up. But I can
see now how this is actually worth it in the end.

For one, NixOS keeps everything in the nix-store by default.
This means that an upgrade doesn't clobber any directory,
no matter if it's just a config update or a full-on system
upgrade. This has an immediately noticeable benefit, because
the entire reason I switched over was because an arch update
completely ruined my day. With Nix, I just do a rollback and
continue on with my life.

However, I didn't really appreciate the next benefit until I
started getting knee-deep in the Nix Flake ecosystem and started
to drop flakes in every file directory, even flake-ifying my
entire system configuration.
Because now, instead of having a loose collection of dotfiles
that I have to meticulously manage, I have a centralized repo
of nix configurations that are used to derive my final system
config. Even better, I can have device-specific configurations
separated out into their own module, and I specify which config
I want based off a simple switch:

```sh
# For my desktop
sudo nixos-rebuild switch --flake #sol

# For my laptop
sudo nixos-rebuild switch --flake #alphacen
```

## This feels familiar...

Funnily enough, this paradigm isn't new to me. I have some
experience with the Yocto Project. And sure, the Yocto project
has a very different goal in mind with how it's structured, both
projects end up solving the exact same problem.

With Yocto, there's a need to define the configuration for
an embedded linux system in a centralized manner. The solution?
Bitbake.

Now bitbake is a bit of a bloated mess. I've never been the
biggest fan of it. But fundamentally, it solves this problem
in a robust fashion, which is great because nobody wants to
write the same script that packages a root filesystem in the
exact format needed to boot on some custom mcu board.

However, with Nix it's a bit different. Nix is a bit more
general-purpose in it's goals. Unlike Yocto, NixOs comes default
configured to use a build-cache. This means the experience of
deriving a final Linux configuration is less painful, though
also less configurable.

*That being said, I assume that not using the build-cache allows
for some more yocto-like functionality, I just haven't
investigated it yet*

Instead I see it as a more useful terraform. My systems now have
a central definition, with the only useful differences being
paramterized and controlled with a simple cli flag when I
run a rebuild.

# Some pain points

That isn't to say it's a totally seamless process. Whenever
I find myself needing build tools, especially build tools
that want to use their own package managers (Python, Node, etc)
I find myself a bit confused about whether to define these deps
in the flake or in the node-modules/requirements.txt/etc.

So far I've found a healthy balance of just defining it
everywhere... maybe this isn't a healthy balance, but it's the
only way I got my website to build without completely overhauling
the github workflow. I'll probably have to add that to my
todo list...

# Final thoughts

I haven't put nixos on my laptop yet, as I'm still hammering down
every last config I'm missing. But I hope that when I do deploy
it, it's as simple as running the following command:

```
sudo nixos-rebuild switch --flake #alphacen
```

No merge conflicts. No issues. Just a pure derivation based
on a config that I already tested on my other machine.

And that is fundamentally why I decided to switch to Nix.
