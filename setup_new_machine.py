import os
import subprocess


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
    '$HOME/dotfiles/ssh': '$HOME/.ssh',
    '$HOME/dotfiles/Xmodmap': '$HOME/.Xmodmap',
}
# os.path.expanduser
# os.path.expandvars
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
]
pip_install = [
    'matplotlib',
    'numpy',
    'scipy',
    'pillow',
]


for source, symbolic_location in symlinks.iteritems():
  # NOTE: We could make this idempotent by using os.path.islink.
  src = os.path.expandvars(source)
  dst = os.path.expandvars(symbolic_location)
  os.symlink(src, dst)


apt_cmd = ['sudo', 'apt-get', 'install'] + aptitude_install
subprocess.check_output(*apt_cmd)
pip_cmd = ['sudo', 'pip', 'install', '--upgrade'] + pip_install
subprocess.check_output(*pip_cmd)
