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

def find_prints_in_rust_file(filename):
    """Find if the student has added the two additional functions from dev branches"""

    function_names = ['I am from master branch', 'I am from a dev branch', 'I am also from a dev branch']
    function_patterns = [r'{}'.format(name) for name in function_names]
    
    with open(filename, 'r') as file:
        content = file.read()
    
    found_functions = []
    
    for pattern in function_patterns:
        matches = re.findall(pattern, content)
        found_functions.extend(matches)
    
    if len(found_functions) == len(function_names):
        print("O - All three functions found in the file.")
    else:
        missing_functions = set(function_names) - set(found_functions)
        print("X - Missing:", missing_functions)

def check_gitignore_for_txt(filename):
    """Check if the student has added .txt to .gitignore"""

    txt_file_pattern = r'\.txt'

    with open(filename, 'r') as file:
        gitignore_content = file.read()

    txt_files_ignored = re.search(txt_file_pattern, gitignore_content)

    if txt_files_ignored is not None:
        print("O - \".txt\" found in .gitignore")
    else:
        print("X - \".txt\" not found in .gitignore")

def check_todofile(filename):
    """Check if the student has removed the TODO.txt file"""
    if not os.path.exists(filename):
        print("O - TODO file was removed.")
    else:
        print("X - TODO file was not removed.")

def check_readmefile(filename):
    """Check if the student has added a README.md file"""
    if os.path.exists(filename):
        print("O - Readme.md file exists")
    else:
        print("X - Readme.md file does not exist")

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

    destination = "./repos/lab1/"

    clone_repository(args.link, destination)
    find_prints_in_rust_file(os.path.join(destination, "src/main.rs"))
    check_gitignore_for_txt(os.path.join(destination, ".gitignore"))
    check_todofile(os.path.join(destination, "TODO.txt"))
    check_readmefile(os.path.join(destination, "README.md"))
    remove_repository(destination)
