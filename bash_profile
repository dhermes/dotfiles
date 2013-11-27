source $HOME/.bashrc

if [[ "`uname`" == 'Darwin' ]]; then
  PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin:${PATH}:/usr/texbin:$HOME/go/bin:/usr/local/git/bin"
  export PATH
  [[ -s `brew --prefix`/etc/autojump.sh ]] && . `brew --prefix`/etc/autojump.sh
fi

if [[ "`uname`" == 'Linux' ]]; then
  PATH="/usr/local/bin/google_appengine:${PATH}"
  export PATH
fi

# Get the aliases and functions
if [ -f /.bashrc ]; then
  . /.bashrc
fi
