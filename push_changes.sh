#!/bin/bash

# Function to run git command with error handling
run_git_command() {
    command=$1
    eval $command
    if [ $? -ne 0 ]; then
        echo "Error running command: $command"
        exit 1
    fi
}

# Git fetch
run_git_command "git fetch"

# Git add
files_to_stage="${@:1:($#-1)}"
run_git_command "git add $files_to_stage"

# Git commit
commit_message="${!#}"
run_git_command "git commit -m \"$commit_message\""

# Git rebase
run_git_command "git rebase origin/dev/backend2"

# Git push
run_git_command "git push origin dev/backend2"