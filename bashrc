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

#autojump
_autojump()
{
        local cur
        cur=${COMP_WORDS[*]:1}
        while read i
        do
            COMPREPLY=("${COMPREPLY[@]}" "${i}")
        done  < <(autojump --bash --completion $cur)
}

complete -F _autojump j
data_dir=$([ -e ~/.local/share ] && echo ~/.local/share || echo ~)
export AUTOJUMP_HOME=${HOME}

if [[ "$data_dir" = "${HOME}" ]]
then
    export AUTOJUMP_DATA_DIR=${data_dir}
else
    export AUTOJUMP_DATA_DIR=${data_dir}/autojump
fi

if [ ! -e "${AUTOJUMP_DATA_DIR}" ]
then
    mkdir "${AUTOJUMP_DATA_DIR}"
    mv ~/.autojump_py "${AUTOJUMP_DATA_DIR}/autojump_py" 2>>/dev/null #migration
    mv ~/.autojump_py.bak "${AUTOJUMP_DATA_DIR}/autojump_py.bak" 2>>/dev/null
    mv ~/.autojump_errors "${AUTOJUMP_DATA_DIR}/autojump_errors" 2>>/dev/null
fi

AUTOJUMP='{ [[ "$AUTOJUMP_HOME" == "$HOME" ]] && (autojump -a "$(pwd -P)"&)>/dev/null 2>>${AUTOJUMP_DATA_DIR}/autojump_errors;} 2>/dev/null'

alias jumpstat="autojump --stat"
function j { new_path="$(autojump $@)";if [ -n "$new_path" ]; then echo -e "\\033[31m${new_path}\\033[0m"; cd "$new_path";else false; fi }

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

export PROMPT_COMMAND="history -a; history -c; history -r; : ; { [[ "$AUTOJUMP_HOME" == "$HOME" ]] && (autojump -a "$(pwd -P)"&)>/dev/null 2>>${AUTOJUMP_DATA_DIR}/autojump_errors;} 2>/dev/null"

alias screen="screen -S djh-screen"
cd `python $HOME/dotfiles/add_screen_tab.py --new`
function cd() { builtin cd "$@" && python $HOME/dotfiles/add_screen_tab.py; }
trap "python $HOME/dotfiles/remove_screen_tab.py" exit
