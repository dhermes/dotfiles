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

function git_color {
  if [[ $EUID -ne 0 ]]; then
    local git_status="$(git status 2> /dev/null)"

    if [[ ! $git_status =~ "working directory clean" ]]; then
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
PS1+="\[\$(git_color)\]"
PS1+="\$(git_branch)"
PS1+=" \[$promptcolor\]$prompt\[$txtrst\] \[$bldwht\]"

# END: Git specific prompt methods.

# TODO(dhermes): Implement
# https://gist.github.com/1169093

bind '"\e[A": history-search-backward'
bind '"\e[B": history-search-forward'

# Sync history across screen
# Increase history size
HISTSIZE=1000
HISTFILESIZE=2000

# Custom autojump command.
alias jumpstat="autojump --stat"
if [[ "`uname`" == 'Darwin' ]]; then
  [[ -s `brew --prefix`/etc/autojump.sh ]] && . `brew --prefix`/etc/autojump.sh
fi

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
trap "my_python $HOME/dotfiles/remove_screen_tab.py" exit

## H/T: http://superuser.com/a/707645/196822
if [[ -z "$SSH_AUTH_SOCK" || -z "$SSH_AGENT_PID" ]]; then
  echo "SSH Agent not set, setting agent.";
  eval $(ssh-agent);

  echo "";

  echo "SSH-Adding GitHub SSH key.";
  ssh-add $HOME/.ssh/github_rsa;
fi
