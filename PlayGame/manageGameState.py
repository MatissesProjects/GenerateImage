import github
import os

ISSUE_NUMBER = int(os.getenv("ISSUE_NUMBER"))
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def main():
    client = github.Github(GITHUB_TOKEN)
    repo = client.get_repo(GITHUB_REPO)
    issue = repo.get_issue(number=ISSUE_NUMBER)

    title = issue.title

    
    with open("./PlayGame/currentEntries.json", "r+") as f:
        jsonData = f.readlines()
    
    print(jsonData)
    issue.edit(state="close")