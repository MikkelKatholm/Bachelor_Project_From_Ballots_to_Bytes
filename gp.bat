@echo off

:: Display current Git status
git status

:: Add all changes to the staging area
git add .

:: Prompt the user for a commit message
set /p commit_message="Enter your commit message: "

:: Commit changes with the provided message or a default message if none is provided
if "%commit_message%"=="" (
  git commit -m "Shit not work"
) else (
  git commit -m "%commit_message%"
)

:: Push changes to the remote repository (assuming the branch is 'main', change it if needed)
git push origin main
