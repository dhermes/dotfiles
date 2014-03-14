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

# http://stackoverflow.com/questions/4133904
function git_branch_string {
    local __curr_branch="`git rev-parse --abbrev-ref HEAD 2> /dev/null`"
    if [[ $__curr_branch != "" ]]; then
      __curr_branch=" ($__curr_branch)"
    fi
    IFS='' && echo $__curr_branch
}
export PS1='\h:\W`git_branch_string` \u$ '

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

## Macaulay 2 start
if [ -f ~/.profile-Macaulay2 ]
then . ~/.profile-Macaulay2
fi
## Macaulay 2 end
