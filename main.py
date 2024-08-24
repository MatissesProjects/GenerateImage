import github
import os
import requests
import random
import time
import re
from better_profanity import profanity

ISSUE_NUMBER = int(os.getenv("ISSUE_NUMBER"))
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
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
matisseId = "630649313860780043" # matisse's discord id, not sensitive info

def close_with_error(issue, msg):
    issue.create_comment(f"ERROR: {msg}")
    issue.edit(state="closed", labels=["Invalid"])

def render_readme(imageLocation):
    lines = [
                "# GenerateImage",
                "Click the image below to generate a new image.",
                "",
                "## How to use",
                "<ol>",
                "  <li>You can transform the image below or create a new image</li>",
                "  <ol type='A'>",
                "      <li>To transform the image",
                "        <ul>",
                "          <li>Click the image below</li>",
                "          <li>Add your transformation text to the title</li>",
                "          <li>Submit the issue</li>",
                "        </ul>",
                "      </li>",
                "      <li>To create a new image",
                "        <ul>",
                "          <li>Select the link <a href='https://github.com/MatissesProjects/GenerateImage/issues/new?title=CreateImage:%20Create%20New%20Image&template=NewImage.yml'>New image request form</a></li>",
                "          <li>Follow the issue creation steps</li>",
                "          <li>Submit the issue</li>",
                "        </ul>",
                "      </li>",
                "    </ol>",
                "    <li>Wait for the new image to be generated, around 30 seconds</li>",
                "</ol>",
                "",
                "## Current Generated Image",
                f"[<img src='{imageLocation}'>](https://github.com/{GITHUB_REPO}/issues/new?title=Transform:%20&body=No%20need%20to%20modify%20the%20body,%20just%20add%20your%20transformation%20to%20the%20photo%20in%20the%20title)",
                "",
                "## Want faster results?",
                "Try the page these APIs is based on: [Maitisse](https://deepnarration.matissetec.dev/)",
            ]
    return "\n".join(lines)

def transformFunction(issue):
    with open("currentImageURL.txt", "r+") as f:
        targetLocalImage = f.read()

    title = issue.title
    allowedStart = "Transform:"
    if allowedStart not in title:
        close_with_error(issue, "Invalid input format, include Transform:")
        return

    if len(title) == len(allowedStart):
        close_with_error(issue, "Input must contain a string to transform")
        return
    
    profanity.load_censor_words()
    if profanity.contains_profanity(title):
        close_with_error(issue, "Profanity is not allowed")
        return

    textToRiffWith = title[len(allowedStart):]
    data1 = {"discordId":matisseId,"discordUsername":"matisse","targetPicture":targetLocalImage,"prompt":textToRiffWith,"id":random.randint(1000,9999), "accessToken": DISCORD_TOKEN}
    print("starting request to backend")
    response1 = requests.post('https://deepnarrationapi.matissetec.dev/startSimilarImages', headers=headers, json=data1)
    imageLocation = response1.text
    if len(imageLocation) > 300:
        close_with_error(issue, "Error generating image, the response was wrong")
        return
    
    return imageLocation

# validate that items are within the allowed list
def validateItems(items, allowed_items):
    for item in items:
        if item not in allowed_items:
            return False
    return True

def parseImageString(input_string):
    # Extract the item under "Choose one"
    choose_one_match = re.search(r'### Choose one\n+(.+)', input_string)
    choose_one = choose_one_match.group(1).strip() if choose_one_match else None

    # Extract the items under "Choose multiple" that have an [X]
    choose_multiple_matches = re.findall(r'- \[X\] (.+)', input_string)
    # using validateItems filter all the items that are not in the allowed list
    # choose_multiple_matches = [item for item in choose_multiple_matches if validateItems(item.split(", "), ["item1", "item2", "item3"])]
    # Construct the result string
    result = f"{choose_one}, {', '.join(choose_multiple_matches)}"
    return result

def createImageFunction(issue):
    issueBody = issue.body
    print(issueBody)
    newImagePrompt = parseImageString(issueBody)
    print(newImagePrompt)
    data1 = {"discordId":matisseId,"discordUsername":"matisse","prompt":newImagePrompt,"id":random.randint(1000,9999), "accessToken": DISCORD_TOKEN}
    print("starting request to backend")
    response1 = requests.post('https://deepnarrationapi.matissetec.dev/startCreateImage', headers=headers, json=data1)
    imageLocation = response1.text

    if len(imageLocation) > 300:
        close_with_error(issue, "Error generating image, the response was wrong")
        return
    
    print("response from backend", imageLocation)

    return imageLocation

def main():
    client = github.Github(GITHUB_TOKEN)
    repo = client.get_repo(GITHUB_REPO)
    issue = repo.get_issue(number=ISSUE_NUMBER)
    imageLocation = ""
    if "Transform" in issue.title:
        imageLocation = transformFunction(issue)
    elif "CreateImage" in issue.title:
        imageLocation = createImageFunction(issue)
    
    print("response from backend", imageLocation)

    readme = render_readme(imageLocation)
    # issue.create_comment(readme)
    with open("README.md", "w+") as f:
        f.write(readme)

    with open("currentImageURL.txt", "w+") as f:
        f.write(imageLocation)

    time.sleep(5)

    issue.create_comment(f"Your photo is here! \n![new image]({imageLocation}) \n\nif the image doesnt populate refresh in a few seconds")
    issue.edit(state="closed")

if __name__ == "__main__":
    print("RUNNING SCRIPT")
    main()