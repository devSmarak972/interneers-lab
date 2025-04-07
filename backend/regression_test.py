import subprocess
import sys

def run_pytest():
    print("Running regression tests using pytest...\n")
    result = subprocess.run(["pytest", "-v"], capture_output=True, text=True)

    print(result.stdout)  # Print test output to console

    if result.returncode != 0:
        print("Regression tests failed!")
        print(result.stderr)
        sys.exit(result.returncode)
    else:
        print("All regression tests passed successfully!")

if __name__ == "__main__":
    run_pytest()
