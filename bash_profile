# Allow custom bin for systems without root privilege.
if [[ -d "${HOME}/bin" ]]; then
  export PATH="${HOME}/bin:${PATH}"
fi

# The next line updates PATH for the Google Cloud SDK.
if [[ -f ${HOME}/google-cloud-sdk/path.bash.inc ]]; then
  source ${HOME}/google-cloud-sdk/path.bash.inc
fi

# For changes to PATH (or other env vars) which only belong on a
# temporary machine or involve a temporary install:
if [[ -f ${HOME}/.local_profile_extensions ]]; then
  source ${HOME}/.local_profile_extensions
fi

if [[ -d "/usr/local/go/bin" ]]; then
    export PATH="${PATH}:/usr/local/go/bin"
fi

# NOTE: The `visual-studio-code` plugin for `bash-it` takes precedence here:
# $ type code
# code is a function
# code ()
# {
#     about 'Starts Visual Studio Code in the provided directory';
#     group 'visual-studio-code';
#     VSCODE_CWD="$PWD" open -n -b "com.microsoft.VSCode" --args $*
# }
if [[ "$(uname)" == 'Darwin' ]]; then
  export PATH="${PATH}:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"
fi

if [[ -d "${HOME}/.pyenv" ]]; then
  export PYENV_ROOT="${HOME}/.pyenv"
  export PATH="${PYENV_ROOT}/bin:${PATH}"
fi

if [[ -d ${HOME}/.nodenv/bin ]]; then
  export PATH="${HOME}/.nodenv/bin:${PATH}"
fi

# Get the aliases and functions
if [[ -f ${HOME}/.bashrc ]]; then
  source ${HOME}/.bashrc
fi
