# Get the aliases and functions
if [[ -f $HOME/.bashrc ]]; then
  source $HOME/.bashrc
fi

# Allow custom bin for systems without root privilege.
if [[ -d "$HOME/bin" ]]; then
  export PATH="$HOME/bin:$PATH"
fi

# The next line updates PATH for the Google Cloud SDK.
if [[ -f $HOME/google-cloud-sdk/path.bash.inc ]]; then
  source $HOME/google-cloud-sdk/path.bash.inc
fi

# The next line enables bash completion for gcloud.
if [[ -f $HOME/google-cloud-sdk/completion.bash.inc ]]; then
  source $HOME/google-cloud-sdk/completion.bash.inc
fi

# Activate global completion for the argcomplete library.
if [[ -f $HOME/.bash_completion.d/python-argcomplete.sh ]]; then
  # Only install on bash>=4.2, since -D option is needed.
  # H/T: http://stackoverflow.com/a/9450628/1068170
  FULL_VERSION=${BASH_VERSION%%[^0-9.]*}
  MAJOR_VERSION=${FULL_VERSION%%[^0-9]*}
  MINOR_VERSION=${FULL_VERSION#[0-9].}
  MINOR_VERSION=${MINOR_VERSION%%[^0-9]*}
  if [[ $MAJOR_VERSION -ge 5 || ($MAJOR_VERSION == 4 && $MINOR_VERSION -ge 2) ]]; then
    source $HOME/.bash_completion.d/python-argcomplete.sh
  fi
fi

NODE_PATH="/usr/local/lib/node_modules:${NODE_PATH}"
export NODE_PATH
