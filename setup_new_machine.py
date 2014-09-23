#!/usr/bin/env python

import __builtin__
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
]
PIP_INSTALL = [
    'matplotlib',
    'numpy',
    'scipy',
    'pillow',
    'mercurial',
    'readline',  # HAS ISSUES, MIGHT NEED TO TARGET A VERSIOn
    'ipython',
    'virtualenv',
    'tox',
    'unittest2',
    'nose',
]
LINE = '-' * 70


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
  # NOTE: This must run before `add_symlinks`.
  hgrc_fi = os.path.expandvars('$HOME/dotfiles/hgrc')
  hgrc_template_fi = hgrc_fi + '.pytemplate'
  with open(hgrc_template_fi, 'r') as fh:
    hgrc_template = string.Template(fh.read())

  netrc_fi = os.path.expandvars('$HOME/dotfiles/netrc')
  netrc_template_fi = netrc_fi + '.pytemplate'
  with open(netrc_template_fi, 'r') as fh:
    netrc_template = string.Template(fh.read())

  # Get the template values to be placed into rc files.
  codehosting_email = raw_input('Email for Google Code Hosting: ')
  print 'NOTE: Google Code Hosting password can be found at'
  print '      https://code.google.com/hosting/settings'
  codehosting_password = getpass.getpass('Password for Google Code Hosting: ')
  substitution_dict = {
      'codehosting_email': codehosting_email,
      'codehosting_password': codehosting_password,
  }

  # Make substitutions and write to files.
  with open(hgrc_fi, 'w') as fh:
    fh.write(hgrc_template.substitute(substitution_dict))
    print 'Wrote:', hgrc_fi

  with open(netrc_fi, 'w') as fh:
    fh.write(netrc_template.substitute(substitution_dict))
    print 'Wrote:', netrc_fi


def add_symlinks():
  # NOTE: This must run after `add_rc_files`.
  print 'Adding symlinks:'
  print LINE

  for source, symbolic_location in SYMLINKS.iteritems():
    # NOTE: We could make this idempotent by using os.path.islink.
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


def _linux_add_packages():
  # NOTE: This is Linux only. (Really even more specific than Linux.)
  print 'Adding Linux packages:'
  print LINE

  apt_cmd = ['apt-get', 'install', '-y'] + APTITUDE_INSTALL
  subprocess.check_call(apt_cmd)


def add_packages():
  if PLATFORM == LINUX_PLATFORM:
    _linux_add_packages()


def add_python_packages():
  # NOTE: This is OS agnostic.
  print 'Adding Python packages:'
  print LINE

  # First install `pip`.
  subprocess.check_call(['easy_install', '--upgrade', 'pip'])

  # Then use `pip` to install all desired packages.
  pip_cmd = ['pip', 'install', '--upgrade'] + PIP_INSTALL
  subprocess.check_call(pip_cmd)


def _linux_make_ssh_public_key_only():
  # NOTE: This is Linux only.

  # See:
  # ('http://www.linux.org/threads/how-to-force-ssh-login-via-'
  #  'public-key-authentication.4253/')
  # ('https://www.digitalocean.com/community/tutorials/'
  #  'how-to-set-up-ssh-keys--2')
  ssh_config_fi = '/etc/ssh/sshd_config'
  ssh_config_fi_backup = ssh_config_fi + '.factory-defaults'

  # Create a backup.
  shutil.copyfile(ssh_config_fi, ssh_config_fi_backup)

  with open(ssh_config_fi, 'r') as fh:
    original_contents = fh.read()

  lines = original_contents.split('\n')
  password_lines = [(i, line) for i, line in enumerate(lines)
                    if 'PasswordAuthentication' in line]
  if len(password_lines) != 1:
    raise ValueError('Non-unique match for PasswordAuthentication.')

  i, line = password_lines[0]
  do_replace = raw_input('Replace line: %r? [y/N] ' % line)
  if do_replace.strip().lower() != 'y':
    raise ValueError('Line rejected by user.')

  lines[i] = 'PasswordAuthentication no'
  with open(ssh_config_fi, 'w') as fh:
    fh.write('\n'.join(lines))

  # Restart ssh server.
  subprocess.check_call(['restart', 'ssh'])


def _os_x_make_ssh_public_key_only():
  # NOTE: This is Mac OS X only.

  # See: http://serverfault.com/a/86007
  ssh_config_fi = '/private/etc/sshd_config'
  ssh_config_fi_backup = ssh_config_fi + '.factory-defaults'

  # Create a backup.
  shutil.copyfile(ssh_config_fi, ssh_config_fi_backup)

  with open(ssh_config_fi, 'r') as fh:
    original_contents = fh.read()

  lines = original_contents.split('\n')

  # Turn PasswordAuthentication off.
  password_lines = [(i, line) for i, line in enumerate(lines)
                    if line == '#PasswordAuthentication no']
  if len(password_lines) != 1:
    raise ValueError('Non-unique match for PasswordAuthentication.')

  i, line = password_lines[0]
  do_replace = raw_input('Replace line: %r? [y/N] ' % line)
  if do_replace.strip().lower() != 'y':
    raise ValueError('Line rejected by user.')

  lines[i] = 'PasswordAuthentication no'

  # Turn ChallengeResponseAuthentication off.
  challenge_lines = [(i, line) for i, line in enumerate(lines)
                     if line == '#ChallengeResponseAuthentication yes']
  if len(challenge_lines) != 1:
    raise ValueError('Non-unique match for PasswordAuthentication.')

  i, line = challenge_lines[0]
  do_replace = raw_input('Replace line: %r? [y/N] ' % line)
  if do_replace.strip().lower() != 'y':
    raise ValueError('Line rejected by user.')

  lines[i] = 'ChallengeResponseAuthentication no'

  # Write new lines to file.
  with open(ssh_config_fi, 'w') as fh:
    fh.write('\n'.join(lines))

  # NOTE: (Quote from the server fault page)
  #       "If you are using a stock install (i.e., you didn't build/install
  #        it yourself from source), launchd should take care of picking up
  #        the new config without having to restart the daemon."


def make_ssh_public_key_only():
  if PLATFORM == LINUX_PLATFORM:
    _linux_make_ssh_public_key_only()
  elif PLATFORM == OS_X_PLATFORM:
    _os_x_make_ssh_public_key_only()
  else:
    print 'Platform is %r.' % (PLATFORM,)
    print 'Exiting make_ssh_public_key_only without doing anything.'


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


def _os_x_suggestions():
  print '0. You may want to install pdfkt from'
  print '       http://www.pdflabs.com/tools/pdftk-server/'
  print '   to help extract information from PDF files.'


def suggestions():
  if PLATFORM == LINUX_PLATFORM:
    _linux_suggestions()
  elif PLATFORM == OS_X_PLATFORM:
    _os_x_suggestions()


def main():
  if getpass.getuser() != 'root':
    print 'Please run as root. This is required to install.'
    sys.exit(1)

  global PLATFORM
  PLATFORM = platform.system()

  check_python_version()
  print LINE
  add_rc_files()
  print LINE
  add_symlinks()
  print LINE
  add_packages()
  print LINE
  add_python_packages()
  print LINE
  make_ssh_public_key_only()
  print LINE
  suggestions()


if __name__ == '__main__':
  # H/T: http://stackoverflow.com/a/9093598/1068170
  if hasattr(__builtin__, '__IPYTHON__'):
    print 'In IPYTHON, not running main().'
  else:
    main()
