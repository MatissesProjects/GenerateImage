#!/bin/bash

# Ensure the required environment variables are set
git config --global user.name "github-actions[bot]"
git config --global user.email "github-actions[bot]@users.noreply.github.com"
git add .
if [[ -z "$ISSUE_TITLE" && -z "$ISSUE_AUTHOR" ]]; then
  git commit -m "${ISSUE_TITLE} by ${ISSUE_AUTHOR}"
else
  git commit -m "Creating new game setup for all difficulties"
fi
git pull --rebase origin main
git push