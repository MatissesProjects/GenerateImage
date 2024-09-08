import github
import os
import json
import re
import requests
import random

ISSUE_NUMBER = int(os.getenv("ISSUE_NUMBER"))
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
matisseId = "630649313860780043" # matisse's discord id, not sensitive info

headers = {
    'authority': 'deepnarrationapi.matissetec.dev',
    'accept': '/',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'text/plain;charset=UTF-8',
    'origin': 'https://deepnarration.matissetec.dev/',
    'pragma': 'no-cache',
    'referer': 'https://deepnarration.matissetec.dev/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

def close_with_error(issue, msg):
    print(f"We are closing the issue with the following error: {msg} label: Invalid")
    issue.create_comment(f"ERROR: {msg}")
    issue.edit(state="closed", labels=["Invalid"])

def parseCheckBoxData(text):
    choose_multiple_matches = re.findall(r'- \[X\] (.+)', text)
    return choose_multiple_matches

def deleteEntry(issue):
    user = issue.user.login
    removeThese = parseCheckBoxData(issue.body)
    print(f"Entries to Remove: {removeThese}")
    if len(removeThese) == 0:
        issue.create_comment("No entries to remove.")
        issue.edit(state="closed")
        return

    try:
        with open("./PlayGame/currentEntries.json", "r") as f:
            jsonData = json.load(f)
        with open("./PlayGame/currentVotes.json", "r") as f:
            voteData = json.load(f)
    except FileNotFoundError:
        print("Error: JSON file not found.")
        return
    except json.JSONDecodeError:
        print("Error: JSON file is not valid.")
        return
    for level in removeThese:
        if user in jsonData[level]:
            del jsonData[level][user]
        if user in voteData[level]:
            del voteData[level][user]
    print(jsonData)
    try:
        with open("./PlayGame/currentEntries.json", "w") as f:
            json.dump(jsonData, f, indent=4)
        print("Updated JSON file successfully.")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")
        return

def playGame(issue):
    # print(issue.body)
    textToRiffWith = ', '.join(parseCheckBoxData(issue.body))
    print(f"text we are trying to use: {textToRiffWith}")
    with open("./PlayGame/currentStartImage.txt", "r") as f:
        targetLocalImage = f.read()
    data1 = {"discordId":matisseId,"discordUsername":"matisse","targetPicture":targetLocalImage,"prompt":textToRiffWith,"id":random.randint(1000,9999), "accessToken": DISCORD_TOKEN}
    print("starting request to backend")
    response1 = requests.post('https://deepnarrationapi.matissetec.dev/startSimilarImages', headers=headers, json=data1)
    imageLocation = response1.text
    if len(imageLocation) > 300:
        close_with_error(issue, "Error generating image, the response was wrong")
        return
    print("resulting image location: ", imageLocation)
    issue.create_comment(f"Here is your image:\n![{imageLocation}]({imageLocation})\nDo you want to enter this for your current difficulty level? (one entry per difficulty level)\n\n- [Yes](https://github.com/MatissesProjects/GenerateImage/issues/new?template=enterCurrentImage.yml)\nif no you are done, or optionally you can answer the form no.")

    with open("./PlayGame/currentEntries.json", "r") as f:
        jsonData = json.load(f)
    with open("./PlayGame/currentEntries.json", "w") as f:
        # get the game mode from the title
        gameMode = issue.title.split(" ")[1]
        if gameMode in ["easy", "medium", "hard"]:
            jsonData[gameMode][issue.user.login] = imageLocation
        f.write(json.dumps(jsonData, indent=4))
    print(jsonData)
    modifyVotePageReadme(jsonData)

def modifyVotePageReadme(jsonData):
    with open("./PlayGame/VotePage/README.md", "w+") as f:
        f.write("# To vote\n")
        f.write("Click on the image and submit the issue\n")
        topic = "tree on the beach" # put into env variable
        f.write(f"Topic is to create a {topic}\n\n")
        for level in jsonData:
            f.write(f"## {level}\n")
            f.write(f"<details><summary>Click to {level}</summary>\n\n")
            for user, image in jsonData[level].items():
                # Wrap the image with a link to make it clickable
                f.write(f"[![Vote for {user}]({image})](https://github.com/MatissesProjects/GenerateImage/issues/new?title=Vote%20for%20{user}%20{level}&body=Good%20luck%20to%20{user}%20thank%20you%20for%20voting.%20One%20vote%20per%20difficulty)\n")
            f.write("</details>\n\n")

def voteForImage(voterName, userToVoteFor, level):
    if level not in ["easy", "medium", "hard"]:
        return
    with open("./PlayGame/currentVotes.json", "r") as f:
        votes = json.load(f)
    # Remove the voter from all other votes in the same level
    for user, votesForUser in votes[level].items():
        if voterName in votesForUser:
            votesForUser.remove(voterName)
    if userToVoteFor not in votes[level]:
        votes[level][userToVoteFor] = [voterName]
    else:
        votes[level][userToVoteFor].append(voterName)
    with open("./PlayGame/currentVotes.json", "w") as f:
        json.dump(votes, f, indent=4)
    
    # Update the CurrentVotes.md
    with open("./PlayGame/VotePage/CurrentVotes.md", "w") as f:
        f.write("# Votes\nThe current votes we have for this competition")
        for level in votes:
            f.write(f"\n<details><summary>{level}</summary>\n\n")
            f.write(f"| name | score |\n| --- | --- |\n")
            for user, votesForUser in votes[level].items():
                f.write(f"| {user} | {len(votesForUser)} |\n")
            f.write("\n\n</details>\n\n")

def main():
    print("ISSUE_NUMBER:", ISSUE_NUMBER)
    client = github.Github(GITHUB_TOKEN)
    repo = client.get_repo(GITHUB_REPO)
    issue = repo.get_issue(number=ISSUE_NUMBER)

    title = issue.title
    user = issue.user.login
    print(f"User: {user}")
    print(f"Issue Title: {title}")

    if "DeleteEntry" in title:
        deleteEntry(issue)
    elif "Game" in title:
        playGame(issue)
    elif "Vote" in title:
        voteForImage(user, title.split(" ")[2], title.split(" ")[3])

    issue.edit(state="closed")

if __name__ == "__main__":
    print("RUNNING SCRIPT")
    main()
