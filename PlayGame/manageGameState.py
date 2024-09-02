import github
import os
import json

ISSUE_NUMBER = int(os.getenv("ISSUE_NUMBER"))
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def main():
    print("ISSUE_NUMBER: ", ISSUE_NUMBER)
    client = github.Github(GITHUB_TOKEN)
    repo = client.get_repo(GITHUB_REPO)
    issue = repo.get_issue(number=ISSUE_NUMBER)

    title = issue.title
    user = issue.user.login
    print(user)
    print(title)    
    with open("./PlayGame/currentEntries.json", "r+") as f:
        jsonData = json.load(f)
    
    print(jsonData)
    print(user in jsonData)
    issue.edit(state="close")

if __name__ == "__main__":
    print("RUNNING SCRIPT")
    main()
