import github
import os
import requests
import random

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

def close_with_error(issue, msg):
    issue.create_comment(f"ERROR: {msg}")
    issue.edit(state="closed", labels=["Invalid"])

def render_readme(imageLocation):
    lines = [
                "# GenerateImage",
                "A test to see if we can generate images using git issues.",
                "## Current Generated Image",
                f"[<img src='{imageLocation}'>]({imageLocation})",
                "The images takes around 30s to generate, please be patient.",
            ]
    return "\n".join(lines)

def main():
    client = github.Github(GITHUB_TOKEN)
    repo = client.get_repo(GITHUB_REPO)
    issue = repo.get_issue(number=ISSUE_NUMBER)
    matisseId = "630649313860780043" # matisse's discord id, not sensitive info
    targetLocalImage = "https://static-cdn.jtvnw.net/jtv_user_pictures/db94532a-3367-4819-a2e2-03f2cbeefdc1-profile_image-300x300.png"

    title = issue.title
    allowedStart = "Transform:"
    if allowedStart not in title:
        close_with_error(issue, "Invalid input format, include Transform:")
        return

    if len(title) == len(allowedStart):
        close_with_error(issue, "Input must contain a string to transform")
        return

    textToRiffWith = title[len(allowedStart):]
    data1 = {"discordId":matisseId,"discordUsername":"matisse","targetPicture":targetLocalImage,"prompt":textToRiffWith,"id":random.randint(1000,9999), "accessToken": DISCORD_TOKEN}
    response1 = requests.post('https://deepnarrationapi.matissetec.dev/startSimilarImages', headers=headers, json=data1)
    imageLocation = response1.text

    if len(imageLocation) > 300:
        close_with_error(issue, "Error generating image, the response was wrong")
        return

    readme = render_readme(imageLocation)
    # issue.create_comment(readme)
    with open("README.md", "w+") as f:
        f.write(readme)

    issue.create_comment(f"Your photo is here! {imageLocation}")
    issue.edit(state="closed")

if __name__ == "__main__":
    print("RUNNING SCRIPT")
    main()