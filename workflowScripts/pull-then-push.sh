#!/bin/bash

# Ensure the required environment variables are set
git config --global user.name "github-actions[bot]"
git config --global user.email "github-actions[bot]@users.noreply.github.com"
git add .
if [[ -n "$ISSUE_TITLE" && -n "$ISSUE_AUTHOR" ]]; then
  git commit -m "${ISSUE_TITLE} by ${ISSUE_AUTHOR}"
else
  git commit -m "Creating new game setup for all difficulties"
fi

git pull origin main -X ours || {
  echo "Automatic merge failed, aborting."
  git merge --abort
  exit 1
}

git push