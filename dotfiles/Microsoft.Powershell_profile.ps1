# Save as %USERPROFILE%\Documents\WindowsPowershell\Microsoft.PowerShell_profile.ps1 to save as user-level profile

############# Functions ##################

# Delete .ssh\known_hosts as a dirty fix for ssh "strict checking" error
function fn_rm_hosts {Remove-Item -Path C:\Users\cooper.hopkin\.ssh\known_hosts }

# List current Environment variables
function Get-Env { Get-ChildItem env:* | sort-object name }

# Change the command prompt, replace home directory path with bash-style "~"
function Prompt {
	#ANSI Escape char
	$ESC = [char]27
	#Directory names
	$current_dir="$ESC[32m$env:USERNAME@$env:COMPUTERNAME$ESC[0m:$ESC[34m" + (Get-Location) + "$ESC[0m$ "
	$home_dir = "C:$env:HOMEPATH"
	
	$current_dir.replace("$home_dir", '~')

}


############# Aliases ####################
Set-Alias -Name rm-hosts -Value fn_rm_hosts