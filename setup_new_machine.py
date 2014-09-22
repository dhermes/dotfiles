import getpass
import os
import platform
import shutil
import subprocess
import sys


symlinks = {
    '$HOME/dotfiles/bash-colors': '$HOME/.bash-colors',
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
}
aptitude_install = [
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
]
pip_install = [
    'matplotlib',
    'numpy',
    'scipy',
    'pillow',
]


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
  subprocess.check_output(['restart', 'ssh'])


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
  base_platform = platform.system()
  # NOTE: This is Linux only.
  if base_platform == 'Linux':
    _linux_make_ssh_public_key_only()
  elif base_platform == 'Darwin':
    _os_x_make_ssh_public_key_only()
  else:
    print 'Platform is %r.' % (base_platform,)
    print 'Exiting make_ssh_public_key_only without doing anything.'


def main():
  for source, symbolic_location in symlinks.iteritems():
    # NOTE: We could make this idempotent by using os.path.islink.
    src = os.path.expandvars(source)
    dst = os.path.expandvars(symbolic_location)
    os.symlink(src, dst)

  apt_cmd = ['apt-get', 'install', '-y'] + aptitude_install
  subprocess.check_output(*apt_cmd)
  pip_cmd = ['pip', 'install', '--upgrade'] + pip_install
  subprocess.check_output(*pip_cmd)

  make_ssh_public_key_only()


if __name__ == '__main__':
  if getpass.getuser() != 'root':
    print 'Please run as root. This is required to install.'
    sys.exit(1)

  main()
