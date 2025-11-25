import subprocess
import time
import os
import sys

def main():
    executable_name = "./lj_benchmark"
    
    # 1. Run Make to build the project
    # We suppress stdout/stderr to keep the final output clean
    try:
        subprocess.run(
            ["make"], 
            check=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print("Error: 'make' command failed.", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'make' not found. Ensure you are in the repository directory.", file=sys.stderr)
        sys.exit(1)

    # 2. Verify the executable exists
    if not os.path.exists(executable_name):
        print(f"Error: Executable '{executable_name}' not found after build.", file=sys.stderr)
        sys.exit(1)

    # 3. Run the executable and measure time
    # We use perf_counter for higher precision benchmarking
    start_time = time.perf_counter()
    
    try:
        subprocess.run(
            [executable_name], 
            check=True,
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print(f"Error: '{executable_name}' failed to run.", file=sys.stderr)
        sys.exit(1)
        
    end_time = time.perf_counter()

    # 4. Print only the runtime in seconds
    duration = end_time - start_time
    print(f"{duration:.6f}")

if __name__ == "__main__":
    main()
