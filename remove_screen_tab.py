import os

import screen_tab_utils


def remove_emacs_desktop(session_info):
  if screen_tab_utils.emacs_desktop_saved(session_info):
    os.remove(screen_tab_utils.emacs_desktop_path(session_info))


def remove_current_session(screen_sessions, session_info):
  session_id = session_info['session_id']
  window = session_info['window']

  current_session = screen_sessions.setdefault(session_id, {})

  current_tab = current_session.get(window)

  keep_tab_intact = False
  if isinstance(current_tab, list):
    if len(current_tab) == 2 and current_tab[1] == 'SIGTERM':
      keep_tab_intact = True
      # The tab was not EXITed by a user, restore the correct path
      # for future use.
      current_session[window] = current_tab[0]
    else:
      raise ValueError('Only valid list ends in SIGTERM.')
  elif isinstance(current_tab, basestring):
    current_session.pop(window)
  elif current_tab is not None:
    raise TypeError('Unexpected value for current tab.')

  if not current_session:
    screen_sessions.pop(session_id)

  return keep_tab_intact


def main():
  session_info = screen_tab_utils.get_session_info()
  if session_info is None:
    return

  screen_sessions = screen_tab_utils.load_sessions()
  keep_tab_intact = remove_current_session(screen_sessions, session_info)
  screen_tab_utils.write_sessions(screen_sessions)
  if not keep_tab_intact:
    remove_emacs_desktop(session_info)


if __name__ == '__main__':
  main()
