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


async def get_source_code():
    try:
        with open("benchmark/stream_benchmark.c", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Error: Source file not found."


async def make_custom_benchmark(CC: str, CFLAGS: str, LDFLAGS: str,
                                allocation_code: str = None,
                                copy_code: str = None,
                                scale_code: str = None,
                                add_code: str = None,
                                triad_code: str = None):
    try:
        with open("benchmark/stream_benchmark.c", "r") as f:
            source = f.read()

        if allocation_code:
            start = source.find("// ALLOCATION_START")
            end = source.find("// ALLOCATION_END")
            if start != -1 and end != -1:
                source = source[:start] + "// ALLOCATION_START\n" + allocation_code + "\n// ALLOCATION_END" + source[end+len("// ALLOCATION_END"):]

        if copy_code:
            start = source.find("// COPY_START")
            end = source.find("// COPY_END")
            if start != -1 and end != -1:
                source = source[:start] + "// COPY_START\n" + copy_code + "\n// COPY_END" + source[end+len("// COPY_END"):]

        if scale_code:
            start = source.find("// SCALE_START")
            end = source.find("// SCALE_END")
            if start != -1 and end != -1:
                source = source[:start] + "// SCALE_START\n" + scale_code + "\n// SCALE_END" + source[end+len("// SCALE_END"):]

        if add_code:
            start = source.find("// ADD_START")
            end = source.find("// ADD_END")
            if start != -1 and end != -1:
                source = source[:start] + "// ADD_START\n" + add_code + "\n// ADD_END" + source[end+len("// ADD_END"):]

        if triad_code:
            start = source.find("// TRIAD_START")
            end = source.find("// TRIAD_END")
            if start != -1 and end != -1:
                source = source[:start] + "// TRIAD_START\n" + triad_code + "\n// TRIAD_END" + source[end+len("// TRIAD_END"):]

        with open("benchmark/stream_benchmark_custom.c", "w") as f:
            f.write(source)

        subprocess.run(
            [f"{CC}", *CFLAGS.split(), "-o", "stream_benchmark", "stream_benchmark_custom.c", *LDFLAGS.split()],
            check=True,
            capture_output=True,
            text=True,
            cwd="benchmark"
        )
        return True
    except subprocess.CalledProcessError as e:
        error_msg = f"Compilation failed:\n{e.stderr}"
        print(error_msg, file=sys.stderr)
        return error_msg
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return str(e)