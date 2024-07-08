# devops/common/src/healthcheck.py
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.abspath(os.path.join(BASE_DIR, '..', 'version.txt'))

def get_version(app_name):
    version_file = VERSION_FILE
    try:
        with open(version_file, 'r') as file:
            version = file.read().strip()
    except FileNotFoundError:
        version = 'version file not found'
    return version


def get_git_branch():
    try:
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)