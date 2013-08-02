import json
import os
import subprocess
import sys


SESSION_ID_KEY = 'STY'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREEN_SESSIONS_FILE = os.path.join(SCRIPT_DIR, 'screen_sessions.json')


def get_session_id():
  session_sty_value = os.getenv(SESSION_ID_KEY)
  if session_sty_value is None or '.' not in session_sty_value:
    return
  return session_sty_value.split('.', 1)[1]


def obey_symlink_pwd():
  proc = subprocess.Popen(['pwd'], stdout=subprocess.PIPE)
  proc.wait()
  return proc.stdout.read().strip()


def emacs_desktop_saved(session_id, window):
  """Checks if there is a saved desktop session for this tab.

  Caller makes sure session_id and window are not None.
  """
  session_name = 'emacs-desktop-%s-%s' % (session_id, window)
  session_path = os.path.join(SCRIPT_DIR, 'emacs.d', session_name)
  return os.path.isfile(session_path)


def print_emacs_stuff(session_id, window):
  if emacs_desktop_saved(session_id, window):
    print >>sys.stderr, 'Yo dawg'
    print >>sys.stderr, ''
    print >>sys.stderr, 'One last thing'
    print >>sys.stderr, ''
    print >>sys.stderr, ''
    print >>sys.stderr, 'You have an emacs desktop saved for this tab.'
    print >>sys.stderr, 'You should launch emacs and restore that shizz.'


def main(argv):
  if len(argv) > 2:
    print >>sys.stderr, 'Bad args',
    print >>sys.stderr, argv
    return

  session_id = get_session_id()
  window = os.getenv('WINDOW')
  try:
    # Don't actually use integer, since integer's can't be keys :(
    int(window)
  except (ValueError, TypeError):
    pass
  if session_id is None or window is None:
    return

  if os.path.isfile(SCREEN_SESSIONS_FILE):
    with open(SCREEN_SESSIONS_FILE, 'r') as fh:
      screen_sessions = json.load(fh)
  else:
    screen_sessions = {}

  current_session = screen_sessions.setdefault(session_id, {})
  called_from_bashrc = len(argv) == 2 and argv[1] == '--new'
  if called_from_bashrc:
    previous_path = current_session.get(window)
    if previous_path is not None:
      print previous_path
      print_emacs_stuff(session_id, window)
      return
    else:
      print >>sys.stderr, 'Yo dawg'
      print >>sys.stderr, ''
      print >>sys.stderr, ''
      print >>sys.stderr, 'Tab %s is not stored for session %r.' % (window,
                                                                    session_id)
      print >>sys.stderr, ''
      print >>sys.stderr, ''
      window_as_ints = map(int, current_session)
      max_window = max(window_as_ints) if window_as_ints else 0
      print >>sys.stderr, 'Your max is', max_window

  # If any of the conditions above fail
  current_session[window] = obey_symlink_pwd()

  with open(SCREEN_SESSIONS_FILE, 'w') as fh:
    json.dump(screen_sessions, fh, indent=2)

  if called_from_bashrc:
    print current_session[window]
    print_emacs_stuff(session_id, window)


if __name__ == '__main__':
  main(sys.argv)
