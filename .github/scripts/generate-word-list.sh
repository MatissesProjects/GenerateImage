#!/bin/bash

# Function to filter words based on probability for a specific difficulty
select_words() {
  difficulty_index=$1
  word_count=$2
  echo "$WORD_LIST" | tr ',' '\n' | awk -F':' -v idx=$difficulty_index '{if (rand() < $(idx+1)) print $1}' | shuf | head -n $word_count | tr '\n' ',' | sed 's/,$//'
}

# Generate lists for each difficulty level
easy_WORD_LIST=$(select_words 1 10)
medium_WORD_LIST=$(select_words 2 7)
hard_WORD_LIST=$(select_words 3 5)

# Create the YAML files for each difficulty
for difficulty in easy medium hard; do
  WORDS_VAR="${difficulty}_WORD_LIST"
  awk -v options="${!WORDS_VAR}" -v difficulty="$difficulty" 'BEGIN {
    print "name: Transform the image (" difficulty ")";
    print "title: Game " difficulty " - do not change the title just fill out the form";
    print "description: A form to select the options available for transforming your current image.";
    print "";
    print "body:";
    print "  - type: markdown";
    print "    attributes:";
    print "      value: |";
    print "        ### You can select as many of these as you want:";
    print "  - type: checkboxes";
    print "    id: multi-selection";
    print "    attributes:";
    print "      label: Choose multiple";
    print "      options:";
    split(options, opts, ",");
    for (i in opts) {
      gsub(/^[ \t]+|[ \t]+$/, "", opts[i]);
      print "        - label: " opts[i];
      print "          required: false";
    }
  }' difficulty="$difficulty" > .github/ISSUE_TEMPLATE/${difficulty,,}.yml
done
