# zsh alias file

#colored cat
alias cat='highlight $1 --out-format xterm256 --force -s manxome'
#colored cat with line numbers
alias lcat='cat -l'

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

#remove known host from .ssh/known-hosts
alias rm-host="ssh-keygen -f '/home/mightyficus/.ssh/known_hosts' -R"

# ssh into ubiquiti machines, fingerprint doesn't matter
function ussh
{
	ssh 	-o "ConnectTimeout 3" \
		-o "StrictHostKeyChecking no" \
	    	-o "UserKnownHostsFile /dev/null" \
		-i /home/mightyficus/.ssh/ui-laptop-wsl \
		"$@"
}

# ssh into ubiquiti devices (fingerprint doesn't matter, use legacy protocol)
function uscp
{
	exec scp	-O
			-o "ConnectTimeout 3" \
			-o "StrictHostKeyChecking no" \
	    		-o "UserKnownHostsFile /dev/null" \
			-i /home/mightyficus/.ssh/ui-laptop-wsl \
			"$@"
}
