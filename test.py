import subprocess
import sys


def generate_requirements_txt():
    try:
        # Run pip freeze command to get installed packages and their versions
        pip_freeze_output = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode()

        # Write the packages and their versions to requirements.txt file
        with open('requirements.txt', 'w') as f:
            f.write(pip_freeze_output)
        print("requirements.txt file created successfully.")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    generate_requirements_txt()
