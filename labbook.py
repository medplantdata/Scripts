import time 
import subprocess


notePath = "/home/school/masters/Notes/Labbook/Scripts.md"

with open(notePath, 'r') as md:
    latest = md.readline().strip()
    old_commits = md.read().strip()

if not latest:
    print("No previous commits found. Exiting.")
    exit()

today = time.strftime("%Y-%m-%d")

fmt = "%an – %ai%n%s%n---"


result = subprocess.run(
    ["git", "log", f"--after={latest}", f"--pretty=format:{fmt}"],
    cwd="/home/school/masters/Scripts",
    capture_output=True,
    text=True,
)

output = result.stdout.strip()
if output:
    with open(notePath, 'w') as md:
        md.write(today + "\n" + output + "\n" + old_commits)