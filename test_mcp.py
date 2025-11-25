#!/usr/bin/env python3
"""
Simple test script to verify the MCP server is working in Docker.
"""
import subprocess
import json
import sys

def test_mcp_server():
    print("Starting MCP server in Docker...")

    # Start the Docker container with interactive stdin/stdout
    process = subprocess.Popen(
        ["docker", "run", "-i", "lj_benchmark"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    try:
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }

        print("Sending initialize request...")
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()

        # Read response
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line)
            print(f"✓ Server responded: {json.dumps(response, indent=2)}")

            # Send initialized notification
            initialized = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            process.stdin.write(json.dumps(initialized) + "\n")
            process.stdin.flush()

            # List tools
            list_tools = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
            print("\nListing available tools...")
            process.stdin.write(json.dumps(list_tools) + "\n")
            process.stdin.flush()

            tools_response = process.stdout.readline()
            if tools_response:
                tools = json.loads(tools_response)
                print(f"✓ Available tools: {json.dumps(tools, indent=2)}")
                print("\n✓ MCP server is working correctly!")
                return True
        else:
            print("✗ No response from server")
            stderr = process.stderr.read()
            if stderr:
                print(f"Error output: {stderr}")
            return False

    except Exception as e:
        print(f"✗ Error testing MCP server: {e}")
        return False
    finally:
        process.terminate()
        process.wait(timeout=5)

if __name__ == "__main__":
    success = test_mcp_server()
    sys.exit(0 if success else 1)
