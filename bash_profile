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

# For changes to PATH (or other env vars) which only belong on a
# temporary machine or involve a temporary install:
if [[ -f $HOME/.local_profile_extensions ]]; then
  source $HOME/.local_profile_extensions
fi

NODE_PATH="/usr/local/lib/node_modules:${NODE_PATH}"
export NODE_PATH
