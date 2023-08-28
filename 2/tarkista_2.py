import os, argparse, sys, re
from git import Repo
from git import rmtree

def clone_repository(repository_url, destination):
    """Clone the student's repository"""
    try:
        Repo.clone_from(repository_url, destination)
        print("Repository cloned successfully. \n")
    except Exception as e:
        print("Error occurred while cloning the repository:", str(e))
        sys.exit(1)

def check_for_keywords_in_yml():
    """Check if the student has added the required keywords to the .yml file"""
    keywords = ['push',
                'runs-on',
                'ubuntu-latest',
                'actions/checkout',
                'cargo run',
                '.github/workflows/scripts/output_check.sh']
    keyword_patterns = [r'{}'.format(name) for name in keywords]

    with open('./repo/lab2/.github/workflows/CICD_pipeline.yml', 'r') as file:
        content = file.read()
    
    found_keywords = []
    
    for keyword in keyword_patterns:
        matches = re.findall(keyword, content)
        found_keywords.extend(matches)

    # Remove duplicates from the list of found keywords
    found_keywords = list(set(found_keywords))

    if len(found_keywords) == len(keywords):
        print("O - All expected keywords found in CICD.")
    else:
        missing_keywords = list(set(keyword_patterns) - set(found_keywords))
        print("X - Missing keywords in CICD:", missing_keywords)

def remove_repository(directory):
    """Remove the student's repository"""
    try:
        rmtree(directory)
        print(f"\nRepository deleted successfully.")
    except Exception as e:
        print(f"\nAn error occurred while deleting the repository: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check the student's repository for the required changes.")
    parser.add_argument('link', type=str, help='Repository link')
    args = parser.parse_args()

    destination = "./repo/lab2/"

    clone_repository(args.link, destination)
    check_for_keywords_in_yml()
    remove_repository(destination)
