from mcp.server.fastmcp import FastMCP
import async_api

# Initialize the MCP server for the autotune hackathon
mcp = FastMCP("autotune_hackathon")

@mcp.tool()
async def make_lj_benchmark(CC: str, CFLAGS: str, LDFLAGS: str):
    """
    Compile the Lennard-Jones benchmark with specified compiler and flags.
    
    Args:
        CC (str): The C compiler to use (e.g., "gcc", "clang", "icc")
        CFLAGS (str): Compiler flags for optimization (e.g., "-O3 -march=native")
        LDFLAGS (str): Linker flags (e.g., "-lm" for math library)
    
    Returns:
        str: Success message if compilation succeeds, error message otherwise
    
    Example:
        make_lj_benchmark("gcc", "-O3 -march=native", "-lm")
    """
    success = await async_api.make_lj_benchmark(CC, CFLAGS, LDFLAGS)
    return success

@mcp.tool()
async def test_correctness():
    """
    Run the compiled benchmark to verify correctness of the implementation.
    
    This function executes the benchmark and checks if the computed results
    match the expected values within acceptable tolerance.
    
    Returns:
        str: Success message if test passes, error message if it fails or 
             if the benchmark hasn't been compiled yet
    
    Note:
        Must call make_lj_benchmark() before running this test
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

# @mcp.tool()
# def test_speed():
#     pass

if __name__ == "__main__":
    mcp.run(transport="stdio")