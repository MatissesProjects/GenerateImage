#!/bin/bash

# Define the path to your JSON file
JSON_FILE="PlayGame/currentVotes.json"

# Function to find the key (entry) with the max votes for a given difficulty level
find_max_votes_entry() {
  difficulty=$1
  max_votes=0
  url_of_max=""

  # Get all entries for the given difficulty
  entries=$(jq -r --arg level "$difficulty" '.[$level] | keys[]?' "$JSON_FILE")

  if [ -z "$entries" ]; then
    echo "No entries found for $difficulty level."
    echo "" > PlayGame/"$difficulty-winner.txt"
    return
  fi

  for entry in $entries; do
    # Get the number of contributors (votes) for this entry
    votes_count=$(jq -r --arg level "$difficulty" --arg entry "$entry" '.[$level][$entry] | length' "$JSON_FILE")

    # Check if this entry has more votes than the current max
    if (( votes_count > max_votes )); then
      max_votes=$votes_count
      url_of_max=$entry
    fi
  done
  echo "$url_of_max" > PlayGame/"$difficulty-winner.txt"
}

# Process each difficulty level
for difficulty in "easy" "medium" "hard"; do
  find_max_votes_entry "$difficulty"
done
