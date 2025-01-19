import subprocess
argue = "1"
result = subprocess.run(['node', r'sec14.js', argue], shell=True, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
