source $HOME/.bashrc

if [[ "`uname`" == 'Darwin' ]]; then
  PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin:${PATH}:/usr/texbin:/usr/local/go/bin:/usr/local/git/bin"
  export PATH
  PYTHONPATH="/usr/local/lib/python2.7/site-packages:${PYTHONPATH}"
  export PYTHONPATH
fi

if [[ "`uname`" == 'Linux' ]]; then
  # ../usg/bin For Hopper/Carver/etc. at NERSC
  PATH="/usr/local/bin/google_appengine:${PATH}:/usr/common/usg/bin"
  export PATH
fi

# Get the aliases and functions
if [ -f /.bashrc ]; then
  . /.bashrc
fi

## Macaulay 2 start
if [ -f ~/.profile-Macaulay2 ]
then . ~/.profile-Macaulay2
fi
## Macaulay 2 end

# The next line updates PATH for the Google Cloud SDK.
source $HOME/google-cloud-sdk/path.bash.inc

# The next line enables bash completion for gcloud.
source $HOME/google-cloud-sdk/completion.bash.inc

# Activate global completion for the argcomplete library.
source $HOME/.bash_completion.d/python-argcomplete.sh
