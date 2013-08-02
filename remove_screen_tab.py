import json
import os
import subprocess


SESSION_ID_KEY = 'STY'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREEN_SESSIONS_FILE = os.path.join(SCRIPT_DIR, 'screen_sessions.json')


def get_session_id():
  session_sty_value = os.getenv(SESSION_ID_KEY)
  if session_sty_value is None or '.' not in session_sty_value:
    return
  return session_sty_value.split('.', 1)[1]


def emacs_desktop_saved(session_id, window):
  """Checks if there is a saved desktop session for this tab.

  Caller makes sure session_id and window are not None.
  """
  session_name = 'emacs-desktop-%s-%s' % (session_id, window)
  session_path = os.path.join(SCRIPT_DIR, 'emacs.d', session_name)
  return os.path.isfile(session_path)


def remove_emacs_desktop(session_id, window):
  session_name = 'emacs-desktop-%s-%s' % (session_id, window)
  session_path = os.path.join(SCRIPT_DIR, 'emacs.d', session_name)
  os.remove(session_path)


def main():
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
  current_session.pop(window, None)
  if not current_session:
    screen_sessions.pop(session_id)

  with open(SCREEN_SESSIONS_FILE, 'w') as fh:
    json.dump(screen_sessions, fh, indent=2)

  if emacs_desktop_saved(session_id, window):
    remove_emacs_desktop(session_id, window)


if __name__ == '__main__':
  main()
