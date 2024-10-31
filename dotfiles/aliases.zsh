# zsh alias file

#colored cat
alias cat='highlight $1 --out-format xterm256 -l --force -s manxome'

# Pipe highlight to less
export LESSOPEN="| $(which highlight) %s --out-format xterm256 -l --force -s manxome --no-trailing-nl"
export LESS=" -R"
alias less='less -m -g -i -J'
alias more='less'

# ls aliases
alias ll='ls -lFh'
alias la='ls -lAFh'
alias ldot='ls -ld .*' # list all dotfiles

# File Handling
alias rm='rm -I'
alias zshrc='${=EDITOR} ~/.zshrc'
alias dud='du -d 1 -h -a' #display the size of file at depth 1 in current location
alias t='tail -f' # live output of end of file

# find
alias fd='find . -type d -iname'
alias ff='find . -type f -iname'

# Other
alias h='history'
alias hgrep='fc -l 0 | grep'

# dig with just answers
alias digr='dig +nostats +nocomments +nocmd'
