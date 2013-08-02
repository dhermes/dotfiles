source $HOME/.bashrc

if [[ "`uname`" == 'Darwin' ]]; then
  PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin:${PATH}:/usr/texbin:$HOME/go/bin:/usr/local/share/python3:/usr/local/git/bin"
  export PATH
  export PYTHONPATH=$PYTHONPATH:/usr/local/Cellar/pil/1.1.7/lib/python2.7/site-packages
fi

if [[ "`uname`" == 'Linux' ]]; then
  PATH="/usr/local/bin/google_appengine:${PATH}"
  export PATH
fi

# Get the aliases and functions
if [ -f /.bashrc ]; then
  . /.bashrc
fi
