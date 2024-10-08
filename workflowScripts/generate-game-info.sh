#!/bin/bash

# Ensure the required environment variables are set
if [[ -z "$TARGET_URL" || -z "$TOPIC" ]]; then
  echo "TARGET_URL and TOPIC environment variables must be set."
  exit 1
fi

echo "
# Game Information

Your goal is to take the picture

![CurrentImage](${TARGET_URL})

and transform it to the following topic 

<h3> ${TOPIC} </h3>

# To Play

You can select from multiple levels to play this game:

[Easy](https://github.com/MatissesProjects/GenerateImage/issues/new?title=Game%20easy%20Dont%20modify%20the%20title%20just%20use%20the%20form&template=easy.yml)

[Medium](https://github.com/MatissesProjects/GenerateImage/issues/new?title=Game%20medium%20Dont%20modify%20the%20title%20just%20use%20the%20form&template=medium.yml)

[Hard](https://github.com/MatissesProjects/GenerateImage/issues/new?title=Game%20hard%20Dont%20modify%20the%20title%20just%20use%20the%20form&template=hard.yml)

You can only have a single entry in each mode.

If you would like to start over, you can [delete your entry](https://github.com/MatissesProjects/GenerateImage/issues/new?title=DeleteEntry%20Dont%20modify%20the%20title%20just%20use%20the%20form&template=deleteEntry.yml).

# To Vote

You can go to the [vote page](https://github.com/MatissesProjects/GenerateImage/tree/main/PlayGame/VotePage).
" > PlayGame/README.md