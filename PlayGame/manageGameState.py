import github
import os
import json
import re

ISSUE_NUMBER = int(os.getenv("ISSUE_NUMBER"))
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def parseCheckBoxData(text):
    choose_multiple_matches = re.findall(r'- \[X\] (.+)', text)
    #f"{', '.join(choose_multiple_matches)}"
    return choose_multiple_matches

def main():
    print("ISSUE_NUMBER: ", ISSUE_NUMBER)
    client = github.Github(GITHUB_TOKEN)
    repo = client.get_repo(GITHUB_REPO)
    issue = repo.get_issue(number=ISSUE_NUMBER)

    title = issue.title
    user = issue.user.login
    print(user)
    print(title)
    # if "Game" in title:
    #     print(parseGameString(issue.body))
    # el
    if "DeleteEntry" in title:
        removeThese = parseCheckBoxData(issue.body)
        print(removeThese)
        with open("./PlayGame/currentEntries.json", "r+") as f:
            jsonData = json.load(f)
            for level in removeThese:
                if user in jsonData[level]:
                    # remove the user from the list if in the list
                    jsonData[level].remove(user)
        print(f"jsonData: {jsonData}")
        with open("./PlayGame/currentEntries.json", "w") as f:
            f.write(json.dumps(jsonData))
    # with open("./PlayGame/currentEntries.json", "r+") as f:
    #     jsonData = json.load(f)
    
    print(jsonData)
    print(user in jsonData)
    issue.edit(state="close")

if __name__ == "__main__":
    print("RUNNING SCRIPT")
    main()
