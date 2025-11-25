import subprocess
import time
import os
import sys

async def make_lj_benchmark(CC: str, CFLAGS: str, LDFLAGS: str):
    # 1. Run Make to build the project
    # We suppress stdout/stderr to keep the final output clean
    try:
        subprocess.run(
            ["make", "lj_benchmark", f"CC={CC}", f"CFLAGS={CFLAGS}", f"LDFLAGS={LDFLAGS}"], 
            check=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print("Error: 'make' command failed.", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: 'make' not found. Ensure you are in the repository directory.", file=sys.stderr)
        return False
    
    return True
    

async def test_correctness():
    # 2. Verify the executable exists
    executable_name = "./lj_benchmark"
    if not os.path.exists(executable_name):
        print(f"Error: Executable '{executable_name}' not found after build.", file=sys.stderr)
        return False

    return True


async def make_clean():
    try:
        subprocess.run(
            ["make", "clean"], 
            check=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        print("Error: 'make' command failed.", file=sys.stderr)
        return False
    
    return True


async def test_speed():
    pass