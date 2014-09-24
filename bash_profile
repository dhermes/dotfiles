source $HOME/.bashrc

# Get the aliases and functions
if [ -f /.bashrc ]; then
  . /.bashrc
fi

# The next line updates PATH for the Google Cloud SDK.
source $HOME/google-cloud-sdk/path.bash.inc

# The next line enables bash completion for gcloud.
source $HOME/google-cloud-sdk/completion.bash.inc

# Activate global completion for the argcomplete library.
source $HOME/.bash_completion.d/python-argcomplete.sh

NODE_PATH="/usr/local/lib/node_modules:${NODE_PATH}"
export NODE_PATH
