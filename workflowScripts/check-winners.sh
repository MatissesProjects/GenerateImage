#!/bin/bash

# Define the path to your JSON files
VOTES_JSON_FILE="PlayGame/currentVotes.json"
ENTRIES_JSON_FILE="PlayGame/currentEntries.json"
OUTPUT_FILE="PlayGame/winners.txt"

# Clear the output file before writing new data
echo "Current competition winners" > "$OUTPUT_FILE"

# Function to find the key (entry) with the max votes for a given difficulty level
find_max_votes_entry() {
  difficulty=$1
  max_votes=0
  name_of_person=""
  url_of_max=""

  # Get all entries for the given difficulty from the votes file
  entries=$(jq -r --arg level "$difficulty" '.[$level] | keys[]?' "$VOTES_JSON_FILE")

  if [ -z "$entries" ]; then
    echo "No entries found for $difficulty level."
    echo "$difficulty - had no entries" >> "$OUTPUT_FILE"
    return
  fi

  for entry in $entries; do
    # Get the number of contributors (votes) for this entry
    votes_count=$(jq -r --arg level "$difficulty" --arg entry "$entry" '.[$level][$entry] | length' "$VOTES_JSON_FILE")

    # Check if this entry has more votes than the current max
    if (( votes_count > max_votes )); then
      max_votes=$votes_count
      name_of_person=$entry
    fi
  done

  if [ -n "$name_of_person" ]; then
    # Retrieve the URL for the winning entry from the currentEntries.json file
    url_of_max=$(jq -r --arg level "$difficulty" --arg name "$name_of_person" '.[$level][$name]' "$ENTRIES_JSON_FILE")

    # Output the winner's name and URL
    echo "$difficulty - $name_of_person - $url_of_max" >> "$OUTPUT_FILE"
  else
    echo "$difficulty - no winner" >> "$OUTPUT_FILE"
  fi
}

# Process each difficulty level
for difficulty in "easy" "medium" "hard"; do
  find_max_votes_entry "$difficulty"
done
