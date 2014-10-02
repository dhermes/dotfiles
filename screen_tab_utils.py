# pylint: disable=missing-docstring

try:
    import json
except ImportError:
    import simplejson as json
import os


SESSION_ID_KEY = 'STY'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREEN_SESSIONS_FILE = os.path.join(SCRIPT_DIR, 'screen_sessions.json')


def get_session_id():
    session_sty_value = os.getenv(SESSION_ID_KEY)
    if session_sty_value is None or '.' not in session_sty_value:
        return
    return session_sty_value.split('.', 1)[1]


def emacs_desktop_path(session_info):
    session_id = session_info['session_id']
    window = session_info['window']

    session_name = 'emacs-desktop-%s-%s' % (session_id, window)
    session_path = os.path.join(SCRIPT_DIR, 'emacs.d', session_name)
    return session_path


def get_session_info():
    session_id = get_session_id()
    window = os.getenv('WINDOW')
    try:
        # NOTE: Don't actually use integer, since integers can't be JSON keys.
        int(window)
    except (ValueError, TypeError):
        pass
    if session_id is None or window is None:
        return None

    return {
        'session_id': session_id,
        'window': window,
    }


def emacs_desktop_saved(session_info):
    """Checks if there is a saved desktop session for this tab.

  Caller makes sure session_id and window are not None.
  """
    return os.path.isfile(emacs_desktop_path(session_info))


def load_sessions():
    if os.path.isfile(SCREEN_SESSIONS_FILE):
        # NOTE: Not using `with` since may be using an old version of Python.
        file_obj = open(SCREEN_SESSIONS_FILE, 'r')
        screen_sessions = json.load(file_obj)
        file_obj.close()
    else:
        screen_sessions = {}

    return screen_sessions


def write_sessions(screen_sessions):
    # NOTE: Not using `with` since may be using an old version of Python.
    file_obj = open(SCREEN_SESSIONS_FILE, 'w')
    json.dump(screen_sessions, file_obj, indent=2)
    file_obj.close()
