## bashrc should not be executed outside of log-in shells.
## SEE http://stackoverflow.com/a/12442753/1068170
## AND http://superuser.com/a/690749
## AND http://www.openssh.com/faq.html#2.9
if [[ -z "$PS1" ]]; then
   return
fi

# Need to use -nw since the alias below doesn't apply to root user
export EDITOR="emacs -nw"

alias cp="cp -i"
alias mv="mv -i"
alias rm="rm -i"
alias rmdir="rm -ir"

alias ls="ls -F"
alias ll="ls -alFG"

alias emacs="emacs -nw"
if [[ "`uname`" == 'Linux' ]]; then
  alias open="gnome-open"
  alias pbcopy="xclip -selection clipboard"
  alias pbpaste="xclip -selection clipboard -o"
fi

alias diff="diff -Nru"

source ~/.git-completion.bash

# BEGIN: Git specific prompt methods.
# From: https://gist.github.com/foosel/e46c649f4eb6a6e0fbde
# NOTE: git status slightly adapted from https://coderwall.com/p/pn8f0g

source ~/.bash_colors

# How does =~ work in BASH: http://stackoverflow.com/a/12454780/1068170
function git_color {
  if [[ $EUID -ne 0 ]]; then
    local git_status="$(git status 2> /dev/null)"

    if [[ ! $git_status =~ "working tree clean" ]]; then
      echo -e $bldred
    elif [[ $git_status =~ "Your branch is ahead of" ]]; then
      echo -e $bldylw
    elif [[ $git_status =~ "nothing to commit" ]]; then
      echo -e $bldgrn
    else
      echo -e $txtylw
    fi
  else
    echo -e $bldred
  fi
}

function git_branch {
  local git_status="$(git status 2> /dev/null)"
  local on_branch="On branch ([^${IFS}]*)"
  local on_commit="HEAD detached at ([^${IFS}]*)"

  if [[ $git_status =~ $on_branch ]]; then
    local branch=${BASH_REMATCH[1]}
    echo " ($branch)"
  elif [[ $git_status =~ $on_commit ]]; then
    local commit=${BASH_REMATCH[1]}
    echo " ($commit)"
  fi
}

if [[ $EUID -ne 0 ]]; then
  usercolor=$txtgrn
  pathcolor=$bldblu
  gitcolor=$bldylw
  promptcolor=$bldgrn
  prompt='\$'
else
  usercolor=$txtred
  promptcolor=$bldred
  pathcolor=$bldred
  gitcolor=$txtred
  prompt='#'
fi

PS1="\[$usercolor\]\u@\h\[$txtrst\] \[$pathcolor\]\w\[$txtrst\]"
# NOTE: Retain the escape, http://askubuntu.com/a/651875/439339
PS1+="\[\$(git_color)\]"
PS1+="\$(git_branch)"
PS1+=" \[$promptcolor\]$prompt\[$txtrst\] \[$bldwht\]"

# END: Git specific prompt methods.

# TODO(dhermes): Implement
# https://gist.github.com/1169093

bind '"\033[A": history-search-backward';
bind '"\033[B": history-search-forward';

# Sync history across screen
# Increase history size
HISTSIZE=1000
HISTFILESIZE=2000
# Don't put duplicate lines in the history.
HISTCONTROL=ignoredups:ignorespace
# Append to the history file, don't overwrite it
shopt -s histappend

# Check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# For inferior shells that don't define update_terminal_cwd
# http://stackoverflow.com/questions/85880
# http://superuser.com/questions/418559
function_exists() {
    declare -f -F $1 > /dev/null
    return $?
}
if ! function_exists "update_terminal_cwd"; then
    update_terminal_cwd() {
        return
    }
fi

# Update the prompt command with a history prefix if have not already.
# Should probably check for string containment rather than beginning
# with the prefix, though this brings it much closer to idempotent than
# it was before (especially with screen).
PROMPT_PREFIX="history -a; history -c; history -r;"
if [[ $PROMPT_COMMAND != ${PROMPT_PREFIX}* ]] ;
then
    export PROMPT_COMMAND="history -a; history -c; history -r; ${PROMPT_COMMAND:-:}"
fi

alias screen="screen -S djh-screen"
# For appsa, h/t http://stackoverflow.com/questions/592620
my_python() {
    if hash python2.7 2>/dev/null; then
        python2.7 "$@"
    else
        if hash python26 2>/dev/null; then
            python26 "$@"
        else
            if hash python2.6 2>/dev/null; then
                python2.6 "$@"
            else
                python2 "$@"
            fi
        fi
    fi
}
cd `my_python $HOME/dotfiles/add_screen_tab.py --new`
function cd() { builtin cd "$@" && my_python $HOME/dotfiles/add_screen_tab.py; }
# See http://stackoverflow.com/a/9256709/1068170
# for details on determining which signals are being caught.
trap "my_python $HOME/dotfiles/detect_term.py" TERM
trap "my_python $HOME/dotfiles/remove_screen_tab.py" EXIT

## H/T: http://superuser.com/a/707645/196822
if [[ -z "$SSH_AUTH_SOCK" || -z "$SSH_AGENT_PID" ]]; then
  if [[ -f $HOME/.ssh/github_rsa ]]; then
    echo "SSH Agent not set, setting agent.";
    eval $(ssh-agent);

    echo "";

    echo "SSH-Adding GitHub SSH key.";
    ssh-add $HOME/.ssh/github_rsa;
  fi
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

export NVM_DIR="${HOME}/.nvm"
[ -s "${NVM_DIR}/nvm.sh" ] && \. "${NVM_DIR}/nvm.sh"  # This loads nvm
[ -s "${NVM_DIR}/bash_completion" ] && \. "${NVM_DIR}/bash_completion"  # This loads nvm bash_completion
