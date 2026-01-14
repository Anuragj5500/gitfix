import os

class Sandbox:
    def __init__(self):
        self.client = None
        self.container = None
        self.is_active = False
        
        # Try to import and connect to Docker safely (Lazy Import)
        try:
            import docker  # <--- WE IMPORT IT HERE NOW
            self.client = docker.from_env()
            self.client.ping()
            self.is_active = True
        except (ImportError, Exception):
            # If docker lib is missing (Cloud) or Engine is off (Local)
            self.is_active = False

    def build_and_start(self):
        """Starts Docker ONLY if available."""
        if not self.is_active:
            print("⚠️ Docker unavailable. Skipping container start.")
            return

        import docker  # Import here again to be safe
        print("🐳 Building Sandbox Image...")
        
        try:
            self.client.images.build(path="./sandbox", tag="gitfix-sandbox")
            
            current_dir = os.getcwd()
            # Remove old containers
            existing = self.client.containers.list(filters={"ancestor": "gitfix-sandbox"})
            for c in existing:
                c.remove(force=True)

            self.container = self.client.containers.run(
                "gitfix-sandbox",
                detach=True,
                volumes={current_dir: {'bind': '/app', 'mode': 'rw'}},
                working_dir='/app'
            )
        except Exception as e:
            print(f"Error starting Docker: {e}")
            self.is_active = False

    def run_test(self, file_name):
        """Runs real tests if Docker is active."""
        if not self.is_active:
            raise RuntimeError("Docker is not active.")
            
        result = self.container.exec_run(f"pytest {file_name}")
        return result.exit_code == 0, result.output.decode("utf-8")