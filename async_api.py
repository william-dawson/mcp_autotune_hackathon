import subprocess
import time
import os
import sys

async def make_stream_benchmark(CC: str, CFLAGS: str, LDFLAGS: str):
    try:
        subprocess.run(
            ["make", "stream_benchmark", f"CC={CC}", f"CFLAGS={CFLAGS}", f"LDFLAGS={LDFLAGS}"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd="benchmark"
        )
    except subprocess.CalledProcessError:
        print("Error: 'make' command failed.", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: 'make' not found.", file=sys.stderr)
        return False

    return True
    

async def test_correctness():
    executable_name = "benchmark/stream_benchmark"
    if not os.path.exists(executable_name):
        print(f"Error: Executable '{executable_name}' not found after build.", file=sys.stderr)
        return "Failure: Executable not found."

    try:
        result = subprocess.run(
            ["make", "test-correctness"],
            check=True,
            capture_output=True,
            text=True,
            cwd="benchmark"
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_msg = f"Correctness test failed:\n{e.stdout}\n{e.stderr}"
        print(error_msg, file=sys.stderr)
        return error_msg
    except FileNotFoundError:
        print("Error: 'make' not found.", file=sys.stderr)
        return "Failure: 'make' command not found."


async def make_clean():
    try:
        subprocess.run(
            ["make", "clean"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd="benchmark"
        )
    except subprocess.CalledProcessError:
        print("Error: 'make' command failed.", file=sys.stderr)
        return False

    return True


async def test_speed():
    executable_name = "benchmark/stream_benchmark"
    if not os.path.exists(executable_name):
        print(f"Error: Executable '{executable_name}' not found after build.", file=sys.stderr)
        return "Failure: Executable not found."

    try:
        result = subprocess.run(
            ["make", "test-speed"],
            check=True,
            capture_output=True,
            text=True,
            cwd="benchmark"
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_msg = f"Speed test failed:\n{e.stdout}\n{e.stderr}"
        print(error_msg, file=sys.stderr)
        return error_msg
    except FileNotFoundError:
        print("Error: 'make' not found.", file=sys.stderr)
        return "Failure: 'make' command not found."