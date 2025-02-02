import requests

def get_first_commit(username):
    try:
        # Fetch user's repositories
        repos_url = f"https://api.github.com/users/{username}/repos"
        repos_response = requests.get(repos_url)
        repos_response.raise_for_status()  # Raise an error for unsuccessful requests
        repos = repos_response.json()

        first_commit_date = None
        first_commit_info = None

        # Iterate through each repository
        for repo in repos:
            # Fetch commits for the repository
            commits_url = f"https://api.github.com/repos/{username}/{repo['name']}/commits"
            commits_response = requests.get(commits_url)
            commits_response.raise_for_status()  # Raise an error for unsuccessful requests
            commits = commits_response.json()

            # Sort commits by date
            commits.sort(key=lambda x: x['commit']['author']['date'])

            # Check if the earliest commit is earlier than the current earliest
            if commits:
                first_commit = commits[0]
                commit_date = first_commit['commit']['author']['date']
                if first_commit_date is None or commit_date < first_commit_date:
                    first_commit_date = commit_date
                    first_commit_info = {
                        'repository': repo['name'],
                        'commit_date': commit_date,
                        'commit_message': first_commit['commit']['message']
                    }

        return first_commit_info
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
username = input("Enter a name: \n")
first_commit = get_first_commit(username)
if first_commit:
    print(f"First commit for {username}:")
    print(f"Repository: {first_commit['repository']}")
    print(f"Date: {first_commit['commit_date']}")
    print(f"Message: {first_commit['commit_message']}")
else:
    print("No commits found.")
