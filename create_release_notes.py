import requests
from github import Github
from github import Auth


def increment_version(version, component):
    major, minor, patch = version.split('.')
    if component == 'major':
        major = str(int(major) + 1)
        minor = '0'
        patch = '0'
    elif component == 'minor':
        minor = str(int(minor) + 1)
        patch = '0'
    elif component == 'patch':
        patch = str(int(patch) + 1)
    else:
        return version
    return f"{major}.{minor}.{patch}"


def get_latest_tag(owner, repo, token):
    tags = get_github_tags(owner, repo, token)
    if tags:
        # Assuming tags are in the format 'vX.Y.Z'
        tags.sort(key=lambda x: tuple(map(int, x[1:].split('.'))))
        latest_tag = tags[-1]
        return latest_tag
    else:
        return None


def get_github_tags(owner, repo, token):
    headers = {'Authorization': f'token {token}'}
    api_url = f"https://api.github.com/repos/{owner}/{repo}/tags"
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        tags = [tag['name'] for tag in response.json()]
        return tags
    else:
        print(f"Failed to retrieve tags: {response.status_code}")
        print("Exiting release note script")
        return []


def version_naming(prompt):
    while True:
        response = input(prompt).strip().lower()
        if "y" in response:
            return "y"
        elif "n" in response:
            return "n"
        else:
            print("Please enter Yes or No.")


def mark_tag_for_release(token, owner, repo_name, tag_name, release_notes):
    # using an access token
    auth = Auth.Token(token)
    # Initialize the GitHub instance with your personal access token
    g = Github(auth=auth)

    # Get the repository
    repo = g.get_repo(f"{owner}/{repo_name}")

    # Get the SHA hash of the latest commit in the 'main' branch
    latest_commit_sha = repo.get_branch("main").commit.sha

    major, minor, patch = tag_name[1:].split('.')
    prerelease = True
    if int(major) >= 1:
        prerelease = False

    # Proceed with your code that uses the 'repo' object
    # Create a release
    release = repo.create_git_release(
        tag_name,
        f"{tag_name}",
        release_notes,
        target_commitish=latest_commit_sha,
        draft=False,  # Change to True if you want to create a draft release
        prerelease=prerelease
    )

    return release


def main():
    # GitHub repository information
    owner = 'ZompLLC'
    repo = 'BossRealms'
    component = ""

    # read file
    token = ""
    file = open('token.txt', 'r')
    for line in file:
        token = line

    major = version_naming("Are we ready to move up a major version?\n")
    minor = ""
    patch = ""
    if major == 'n':
        minor = version_naming("Are there any major changes being added?\n")
        if minor == 'n':
            patch = version_naming("Are there any small changes being added?\n")
            if patch == 'n':
                print("Exiting script")
                return

    features_added = []
    if minor == 'y':
        print("What kits/features were added or removed? ")
        print("Press enter to add a new change. If you press enter on an empty line, you move onto the next step.\n")
        while True:
            feature_added = input()
            if feature_added.strip() == '':
                break
            features_added.append(feature_added)

    print("What balance changes were made? ")
    print("Press enter to add a new change. If you press enter on an empty line, you move onto the next step.\n")
    changes = []
    while True:
        change = input()
        if change.strip() == '':
            break
        changes.append(change)

    print("What bugs were fixed/QOL were made? ")
    print("Press enter to add a new change. If you press enter on an empty line, you move onto the next step.\n")
    bugs = []
    while True:
        bug = input()
        if bug.strip() == '':
            break
        bugs.append(bug)

    print("Any other notes?")
    print("Press enter to add a new change. If you press enter on an empty line, you move onto the next step.\n")
    notes = []
    while True:
        note = input()
        if note.strip() == '':
            break
        notes.append(note)

    if major == "y":
        component = "major"
    elif minor == "y":
        component = "minor"
    elif patch == "y":
        component = "patch"

    tags = get_github_tags(owner, repo, token)

    if tags:
        current_version = get_latest_tag(owner, repo, token)
        new_version = 'v' + increment_version(current_version[1:], component)
        if current_version[1:] != new_version:
            release_body = '# ' + new_version + ' Patch Notes\n' + \
                           '### Kits/Features: \n' + ''.join(f"- {feature}\n" for feature in features_added) + '\n' + \
                           '### Balance Changes: \n' + ''.join(f"- {change}\n" for change in changes) + '\n' + \
                           '### Bug Fixes/Quality of Life changes: \n' + ''.join(f"- {bug}\n" for bug in bugs) + '\n' + \
                           '### Other Notes: \n' + ''.join(f"- {note}\n" for note in notes) + '\n'

            # Replace {tag_name} with the actual tag name
            release_body = release_body.format(tag_name=new_version)
            print(f"Tag '{new_version}' created and pushed successfully.")
            release = mark_tag_for_release(token, owner, repo, new_version, release_body)
            print(f"Release {release} created successfully: {release.html_url}")
            print("Exiting release note script")
        else:
            print("New version is the same as the old version")
            print("Exiting release note script")

    else:
        print("No tags found.")
        print("Exiting release note script")


if __name__ == "__main__":
    main()