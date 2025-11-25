from mcp.server.fastmcp import FastMCP
import async_api

# Initialize the MCP server for the autotune hackathon
mcp = FastMCP("autotune_hackathon")

@mcp.tool()
async def make_stream_benchmark(CC: str, CFLAGS: str, LDFLAGS: str):
    """
    Compile the STREAM memory bandwidth benchmark.

    Args:
        CC (str): C compiler (e.g., "gcc", "clang")
        CFLAGS (str): Compiler flags (e.g., "-O3 -march=native")
        LDFLAGS (str): Linker flags (e.g., "-lm")

    Returns:
        bool: True if compilation succeeds, False otherwise
    """
    success = await async_api.make_stream_benchmark(CC, CFLAGS, LDFLAGS)
    return success

@mcp.tool()
async def test_correctness():
    """
    Verify benchmark correctness against reference implementation.

    Returns:
        str: JSON with correctness result {"correctness": "PASS"} or {"correctness": "FAIL"}
    """
    success = await async_api.test_correctness()
    return success

@mcp.tool()
async def make_clean():
    """
    Clean up compiled artifacts and temporary files.
    
    This removes the compiled benchmark executable and any object files
    created during compilation, allowing for a fresh build.
    
    Returns:
        str: Success message indicating cleanup completion
    
    Example use case:
        Call this before trying a new set of compiler flags to ensure
        a clean compilation environment
    """
    success = await async_api.make_clean()
    return success

@mcp.tool()
async def test_speed():
    """
    Measure memory bandwidth.

    Returns:
        str: JSON with bandwidth in GB/s for each kernel: {"copy_GB_s": ..., "scale_GB_s": ..., "add_GB_s": ..., "triad_GB_s": ...}
    """
    result = await async_api.test_speed()
    return result

if __name__ == "__main__":
    mcp.run(transport="stdio")