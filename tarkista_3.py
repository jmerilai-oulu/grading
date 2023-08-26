import sys, subprocess, os

from git import Repo
from git import rmtree

def clone_repository(repository_url, destination):
    try:
        Repo.clone_from(repository_url, destination)
        print("Repository cloned successfully. \n")
    except Exception as e:
        print("Error occurred while cloning the repository:", str(e))
        sys.exit(1)  

def cargo_check(directory):
    result = subprocess.run(["cargo", "check"], cwd=directory, capture_output=True, text=True)
    if result.stderr.find("warning") == -1 and result.stderr.find("error") == -1:
        print("O - No warnings or errors found.")
    else:
        print("X - Warnings or errors found.")

def check_pipeline(directory):
    filepath = os.path.join(directory, ".github/workflows/lint_check.yml")
    with open(filepath, 'r') as file:
        contents = file.read()
        if "run:" in contents and "cargo check" in contents:
            print("O - Found \"run\" and \"cargo check\" in lint_check.yml.")
        else:
            print("X - \"run\" or \"cargo check\" not found in lint_check.yml.")

def remove_repository(directory):
    try:
        rmtree(directory)
        print(f"\nRepository deleted successfully.")
    except Exception as e:
        print(f"\nAn error occurred while deleting the repository: {e}")

if __name__ == "__main__":
    destination = "./repos/lab3/"
    clone_repository("https://github.com/jmerilai-oulu/lab3-lint-done", destination)
    cargo_check(destination)
    check_pipeline(destination)
    remove_repository(destination)
