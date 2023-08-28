import sys, subprocess, re, argparse, os

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

    if float(cov) >= 90:
        print("O - Test coverage is " + str(cov) + "%")
    else:
        print("X - Test coverage is " + str(cov) + "%")

def check_for_keywords_in_yml():
    """Check if the student has added the required keywords to the .yml file"""
    keywords = ['push',
                'runs-on',
                'ubuntu-latest',
                'actions/checkout',
                'install cargo-tarpaulin',
                '.github/workflows/scripts/check_coverage.sh']
    
    keyword_patterns = [r'{}'.format(name) for name in keywords]

    with open('./repo/lab4/.github/workflows/ut_check.yml', 'r') as file:
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

def check_if_coverage_report_exists(filename):
    """Check if the student has created a coverage report"""
    if os.path.exists(filename):
        print("O - HTML coverage report was found.")
    else:
        print("X - HTML coverage report not found.")

def remove_repository(directory):
    try:
        rmtree(directory)
        print(f"\nRepository deleted successfully.")
    except Exception as e:
        print(f"\nAn error occurred while deleting the repository: {e}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check the student's repository for the required changes.")
    parser.add_argument('link', type=str, help='Repository link')
    args = parser.parse_args()

    destination = "./repo/lab4/"

    clone_repository(args.link, destination)
    check_coverage_percentage(destination)
    check_for_keywords_in_yml()
    check_if_coverage_report_exists(destination + "tarpaulin-report.html")
    remove_repository(destination)
