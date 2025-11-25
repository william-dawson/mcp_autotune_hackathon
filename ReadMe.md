# MCP Hackathon Tuner

For the MCP hackathon, we pick a simple example having an LLM optimize some
code for computing Lennard-Jones interactions. The code is written in C,
with an associated makefile. We can start with things like having the compiler
tweak the flags for gcc. Then we can ask it to consider some actual hand
written optimizations.

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
python3 test_mcp.py
```

This will:
1. Start the Docker container with the MCP server
2. Send initialization and tool listing requests
3. Verify the server responds correctly
4. Display available tools
