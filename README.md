Danny Hermes `dotfiles`
=======================

## Prerequisites

In order to do this you'll need `git` installed. It should come by default
on macOS and Linux. If not, get a new version of your OS.

## Symlinks

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

## GNU Screen

In order to track open GNU Screen windows, the `dotfiles/screen_sessions.json`
file is used. Populate it with the "initial" content

```json
{"SENTINEL": null}
```

## System Paths / Defaults

There are some paths on the system that define default behavior.

- On Ubuntu, `/etc/ssh/sshd_config` [can be modified][2] to force `ssh`
  login to **only** accept a public key. In particular, the line
  `PasswordAuthentication no` should be added (or a variant of it should
  be uncommented). After modifying this, run `restart ssh` or just reboot.
- On macOS, `/private/etc/ssh/sshd_config` [can be modified][8] to force `ssh`
  login to **only** accept a public key. In particular, the line
  `PasswordAuthentication no` should be added (or a variant of it should
  be uncommented). Also `ChallengeResponseAuthentication no` should be set.
  "If you are using a stock install (i.e., you didn't build/install it yourself
  from source), launchd should take care of picking up the new config without
  having to restart the daemon."

## Optional

- Often the default version of `emacs` on macOS is too old, so it may be
  worth trying to update
- Install VS Code (`code`)
- On macOS, install [Homebrew][3]
- It's not uncommon for me to install the [Google Cloud SDK][1].
- On macOS, it's always important to start by running
  `xcode-select --install` to make sure Developer Tools are installed
- For working with `node`, install [`nvm`][4]
- For working with `python`, install [`pyenv`][5]
- For working with `go`, install [`goenv`][6]
- For working with `ruby`, install [`rbenv`][7]
- I occasionally like to use LaTeX for typesetting, so sometimes will
  install it on a new machine. I will also sometimes install `pdftk`.

[1]: https://cloud.google.com/sdk/install
[2]: https://www.linux.org/threads/how-to-force-ssh-login-via-public-key-authentication.8726/
[3]: https://brew.sh
[4]: https://github.com/creationix/nvm
[5]: https://github.com/pyenv/pyenv
[6]: https://github.com/syndbg/goenv
[7]: https://github.com/rbenv/rbenv
[8]: http://serverfault.com/a/86007
