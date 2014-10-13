# Get the aliases and functions
if [[ -f $HOME/.bashrc ]]; then
  source $HOME/.bashrc
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
  source $HOME/.bash_completion.d/python-argcomplete.sh
fi

NODE_PATH="/usr/local/lib/node_modules:${NODE_PATH}"
export NODE_PATH
