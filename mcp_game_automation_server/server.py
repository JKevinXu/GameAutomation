#!/usr/bin/env python3
"""
MCP Server for 师门任务 (Shimen Task) Automation

This server exposes the existing game automation as an MCP tool that can be
controlled by AI assistants like Claude Desktop.
"""

import subprocess
import time
import os
import sys
from pathlib import Path
from typing import Dict, Any

from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("Shimen Task Automation")

# Get the project root directory (parent of mcp_game_automation_server)
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
SCRIPT_PATH = PROJECT_ROOT / "run_shimen_task.sh"


@mcp.tool()
def run_shimen_task(verbose: bool = False) -> Dict[str, Any]:
    """
    Execute the 师门任务 (Shimen Task) automation sequence.
    
    This tool runs the complete game automation workflow including:
    - Opening MuMu emulator
    - Starting the game
    - Logging in
    - Executing the 师门任务 sequence
    
    Args:
        verbose: If True, include detailed output in the response
    
    Returns:
        Dictionary containing:
        - success: Boolean indicating if automation completed successfully
        - output: Complete output from the automation script
        - execution_time_seconds: Time taken to execute
        - error_message: Error details if execution failed
    """
    start_time = time.time()
    
    try:
        # Check if the script exists
        if not SCRIPT_PATH.exists():
            return {
                "success": False,
                "output": "",
                "execution_time_seconds": 0,
                "error_message": f"Script not found: {SCRIPT_PATH}"
            }
        
        # Make sure script is executable
        os.chmod(SCRIPT_PATH, 0o755)
        
        # Change to project directory before running script
        original_cwd = os.getcwd()
        os.chdir(PROJECT_ROOT)
        
        try:
            # Run the automation script
            result = subprocess.run(
                [str(SCRIPT_PATH)],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd=PROJECT_ROOT
            )
            
            execution_time = time.time() - start_time
            
            # Determine success based on exit code
            success = result.returncode == 0
            
            # Combine stdout and stderr for complete output
            output = ""
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}\n"
            if result.stderr:
                output += f"STDERR:\n{result.stderr}\n"
            
            if not output.strip():
                output = "No output captured from script"
            
            # Create response
            response = {
                "success": success,
                "output": output if verbose else (output[:500] + "..." if len(output) > 500 else output),
                "execution_time_seconds": round(execution_time, 2),
                "error_message": None if success else f"Script exited with code {result.returncode}"
            }
            
            return response
            
        finally:
            # Restore original working directory
            os.chdir(original_cwd)
    
    except subprocess.TimeoutExpired:
        execution_time = time.time() - start_time
        return {
            "success": False,
            "output": "Script execution timed out after 5 minutes",
            "execution_time_seconds": round(execution_time, 2),
            "error_message": "Timeout: Script took longer than 5 minutes to complete"
        }
    
    except Exception as e:
        execution_time = time.time() - start_time
        return {
            "success": False,
            "output": "",
            "execution_time_seconds": round(execution_time, 2),
            "error_message": f"Unexpected error: {str(e)}"
        }


def main():
    """Run the MCP server"""
    try:
        # Verify project structure
        if not PROJECT_ROOT.exists():
            print(f"Error: Project root not found at {PROJECT_ROOT}")
            sys.exit(1)
        
        if not SCRIPT_PATH.exists():
            print(f"Error: Automation script not found at {SCRIPT_PATH}")
            print("Make sure you're running this from the correct directory")
            sys.exit(1)
        
        print(f"Starting MCP server for 师门任务 automation...")
        print(f"Project root: {PROJECT_ROOT}")
        print(f"Script path: {SCRIPT_PATH}")
        print("Server ready to accept MCP connections via stdio transport")
        
        # Run the FastMCP server
        mcp.run()
        
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 