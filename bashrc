#!/usr/bin/env bash

export BASH_SILENCE_DEPRECATION_WARNING=1

# If not running interactively, don't do anything
case $- in
  *i*) ;;
    *) return;;
esac

# NOTE: `pyenv` and `nodenv` set up is handled by `bash-it`

# Path to the bash it configuration
export BASH_IT="${HOME}/.bash_it"

# Lock and Load a custom theme file.
# Leave empty to disable theming.
# location /.bash_it/themes/
export BASH_IT_THEME='powerline-multiline'  # Default is 'bobby'
export POWERLINE_LEFT_PROMPT="scm python_venv ruby aws_vault cwd"
export POWERLINE_PROMPT_CHAR="$"

# H/T: https://jonasjacek.github.io/colors/
AWS_VAULT_THEME_PROMPT_COLOR=130

function __powerline_aws_vault_prompt {
  set +u
  local aws_vault=""

  if [[ -n "${AWS_VAULT}" ]]; then
    aws_vault="[a] ${AWS_VAULT}"
  fi

  [[ -n "${aws_vault}" ]] && echo "${aws_vault}|${AWS_VAULT_THEME_PROMPT_COLOR}"
}

# (Advanced): Change this to the name of your remote repo if you
# cloned bash-it with a remote other than origin such as `bash-it`.
# export BASH_IT_REMOTE='bash-it'

# Your place for hosting Git repos. I use this for private repos.
export GIT_HOSTING='git@git.domain.com'

# Don't check mail when opening terminal.
unset MAILCHECK

# Change this to your console based IRC client of choice.
export IRC_CLIENT='irssi'

# Set this to the command you use for todo.txt-cli
export TODO="t"

# Set this to false to turn off version control status checking within the prompt for all themes
export SCM_CHECK=true

# Set Xterm/screen/Tmux title with only a short hostname.
# Uncomment this (or set SHORT_HOSTNAME to something else),
# Will otherwise fall back on $HOSTNAME.
#export SHORT_HOSTNAME=$(hostname -s)

# Set Xterm/screen/Tmux title with only a short username.
# Uncomment this (or set SHORT_USER to something else),
# Will otherwise fall back on $USER.
#export SHORT_USER=${USER:0:8}

# Set Xterm/screen/Tmux title with shortened command and directory.
# Uncomment this to set.
#export SHORT_TERM_LINE=true

# Set vcprompt executable path for scm advance info in prompt (demula theme)
# https://github.com/djl/vcprompt
#export VCPROMPT_EXECUTABLE=~/.vcprompt/bin/vcprompt

# (Advanced): Uncomment this to make Bash-it reload itself automatically
# after enabling or disabling aliases, plugins, and completions.
# export BASH_IT_AUTOMATIC_RELOAD_AFTER_CONFIG_CHANGE=1

# Uncomment this to make Bash-it create alias reload.
# export BASH_IT_RELOAD_LEGACY=1

# Load Bash It
source "$BASH_IT"/bash_it.sh
# BEGIN: Remove after https://github.com/Bash-it/bash-it/issues/1882
eval "$(pyenv init --path)"
#   END: Remove after https://github.com/Bash-it/bash-it/issues/1882

# Make sure we on't clobber files by mistake.
alias cp="cp -i"
alias mv="mv -i"
alias rm="rm -i"
alias rmdir="rm -ir"

if [[ "$(uname)" == 'Darwin' ]]; then
  alias ls="ls -F"
  alias ll="ls -alFG"
  alias nproc="sysctl -n hw.logicalcpu" # As opposed to `hw.physicalcpu`
else
  alias ls="ls -F --color=auto"
  alias ll="ls -alFG --color=auto"
fi

alias diff="diff -Nru"
alias which="type -all"

# Unfortunately sometimes `bash-it` adds an empty segment to the
# `${PROMPT_COMMAND}`. This happens on macOS when there is mixed use of
# login and non-login shells.
export PROMPT_COMMAND=${PROMPT_COMMAND/;;/;}

# Update the prompt command with a history prefix if have not already.
# It should probably check for string containment rather than beginning
# with the prefix, though this brings it close to idempotent.
# See also:
# - https://unix.stackexchange.com/a/48113/89278
# - https://github.com/Bash-it/bash-it/blob/master/lib/history.bash
PROMPT_PREFIX="history -a; history -c; history -r;"
if [[ ! $PROMPT_COMMAND =~ ${PROMPT_PREFIX} ]] ;
then
    export PROMPT_COMMAND="history -a; history -c; history -r; ${PROMPT_COMMAND:-:}"
fi
