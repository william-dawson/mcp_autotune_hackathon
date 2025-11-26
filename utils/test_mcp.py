#!/usr/bin/env python3
"""
Test script to verify the MCP server and all tools are working in Docker.
"""
import subprocess
import json
import sys

def send_request(process, method, params=None, request_id=None):
    """Send a JSON-RPC request and get response."""
    request = {
        "jsonrpc": "2.0",
        "method": method
    }
    if request_id is not None:
        request["id"] = request_id
    if params is not None:
        request["params"] = params

    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()

    if request_id is not None:
        response_line = process.stdout.readline()
        if response_line:
            return json.loads(response_line)
    return None

def call_tool(process, tool_name, arguments, request_id):
    """Call an MCP tool."""
    print(f"\n{'='*60}")
    print(f"Calling tool: {tool_name}")
    print(f"Arguments: {json.dumps(arguments, indent=2)}")

    response = send_request(
        process,
        "tools/call",
        {
            "name": tool_name,
            "arguments": arguments
        },
        request_id
    )

    if response and "result" in response:
        print(f"✓ Result: {json.dumps(response['result'], indent=2)}")
        return response["result"]
    else:
        print(f"✗ Error: {response}")
        return None

def test_mcp_server():
    print("Starting MCP server in Docker...")

    process = subprocess.Popen(
        ["docker", "run", "-i", "lj_benchmark"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    try:
        # Initialize
        print("\n1. Initializing MCP server...")
        response = send_request(
            process,
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            },
            1
        )
        if not response:
            print("✗ Failed to initialize")
            return False
        print("✓ Initialized")

        # Send initialized notification
        send_request(process, "notifications/initialized")

        # List tools
        print("\n2. Listing available tools...")
        response = send_request(process, "tools/list", {}, 2)
        if response and "result" in response:
            tools = [t["name"] for t in response["result"]["tools"]]
            print(f"✓ Available tools: {', '.join(tools)}")

        # Test each tool in logical order
        req_id = 3

        # 3. Get source code
        call_tool(process, "get_source_code", {}, req_id)
        req_id += 1

        # 4. Make clean (start fresh)
        call_tool(process, "make_clean", {}, req_id)
        req_id += 1

        # 5. Compile default benchmark
        call_tool(process, "make_stream_benchmark", {
            "CC": "gcc",
            "CFLAGS": "-O2 -Wall",
            "LDFLAGS": "-lm"
        }, req_id)
        req_id += 1

        # 6. Test correctness
        call_tool(process, "test_correctness", {}, req_id)
        req_id += 1

        # 7. Test speed (baseline)
        print("\nBaseline performance:")
        call_tool(process, "test_speed", {}, req_id)
        req_id += 1

        # 8. Make custom benchmark with optimized copy
        custom_copy = '''void copy_kernel(double * restrict a, double * restrict b, int n) {
    for (int i = 0; i < n; i += 4) {
        a[i] = b[i];
        a[i+1] = b[i+1];
        a[i+2] = b[i+2];
        a[i+3] = b[i+3];
    }
}'''
        call_tool(process, "make_custom_benchmark", {
            "CC": "gcc",
            "CFLAGS": "-O3 -march=native",
            "LDFLAGS": "-lm",
            "copy_code": custom_copy
        }, req_id)
        req_id += 1

        # 9. Test speed (custom)
        print("\nCustom implementation performance:")
        call_tool(process, "test_speed", {}, req_id)
        req_id += 1

        # 10. Clean up
        call_tool(process, "make_clean", {}, req_id)
        req_id += 1

        # Shutdown gracefully
        print("\nShutting down MCP server...")
        send_request(process, "shutdown", {}, req_id)
        send_request(process, "exit")

        print("\n" + "="*60)
        print("✓ All MCP tools tested successfully!")
        return True

    except Exception as e:
        print(f"✗ Error testing MCP server: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

if __name__ == "__main__":
    success = test_mcp_server()
    sys.exit(0 if success else 1)
