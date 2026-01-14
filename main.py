import os
from dotenv import load_dotenv
from sandbox.container_mgr import Sandbox
from agent.graph import build_graph

# Load API keys from .env
load_dotenv()

# Define the file we are going to break and fix
BROKEN_FILE = "broken_math.py"

def create_broken_code():
    """Generates a Python file with an intentional bug"""
    code = """
import pytest

def add(a, b):
    # Intentional bug: subtracting instead of adding
    return a - b

def test_add():
    assert add(2, 3) == 5
    assert add(10, 5) == 15
"""
    with open(BROKEN_FILE, 'w') as f:
        f.write(code)
    print(f"🔨 Created broken file: {BROKEN_FILE}")

if __name__ == "__main__":
    # 1. Setup the scenario
    create_broken_code()
    
    # 2. Start the Secure Sandbox
    sandbox = Sandbox()
    
    try:
        sandbox.build_and_start()
        
        # 3. Initialize the AI Agent
        app = build_graph()
        
        initial_state = {
            "code_filename": BROKEN_FILE,
            "error_log": "",
            "current_code": "",
            "iterations": 0,
            "status": "start"
        }
        
        # 4. Run the Loop
        print("🚀 GitFix Agent Starting...")
        app.invoke(initial_state)
        
        print("\n✨ Process Complete. Open broken_math.py to see the fix!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # 5. Cleanup (Stop Docker)
        sandbox.stop()