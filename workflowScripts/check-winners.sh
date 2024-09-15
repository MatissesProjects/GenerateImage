#!/bin/bash

# Define the path to your JSON files
VOTES_JSON_FILE="PlayGame/currentVotes.json"
ENTRIES_JSON_FILE="PlayGame/currentEntries.json"
OUTPUT_FILE="PlayGame/winners.md"
CURRENT_TOPIC="PlayGame/currentTopic.txt"

# Clear the output file before writing new data
echo "# Current competition" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "Goal is to get as clost to the topic: " >> "$OUTPUT_FILE"
echo "### $CURRENT_TOPIC" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "| Easy | Medium | Hard |" >> "$OUTPUT_FILE"
echo "| --- | --- | --- |" >> "$OUTPUT_FILE"

# Function to find the key (entry) with the max votes for a given difficulty level
find_max_votes_entry() {
  difficulty=$1
  max_votes=0
  name_of_person=""
  url_of_max=""

  # Get all entries for the given difficulty from the votes file
  entries=$(jq -r --arg level "$difficulty" '.[$level] | keys[]?' "$VOTES_JSON_FILE")

  if [ -z "$entries" ]; then
    # Add "had no entries" to the corresponding column for this difficulty
    if [ "$difficulty" = "easy" ]; then
      easy_result="had no entries"
    elif [ "$difficulty" = "medium" ]; then
      medium_result="had no entries"
    elif [ "$difficulty" = "hard" ]; then
      hard_result="had no entries"
    fi
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

    # Format the entry for this difficulty in Markdown with name and image
    if [ "$difficulty" = "easy" ]; then
      easy_result="$name_of_person <br> <img src=\"$url_of_max\" alt=\"$name_of_person\" width=\"250\" height=\"250\">"
    elif [ "$difficulty" = "medium" ]; then
      medium_result="$name_of_person <br> <img src=\"$url_of_max\" alt=\"$name_of_person\" width=\"250\" height=\"250\">"
    elif [ "$difficulty" = "hard" ]; then
      hard_result="$name_of_person <br> <img src=\"$url_of_max\" alt=\"$name_of_person\" width=\"250\" height=\"250\">"
    fi
  else
    # If no winner, output no winner text
    if [ "$difficulty" = "easy" ]; then
      easy_result="had no winner"
    elif [ "$difficulty" = "medium" ]; then
      medium_result="had no winner"
    elif [ "$difficulty" = "hard" ]; then
      hard_result="had no winner"
    fi
  fi
}

# Initialize variables for each difficulty
easy_result="had no entries"
medium_result="had no entries"
hard_result="had no entries"

# Process each difficulty level
for difficulty in "easy" "medium" "hard"; do
  find_max_votes_entry "$difficulty"
done

# Output the results to the Markdown table
echo "| $easy_result | $medium_result | $hard_result |" >> "$OUTPUT_FILE"
