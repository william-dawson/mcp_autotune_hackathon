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
    
    Executes 'make test-correctness' which runs the benchmark with seed 42
    and validates that the output matches expected values for:
    - Total Lennard-Jones energy: 304963.782767
    - Number of particles: 30000
    - Number of interactions: 449985000
    - Particle generation attempts: 30253
    
    Returns:
        str: Test output including "✓ Correctness test PASSED" on success,
             or error message with details on failure
    
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

@mcp.tool()
async def test_speed():
    """
    Run the compiled benchmark to measure execution speed.
    
    Executes 'make test-speed' which runs the benchmark without a fixed seed
    to measure the runtime performance of the current compilation.
    
    Returns:
        str: Test output including timing information and benchmark results,
             or error message if the benchmark hasn't been compiled yet
    
    Note:
        Must call make_lj_benchmark() before running this test
    """
    result = await async_api.test_speed()
    return result

if __name__ == "__main__":
    mcp.run(transport="stdio")