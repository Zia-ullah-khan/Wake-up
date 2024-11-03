import subprocess

def run_cpp_executable():
    try:
        # Run the compiled C++ executable
        result = subprocess.run([r'C:\Users\khans\source\repos\Project1\x64\Debug\Project1.exe'], capture_output=True, text=True, check=True)

        # Print the output from the executable
        print("Output:")
        print(result.stdout)
        print("Errors:")
        print(result.stderr)
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the C++ executable: {e}")
        print("Error Output:")
        print(e.stderr)

if __name__ == "__main__":
    run_cpp_executable()
