import screen_tab_utils


def main():
    session_info = screen_tab_utils.get_session_info()
    if session_info is None:
        return

    session_id = session_info['session_id']
    window = session_info['window']

    screen_sessions = screen_tab_utils.load_sessions()
    current_session = screen_sessions.setdefault(session_id, {})
    current_tab = current_session.get(window)

    if isinstance(current_tab, basestring):
        current_session[window] = [current_tab, 'SIGTERM']
        screen_tab_utils.write_sessions(screen_sessions)
    elif current_tab is not None:
        raise TypeError('Tab value not expected to differ from non-existent or'
                        'a string.')


if __name__ == '__main__':
    # See http://stackoverflow.com/a/9256709/1068170
    # for details on determining which signals are being caught.
    main()
