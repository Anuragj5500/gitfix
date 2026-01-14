import docker
import os

class Sandbox:
    def __init__(self):
        self.client = None
        self.container = None
        self.is_active = False
        
        # Try to connect to Docker
        try:
            self.client = docker.from_env()
            self.client.ping()  # Checks if the engine is actually running
            self.is_active = True
        except Exception:
            self.is_active = False  # Docker is missing or off

    def build_and_start(self):
        """Starts Docker ONLY if available."""
        if not self.is_active:
            print("⚠️ Docker unavailable. Skipping container start.")
            return

        print("🐳 Building Sandbox Image...")
        self.client.images.build(path="./sandbox", tag="gitfix-sandbox")
        
        current_dir = os.getcwd()
        # Remove old containers if they exist
        existing = self.client.containers.list(filters={"ancestor": "gitfix-sandbox"})
        for c in existing:
            c.remove(force=True)

        self.container = self.client.containers.run(
            "gitfix-sandbox",
            detach=True,
            volumes={current_dir: {'bind': '/app', 'mode': 'rw'}},
            working_dir='/app'
        )

    def run_test(self, file_name):
        """Runs real tests if Docker is active."""
        if not self.is_active:
            raise RuntimeError("Docker is not active.")
            
        result = self.container.exec_run(f"pytest {file_name}")
        return result.exit_code == 0, result.output.decode("utf-8")