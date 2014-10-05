#!/usr/bin/env python

# pylint: disable=missing-docstring

import __builtin__
import collections
import getpass
import os
import platform
import shutil
import string
import subprocess
import sys


PLATFORM = None
LINUX_PLATFORM = 'Linux'
OS_X_PLATFORM = 'Darwin'
SYMLINKS = {
    '$HOME/dotfiles/bash_colors': '$HOME/.bash_colors',
    '$HOME/dotfiles/bash_completion.d': '$HOME/.bash_completion.d',
    '$HOME/dotfiles/bash_profile': '$HOME/.bash_profile',
    '$HOME/dotfiles/profile': '$HOME/.profile',
    '$HOME/dotfiles/bashrc': '$HOME/.bashrc',
    '$HOME/dotfiles/emacs.d': '$HOME/.emacs.d',
    '$HOME/dotfiles/git-completion.bash': '$HOME/.git-completion.bash',
    '$HOME/dotfiles/gitconfig': '$HOME/.gitconfig',
    '$HOME/dotfiles/hgrc': '$HOME/.hgrc',
    '$HOME/dotfiles/netrc': '$HOME/.netrc',
    '$HOME/dotfiles/screenrc': '$HOME/.screenrc',
    '$HOME/dotfiles/ssh_config': '$HOME/.ssh/config',
    '$HOME/dotfiles/Xmodmap': '$HOME/.Xmodmap',
    # http://unix.stackexchange.com/q/1677
    '$HOME/dotfiles/xsessionrc': '$HOME/.xsessionrc',
    # Hand-rolled scripts.
    '$HOME/dotfiles/wipe_pyc_recursive.py':
        '/usr/local/bin/wipe-pyc-recursive',
}
APTITUDE_INSTALL = [
    'xclip',
    'xsel',
    # http://stackoverflow.com/questions/1911713
    'texlive-latex-base',
    'texlive-latex-extra',
    'texlive-full',
    'python-scitools',
    'okular',
    # http://stackoverflow.com/a/9843560/1068170
    'libpng-dev',
    'libfreetype6-dev',
    'python-pyside',  # Backend for matplotlib>=1.4.0.
    'openssh-server',
    'espeak',
    'libevent-dev',  # Requirement for python readline.
    'libncurses5-dev',  # Requirement for python readline.
    'nodejs',
    'npm',
    'tk-dev',
    'python-gtk2',
    'python-gtk2-dev',
    'emacs24',
    'screen',
    'libgnome2-bin',
    'python-wxgtk2.8',
    'python-wxtools',
    'wx2.8-i18n',
    'libwxgtk2.8-dev',
    'libgtk2.0-dev',
    'autojump',
    'nautilus-dropbox',
    # http://askubuntu.com/a/350799
    'shutter',  # To replace gnome-screenshot.
]
PIP_INSTALL = [
    'matplotlib',
    'numpy',
    'scipy',
    'sympy',
    'pillow',
    'mercurial',
    'readline',  # HAS ISSUES, MIGHT NEED TO TARGET A VERSIOn
    'ipython',
    'virtualenv',
    'tox',
    'unittest2',
    'nose',
]
# NOTE: This will be populated with (web_page, install_method) pairs.
#       Since we need to define the `install_method`, this happens as
#       the methods are created below. As some may rely on previous
#       installs, we use an `OrderedDict`.
MAC_PACKAGES = collections.OrderedDict()
LINE = '-' * 70
SECTION_SEP = ('=' * 70) + ('\n' * 4) + ('=' * 70)


def check_python_version():
    # First check the current running version.
    major, minor, _, _, _ = sys.version_info
    if (major, minor) != (2, 7):
        raise ValueError('Expected Python 2.7 to be version running.')

    # Then check system `python`.

    # http://stackoverflow.com/a/2502883/1068170
    proc = subprocess.Popen(
        ['python', '-V'],
        stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    # NOTE: `communicate` waits for process to terminate.
    stdout, stderr = proc.communicate()
    if stdout != '':
        raise ValueError('Unexpected stdout from `python -V`.')
    if stderr[:11] != 'Python 2.7.':
        raise ValueError('Unexpected system Python: %r.' % stderr)


def add_rc_files():
    print 'Adding rc files which require passwords (and can\'t be checked in):'
    print LINE
    # NOTE: This must run before `add_symlinks`.
    hgrc_fi = os.path.expandvars('$HOME/dotfiles/hgrc')
    hgrc_template_fi = hgrc_fi + '.pytemplate'

    netrc_fi = os.path.expandvars('$HOME/dotfiles/netrc')
    netrc_template_fi = netrc_fi + '.pytemplate'

    if os.path.exists(hgrc_fi) and os.path.exists(netrc_fi):
        print 'Both rc files already exist.'
        do_replace = raw_input('Would you like to overwrite them? [y/N] ')
        if do_replace.lower() != 'y':
            return

    with open(hgrc_template_fi, 'r') as file_obj:
        hgrc_template = string.Template(file_obj.read())

    with open(netrc_template_fi, 'r') as file_obj:
        netrc_template = string.Template(file_obj.read())

    # Get the template values to be placed into rc files.
    codehosting_email = raw_input('Email for Google Code Hosting: ')
    print 'NOTE: Google Code Hosting password can be found at'
    print '      https://code.google.com/hosting/settings'
    codehosting_password = getpass.getpass(
        'Password for Google Code Hosting: ')
    substitution_dict = {
        'codehosting_email': codehosting_email,
        'codehosting_password': codehosting_password,
    }

    # Make substitutions and write to files.
    with open(hgrc_fi, 'w') as file_obj:
        file_obj.write(hgrc_template.substitute(substitution_dict))
        print 'Wrote:', hgrc_fi

    with open(netrc_fi, 'w') as file_obj:
        file_obj.write(netrc_template.substitute(substitution_dict))
        print 'Wrote:', netrc_fi


def add_session_file():
    # Add SENTINEL to screen sessions file so that it is never an empty
    # {}. This is because json.dump({}, file_obj) will store an empty string.
    import screen_tab_utils
    screen_sessions = screen_tab_utils.load_sessions()
    screen_sessions['SENTINEL'] = None
    screen_tab_utils.write_sessions(screen_sessions)


def add_symlinks():
    # NOTE: This must run after `add_rc_files`.
    print 'Adding symlinks:'
    print LINE

    links_added = False
    for source, symbolic_location in SYMLINKS.iteritems():
        src = os.path.expandvars(source)
        dst = os.path.expandvars(symbolic_location)
        if os.path.islink(dst):
            real_path = os.path.realpath(dst)
            if real_path != src:
                msg = '\n'.join(['Real path for link: %r' % dst,
                                 'was %r' % real_path,
                                 'supposed to be %r.' % src])
                raise ValueError(msg)
        else:
            msg = '\n'.join(['Linking %r' % src,
                             'as %r.' % dst])
            print msg
            os.symlink(src, dst)
            links_added = True

    if not links_added:
        print 'No links needed to be added.'


def install_google_cloud_sdk():
    gcloud_sdk = os.path.expandvars('$HOME/google-cloud-sdk')
    if os.path.isdir(gcloud_sdk):
        print 'Directory %r already exists.' % (gcloud_sdk, )
        valid_install = raw_input(
            'Is google-cloud-sdk already installed? [y/N] ')
        if valid_install.lower() == 'y':
            return

    cmd = 'curl https://sdk.cloud.google.com | bash'
    print 'The install command is:'
    print '    $ %s' % cmd
    print 'Check this is still valid at https://cloud.google.com/sdk/.'
    still_valid = raw_input('Is this install command still valid? [y/N] ')
    if still_valid.lower() != 'y':
        msg = ('Please change install_google_cloud_sdk() to reflect the\n'
               'current recommended way to install.')
        raise ValueError(msg)

    os.system(cmd)


def _linux_add_packages():
    # NOTE: This is Linux only. (Really even more specific than Linux.)
    print 'Adding Linux packages:'
    print LINE

    apt_cmd = ['apt-get', 'install', '-y'] + APTITUDE_INSTALL
    subprocess.check_call(apt_cmd)

    install_google_cloud_sdk()


def mac_cli_tools_install():
    try:
        subprocess.check_output(
            ['pkgutil', '--pkg-info=com.apple.pkg.CLTools_Executables'])
        print 'Confirmed Mac OS X command line tools are installed.'
    except subprocess.CalledProcessError:
        print 'To install OS X command line tools, please run'
        print '    xcode-select --install'
        print 'before invoking this script again.'
        sys.exit(1)


MAC_PACKAGES['http://stackoverflow.com/a/19899984/'] = mac_cli_tools_install


def change_system_paths():
    system_path_file = '/etc/paths'
    custom_path_file = os.path.expandvars('$HOME/dotfiles/mac_etc_paths')

    with open(system_path_file, 'r') as file_obj:
        system_path_contents = file_obj.read()

    with open(custom_path_file, 'r') as file_obj:
        custom_path_contents = file_obj.read()

    if system_path_contents == custom_path_contents:
        # If the real path matches the desired file, we are done.
        print '%r->%r mapping already exists.' % (system_path_file,
                                                  custom_path_file)
        return

    print 'We want to replace the contents of %r:' % (system_path_file, )
    print system_path_contents

    print LINE

    print 'The intended replacement is:'
    print custom_path_contents

    proceed = raw_input('Is this file OK to replace? [y/N] ')
    if proceed.lower() != 'y':
        raise ValueError('Can\'t proceed, rejected by user.')

    # Move the existing file to backup.
    system_path_file_backup = system_path_file + '.factory-defaults'
    shutil.move(system_path_file, system_path_file_backup)
    # Copy the contents.
    shutil.copyfile(custom_path_file, system_path_file)


MAC_PACKAGES['http://unix.stackexchange.com/q/75748'] = change_system_paths


def homebrew_install():
    proc = subprocess.Popen(
        ['which', 'brew'],
        stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    if stdout != '':
        print 'Brew found on system at: %r' % (stdout.strip())
        brew_correct = raw_input('Is this the correct install? [y/N] ')
        if brew_correct.lower() == 'y':
            return

    # If we've reached this part of the code, we need to install brew.
    cmd = (
        'ruby -e "$(curl -fsSL '
        'https://raw.githubusercontent.com/Homebrew/install/master/install)"')
    print 'The suggested way to install Homebrew is:'
    print '    $ %s' % cmd
    print 'NOTE: This assumes OS X has ruby installed.'
    proceed = raw_input('Is this still the correct way? [y/N] ')
    if proceed.lower() != 'y':
        msg = ('Please change homebrew_install() to reflect the current\n'
               'recommended way to install.')
        raise ValueError(msg)

    ruby_install_script = subprocess.check_output(
        ['curl', '-fsSL',
         'https://raw.githubusercontent.com/Homebrew/install/master/install'])
    subprocess.check_call(['ruby', '-e', repr(ruby_install_script)])


MAC_PACKAGES['http://brew.sh/'] = homebrew_install


def install_from_pkg_link(link):
    # If we've reached this part of the code, we need to install node.
    local_path = os.path.join(os.getcwd(), 'tmp.pkg')
    if os.path.exists(local_path):
        raise OSError('Download path exists: %r' % (local_path, ))
    cmd1 = ['curl', link, '-o', local_path]
    cmd2 = ['installer', '-pkg', local_path, '-target', '/']
    cmd3 = ['rm', '-f', local_path]

    print 'The suggested way to install is:'
    print '    $ %s' % ' '.join(cmd1)
    print '    $ %s' % ' '.join(cmd2)
    print 'NOTE: For command-line pkg installation see:'
    print '      http://hints.macworld.com/article.php?story=20030614230204397'

    proceed = raw_input('Is this still the correct way? [y/N] ')
    if proceed.lower() != 'y':
        msg = ('Please change the relevant method to reflect the current\n'
               'recommended way to install.')
        raise ValueError(msg)

    subprocess.check_call(cmd1)
    subprocess.check_call(cmd2)
    subprocess.check_call(cmd3)


def nodejs_install():
    proc = subprocess.Popen(
        ['which', 'node'],
        stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    if stdout != '':
        print 'node.js found on system at: %r' % (stdout.strip())
        node_correct = raw_input('Is this the correct install? [y/N] ')
        if node_correct.lower() == 'y':
            return

    # If we've reached this part of the code, we need to install node.
    install_from_pkg_link('http://nodejs.org/dist/v0.10.32/node-v0.10.32.pkg')


MAC_PACKAGES['http://nodejs.org/download/'] = nodejs_install
MAC_PACKAGES['https://cloud.google.com/sdk/'] = install_google_cloud_sdk


def install_tex_on_mac():
    proc = subprocess.Popen(
        ['which', 'pdflatex'],
        stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    if stdout != '':
        print 'pdflatex found on system at: %r' % (stdout.strip())
        tex_correct = raw_input('Is this the correct install? [y/N] ')
        if tex_correct.lower() == 'y':
            return

    # If we've reached this part of the code, we need to install MacTex.
    install_from_pkg_link(
        'http://mirror.ctan.org/systems/mac/mactex/MacTeX.pkg')


MAC_PACKAGES['http://www.tug.org/mactex/'] = install_tex_on_mac


def _os_x_add_packages():
    for web_page, install_method in MAC_PACKAGES.iteritems():
        print LINE
        print 'Trying to install Mac OS X dependency:'
        print '    %s' % (web_page, )
        install_method()


def add_packages():
    print 'Adding platform specific packages:'
    if PLATFORM == LINUX_PLATFORM:
        _linux_add_packages()
    elif PLATFORM == OS_X_PLATFORM:
        _os_x_add_packages()


def add_python_packages():
    # NOTE: This is OS agnostic.
    print 'Adding Python packages:'
    print LINE

    # First install `pip`.
    subprocess.check_call(['easy_install', '--upgrade', 'pip'])

    # Then use `pip` to install all desired packages.
    pip_cmd = ['pip', 'install', '--upgrade'] + PIP_INSTALL
    subprocess.check_call(pip_cmd)


def replace_line(lines, old_line, new_line):
    old_line_matches = [(i, line) for i, line in enumerate(lines)
                        if line == old_line]
    if len(old_line_matches) != 1:
        if lines.count(new_line) == 1:
            print 'The desired line: %r' % (new_line, )
            print '    is already contained in the file.'
            do_nothing = raw_input('Would you like to continue? [y/N] ')
            if do_nothing.lower() == 'y':
                return False
        raise ValueError('Non-unique match for PasswordAuthentication.')

    i, line = old_line_matches[0]
    do_replace = raw_input('Replace line: %r? [y/N] ' % line)
    if do_replace.strip().lower() != 'y':
        raise ValueError('Line rejected by user.')

    lines[i] = new_line
    return True


def _linux_make_ssh_public_key_only():
    # NOTE: This is Linux only.

    # See:
    # ('http://www.linux.org/threads/how-to-force-ssh-login-via-'
    #  'public-key-authentication.4253/')
    # ('https://www.digitalocean.com/community/tutorials/'
    #  'how-to-set-up-ssh-keys--2')
    ssh_config_fi = '/etc/ssh/sshd_config'

    with open(ssh_config_fi, 'r') as file_obj:
        original_contents = file_obj.read()

    lines = original_contents.split('\n')
    replaced_pw = replace_line(lines, '#PasswordAuthentication yes',
                               'PasswordAuthentication no')

    if not replaced_pw:
        print 'File unchanged, exiting make_ssh_public_key_only().'
        return

    # Create a backup before overwriting file.
    ssh_config_fi_backup = ssh_config_fi + '.factory-defaults'
    print 'Creating backup:', ssh_config_fi_backup
    shutil.copyfile(ssh_config_fi, ssh_config_fi_backup)

    # Write new lines to file.
    with open(ssh_config_fi, 'w') as file_obj:
        file_obj.write('\n'.join(lines))

    # Restart ssh server.
    subprocess.check_call(['restart', 'ssh'])


def _os_x_make_ssh_public_key_only():
    # NOTE: This is Mac OS X only.

    # See: http://serverfault.com/a/86007
    ssh_config_fi = '/private/etc/sshd_config'

    with open(ssh_config_fi, 'r') as file_obj:
        original_contents = file_obj.read()

    lines = original_contents.split('\n')

    # Turn PasswordAuthentication off.
    replaced_pw = replace_line(lines, '#PasswordAuthentication no',
                               'PasswordAuthentication no')

    # Turn ChallengeResponseAuthentication off.
    replaced_challenge = replace_line(
        lines, '#ChallengeResponseAuthentication yes',
        'ChallengeResponseAuthentication no')

    if not replaced_pw and not replaced_challenge:
        print 'File unchanged, exiting make_ssh_public_key_only().'
        return

    # Create a backup before overwriting file.
    ssh_config_fi_backup = ssh_config_fi + '.factory-defaults'
    print 'Creating backup:', ssh_config_fi_backup
    shutil.copyfile(ssh_config_fi, ssh_config_fi_backup)

    # Write new lines to file.
    with open(ssh_config_fi, 'w') as file_obj:
        file_obj.write('\n'.join(lines))

    # NOTE: (Quote from the server fault page)
    #       "If you are using a stock install (i.e., you didn't build/install
    #        it yourself from source), launchd should take care of picking up
    #        the new config without having to restart the daemon."


def make_ssh_public_key_only():
    print 'Changing settings files to making SSH use public key only:'
    print LINE
    if PLATFORM == LINUX_PLATFORM:
        _linux_make_ssh_public_key_only()
    elif PLATFORM == OS_X_PLATFORM:
        _os_x_make_ssh_public_key_only()
    else:
        print 'Platform is %r.' % (PLATFORM, )
        print 'Exiting make_ssh_public_key_only without doing anything.'


def matplotlib_suggestion(index):
    rc_file = mpl_backend = None
    try:
        import matplotlib
        mpl_backend = matplotlib.get_backend()
        rc_file = os.path.join(os.path.dirname(matplotlib.__file__),
                               'mpl-data', 'matplotlibrc')
    except ImportError:
        pass
    print '%d. Your current matplotlib backend is:' % (index, )
    print '       %s' % (mpl_backend, )
    print '   If you would like to change this, check your RC file:'
    print '       %s' % (rc_file, )


def _linux_suggestions():
    # NOTE: This is Linux only.
    print 'Optional suggestions for Linux:'
    print LINE
    print '0. To install old versions of Python, i.e. "dead snakes"'
    print '   Check out: http://askubuntu.com/a/141664'
    print '   This may be useful.'
    print '1. You may want to install pdfkt via'
    print '       sudo apt-get install pdftk'
    print '   to help extract information from PDF files.'
    matplotlib_suggestion(2)


def _os_x_suggestions():
    print '0. You may want to install pdfkt from'
    print '       http://www.pdflabs.com/tools/pdftk-server/'
    print '   to help extract information from PDF files.'
    matplotlib_suggestion(1)
    print '2. To install Emacs 24 on OS X, either visit'
    print '     http://stackoverflow.com/a/15084055/1068170'
    print '   or'
    print '     http://readystate4.com/2011/04/19/'


def suggestions():
    print 'Some optional/suggested things to install:'
    print LINE
    if PLATFORM == LINUX_PLATFORM:
        _linux_suggestions()
    elif PLATFORM == OS_X_PLATFORM:
        _os_x_suggestions()


def main():
    if getpass.getuser() != 'root':
        print 'Please run as root. This is required to install.'
        sys.exit(1)

    global PLATFORM  # pylint: disable=global-statement
    PLATFORM = platform.system()

    # These do no printing.
    check_python_version()
    add_session_file()

    add_rc_files()
    print SECTION_SEP
    add_symlinks()
    print SECTION_SEP
    add_packages()
    print SECTION_SEP
    add_python_packages()
    print SECTION_SEP
    make_ssh_public_key_only()
    print SECTION_SEP
    suggestions()


if __name__ == '__main__':
    # H/T: http://stackoverflow.com/a/9093598/1068170
    if hasattr(__builtin__, '__IPYTHON__'):
        print 'In IPYTHON, not running main().'
    else:
        main()
