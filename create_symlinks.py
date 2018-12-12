"""Create symlinks to all configuration files.

This assumes a posix system.
"""

import os


DOTFILES_DIR = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
SYMLINKS = (
    ("bash_colors", ".bash_colors"),
    ("bash_completion.d", ".bash_completion.d"),
    ("bash_profile", ".bash_profile"),
    ("profile", ".profile"),
    ("bashrc", ".bashrc"),
    ("emacs.d", ".emacs.d"),
    ("git-completion.bash", ".git-completion.bash"),
    ("gitconfig", ".gitconfig"),
    ("screenrc", ".screenrc"),
    ("ssh_config", os.path.join(".ssh", "config")),
    ("Xmodmap", ".Xmodmap"),
    # Optional, but will fail to link if doesn't exist).
    ("local_profile_extensions", ".local_profile_extensions"),
    # http://unix.stackexchange.com/q/1677
    ("xsessionrc", ".xsessionrc"),
)
LINE = "-" * 70


def add_symlinks():
    print("Adding symlinks:")
    print(LINE)

    links_added = False
    for source, symbolic_location in SYMLINKS:
        src = os.path.join(DOTFILES_DIR, source)
        dst = os.path.join(HOME, symbolic_location)
        if os.path.islink(dst):
            real_path = os.path.realpath(dst)
            if real_path != src:
                msg = "Real path for link: %r\nwas %r\nsupposed to be %r." % (
                    dst,
                    real_path,
                    src,
                )
                raise ValueError(msg)
        else:
            msg = "Linking %r\nas %r." % (src, dst)
            print(msg)
            os.symlink(src, dst)
            links_added = True

    if not links_added:
        print("No links needed to be added.")


if __name__ == "__main__":
    add_symlinks()
