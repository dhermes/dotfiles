# pylint: disable=missing-docstring

import subprocess
import sys

import screen_tab_utils


EMACS_DESKTOP_ALERT = """\
Yo dawg

One last thing


You have an emacs desktop saved for this tab.
You should launch emacs and restore that shizz.
"""
TAB_MISSING_TEMPLATE = """\
Yo dawg


Tab %s is not stored for session %r.

"""


def obey_symlink_pwd():
    """A version of pwd which does not follow symlinks.

  This is because os.getcwd() follows symlinks.
  """
    proc = subprocess.Popen(['pwd'], stdout=subprocess.PIPE)
    proc.wait()
    return proc.stdout.read().strip()


def print_emacs_stuff(session_info):
    if screen_tab_utils.emacs_desktop_saved(session_info):
        print >> sys.stderr, EMACS_DESKTOP_ALERT


def change_directory(screen_sessions, session_info,
                     called_from_bashrc=False):
    session_id = session_info['session_id']
    window = session_info['window']

    current_session = screen_sessions.setdefault(session_id, {})

    if not called_from_bashrc:
        # We only need to overwrite the current_session[window] value
        # if not being called from bashrc.
        current_session[window] = obey_symlink_pwd()
        return

    previous_path = current_session.get(window)
    if previous_path is not None:
        # NOTE: The printed value will be sourced.
        print previous_path
        # NOTE: `print_emacs_stuff()` puts information in stderr so the user
        #       can learn about the environment they are re-launching.
        print_emacs_stuff(session_info)
        # After we print the path, the ~/.bashrc file will cd into it to
        # re-initialize a stored environment.
        sys.exit(0)
    else:
        print >> sys.stderr, TAB_MISSING_TEMPLATE % (window, session_id)
        # pylint: disable=bad-builtin
        windows_as_ints = map(int, current_session.keys())
        # pylint: enable=bad-builtin
        max_window = 0
        if windows_as_ints:
            max_window = max(windows_as_ints)
        print >> sys.stderr, 'Your max is', max_window
        # Since `previous_path` is None, add the
        # new path (nothing to overwrite).
        current_session[window] = obey_symlink_pwd()
        # Return the path since it will be printed within the sourced bashrc.
        return current_session[window]


def main(argv):
    if len(argv) > 2:
        raise ValueError('Using this method wrong.')

    session_info = screen_tab_utils.get_session_info()
    if session_info is None:
        return

    screen_sessions = screen_tab_utils.load_sessions()

    called_from_bashrc = len(argv) == 2 and argv[1] == '--new'
    path_to_print = change_directory(screen_sessions, session_info,
                                     called_from_bashrc=called_from_bashrc)

    screen_tab_utils.write_sessions(screen_sessions)

    if called_from_bashrc:
        print path_to_print
        print_emacs_stuff(session_info)


if __name__ == '__main__':
    main(sys.argv)
