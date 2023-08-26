import sys, subprocess

from git import Repo
from git import rmtree

def clone_repository(repository_url, destination):
    try:
        # Clone the repository
        Repo.clone_from(repository_url, destination)
        print("Repository cloned successfully. \n")
    except Exception as e:
        print("Error occurred while cloning the repository:", str(e))
        sys.exit(1)  

def check_coverage_percentage(directory):
    result = subprocess.run(['cargo', 'tarpaulin'], cwd=directory, capture_output=True, text=True)

    # Read the last output line with coverage percentage
    lines = result.stdout.strip().split('\n')
    cov = lines[-1].split("%")[0]

    print("Test Coverage: " + str(cov) + "%")

def remove_git_directory(directory):
    try:
        rmtree(directory)
        print(f"\nRepository deleted successfully.")
    except Exception as e:
        print(f"\nAn error occurred while deleting the repository: {e}")

if __name__ == "__main__":
    destination = "./repos/lab4-ut/"
    clone_repository("https://github.com/jmerilai-oulu/lab4-ut", destination)
    check_coverage_percentage(destination)
    remove_git_directory(destination)

    
