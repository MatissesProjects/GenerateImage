#!/bin/bash

# Ensure the required environment variables are set
if [[ -z "$ISSUE_TITLE" || -z "$ISSUE_AUTHOR" ]]; then
  echo "ISSUE_TITLE and ISSUE_AUTHOR environment variables must be set."
  exit 1
fi

git config --global user.name "github-actions[bot]"
git config --global user.email "github-actions[bot]@users.noreply.github.com"
git add .
git commit -m "${ISSUE_TITLE} by ${ISSUE_AUTHOR}"
git pull --rebase origin main
git push