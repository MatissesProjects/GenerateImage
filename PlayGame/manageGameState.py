import github
import os
import json
import re

ISSUE_NUMBER = int(os.getenv("ISSUE_NUMBER"))
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def parseCheckBoxData(text):
    choose_multiple_matches = re.findall(r'- \[X\] (.+)', text)
    return choose_multiple_matches

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
        removeThese = parseCheckBoxData(issue.body)
        print(f"Entries to Remove: {removeThese}")

        try:
            with open("./PlayGame/currentEntries.json", "r") as f:
                jsonData = json.load(f)
        except FileNotFoundError:
            print("Error: JSON file not found.")
            return
        except json.JSONDecodeError:
            print("Error: JSON file is not valid.")
            return

        for level in removeThese:
            if level in jsonData:
                original_length = len(jsonData[level])
                jsonData[level] = [entry for entry in jsonData[level] if user not in entry[0]]
                removed_count = original_length - len(jsonData[level])
                print(f"Removed {removed_count} entries from {level}.")
            else:
                print(f"Level '{level}' not found in JSON data.")

        try:
            with open("./PlayGame/currentEntries.json", "w") as f:
                json.dump(jsonData, f, indent=4)
            print("Updated JSON file successfully.")
        except Exception as e:
            print(f"Error writing to JSON file: {e}")
            return

    issue.edit(state="closed")

if __name__ == "__main__":
    print("RUNNING SCRIPT")
    main()
