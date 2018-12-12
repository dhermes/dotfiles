Danny Hermes `dotfiles`
=======================

## Getting Started

After cloning this, create symlinks to all configuration files:

```
$ python create_symlinks.py
Adding symlinks:
----------------------------------------------------------------------
...
```

You may need to create `~/.ssh` as well. You may also want to enable
`git is-child` via:

```
ln -s is-git-child.sh /usr/local/bin/is-git-child
```

(or some directory on your `${PATH}` other than `/usr/local/bin`).

## Pre-requisites

In order to do this you'll need `git` installed. It should come by default
on macOS and Linux. If not, get a new version of your OS.
