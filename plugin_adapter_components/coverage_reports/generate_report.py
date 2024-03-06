import subprocess

coverage_command = "istanbul report --dir coverage --include './isolated/**' html"

subprocess.run(coverage_command, shell=True, check=True)
