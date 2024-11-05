import subprocess

# Define the azd command
command = ['azd', 'env', 'get-value', 'AZURE_ENV_NAME']

# Run the command
result = subprocess.run(command, capture_output=True, text=True)

# Print the output
if result.returncode == 0:
    print("Command output:", result.stdout)
else:
    print("Error:", result.stderr)


