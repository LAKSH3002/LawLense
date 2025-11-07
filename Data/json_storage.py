# Data extraction from A github repository 
# The following is the script provided
from subprocess import run, PIPE
from sys import platform

# URL of the JSON file (documents and collections)
URL = 'https://raw.githubusercontent.com/Yash-Handa/The_Constitution_Of_India/master/COI.json'

test = None

# For Linux
if platform.startswith('linux'):
    test = run(['wget', URL, '-O', 'COI.json'], stdout=PIPE, stderr=PIPE)

# For Mac
elif platform == 'darwin':  # macOS
    test = run(['curl', URL, '-o', 'COI.json'], stdout=PIPE, stderr=PIPE)

# For Windows
elif platform == 'win32':  # Windows
    ps_command = f'powershell -Command "Invoke-WebRequest {URL} -OutFile COI.json"'
    test = run(ps_command, shell=True, stdout=PIPE, stderr=PIPE)

test.check_returncode()
print("File downloaded successfully as COI.json")
