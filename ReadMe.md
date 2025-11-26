# MCP Hackathon Tuner
For the MCP hackathon, we pick a simple example having an LLM optimize some
code for the stream benchmark. The code is written in C, with an associated makefile
in the folder `benchmark`. We can start with things like having the compiler
tweak the flags for gcc. Then we can ask it to consider some actual hand
written optimizations.

## Building
You can build the docker container:
Build the Docker image:
```bash
docker build -t lj_benchmark .
```
Then verify everything is good by typing
```
python utils/test_mcp.py
```

## Connecting to MCP Clients
If that works, you can modify `~/.gemini/settings.json`. Make sure to use
absolute paths. Add in the `mcpServers` section.
```
    "lj": {
      "name": "lj",
      "type": "stdio",
      "command": "docker",
      "args": [
        "run", "-i", "--rm", "lj_benchmark"
      ]
    }
```
For claude code, you can put the following into a `.mcp.json` file of the
current directory.
```
{
  "mcpServers": {
    "lj_benchmark": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "lj_benchmark"]
    }
  }
}
```

## Running Over HTTP (Remote Server)
The MCP server supports both local (stdio) and remote (HTTP) transports.

Using Docker:
```bash
docker run -p 8000:8000 lj_benchmark python3 server.py --transport http --host 0.0.0.0 --port 8000
```

Using Singularity/Apptainer:
```bash
# Download and extract the sandbox artifact from GitHub Actions
tar xzf stream_benchmark_amd64_sandbox.tar.gz

# Run the server
apptainer exec --pwd /app stream_benchmark_amd64_sandbox python3 server.py --transport http --host 0.0.0.0 --port 8000
```

Or build locally from Docker:
```bash
apptainer build --sandbox stream_benchmark_sandbox docker-daemon://lj_benchmark:latest
apptainer exec --pwd /app stream_benchmark_sandbox python3 server.py --transport http --host 0.0.0.0 --port 8000
```

For ARM systems, use `stream_benchmark_arm64_sandbox.tar.gz` instead.

**Note**: Compilation happens in `/tmp/benchmark_work` which is writable in both Docker and Singularity, so no special flags are needed.
