#!/bin/bash

echo '{"easy":{},"medium":{},"hard":{}}' > PlayGame/currentVotes.json
echo '{"easy":{},"medium":{},"hard":{}}' > PlayGame/currentEntries.json
echo -e "# Votes\nnew competition started empty votes\n" > PlayGame/VotePage/CurrentVotes.md
echo -e '# To vote\nNo current entries\n\n## easy\nNo current entries\n\n## medium\nNo current entries\n\n## hard\nNo current entries\n' > PlayGame/VotePage/README.md
echo -n "$TARGET_URL" > PlayGame/currentStartImage.txt
echo -e "# Current competition\n\nGoal is to get as clost to the topic: \n### PlayGame/currentTopic.txt\n\n| Easy | Medium | Hard |\n| --- | --- | --- |\n| no current votes | no current votes | no current votes |" > PlayGame/winners.md
