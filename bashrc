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

export PROMPT_COMMAND="history -a; history -c; history -r; ${PROMPT_COMMAND:-:}"

alias screen="screen -S djh-screen"
cd `python $HOME/dotfiles/add_screen_tab.py --new`
function cd() { builtin cd "$@" && python $HOME/dotfiles/add_screen_tab.py; }
trap "python $HOME/dotfiles/remove_screen_tab.py" exit
