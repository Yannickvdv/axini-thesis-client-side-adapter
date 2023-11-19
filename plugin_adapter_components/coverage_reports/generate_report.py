import subprocess

coverage_command = "istanbul report --include ./1/** text"
coverage_command = "istanbul report --dir coverage --include ./1/** lcov"


subprocess.run(coverage_command, shell=True, check=True)
