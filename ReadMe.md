# MCP Hackathon Tuner

For the MCP hackathon, we pick a simple example having an LLM optimize some
code for computing Lennard-Jones interactions. The code is written in C,
with an associated makefile. We can start with things like having the compiler
tweak the flags for gcc. Then we can ask it to consider some actual hand
written optimizations.

## Connecting with Gemini

First setup python so that you have the fastmcp package. You can verify
everything is good by typing
```
python utils/test_mcp.py
```
If that works, you can modify `~/.gemini/settings.json`. Make sure to use
absolute paths. Add in the `mcpServers` section.
```
    "lj": {
      "name": "lj",
      "type": "stdio",
      "command": "/Users/wddawson/.local/share/mamba/envs/test_mcp/bin/python",
      "args": [
        "/Users/wddawson/Desktop/mcp_autotune_hackathon/server.py"
      ]
    }
```

## Running the MCP Server with Docker

Build the Docker image:
```bash
docker build -t lj_benchmark .
```

Run the MCP server:
```bash
docker run -i lj_benchmark
```

The MCP server exposes the following tools:
- `make_lj_benchmark(CC, CFLAGS, LDFLAGS)` - Compile the benchmark with specified compiler and flags
- `test_correctness()` - Verify correctness of the compiled benchmark
- `make_clean()` - Clean up build artifacts

## Testing the MCP Server

To verify the MCP server is working correctly in Docker:

```bash
python3 utils/test_mcp.py
```

This will:
1. Start the Docker container with the MCP server
2. Send initialization and tool listing requests
3. Verify the server responds correctly
4. Display available tools

## Connecting from MCP Clients

The server uses **stdio transport**, so your MCP client needs to launch the Docker container as a subprocess.

### Claude Desktop Configuration

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "lj_benchmark": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "lj_benchmark"]
    }
  }
}
```

### Generic MCP Client

Any MCP client should run:
```bash
docker run -i --rm lj_benchmark
```

And communicate via stdin/stdout using JSON-RPC 2.0 protocol.
