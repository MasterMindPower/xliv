import os
import sys
import subprocess
from cryptography.fernet import Fernet
from datetime import datetime
import shutil

# Load encryption key from GitHub Secrets
FERNET_KEY = os.environ["FERNET_KEY"]
PRIVATE_REPO_URL = os.environ["PRIVATE_REPO_URL"]

# Step 1: Decrypt the encrypted script
with open("encrypted_main.py", "rb") as file:
    encrypted_code = file.read()

cipher = Fernet(FERNET_KEY.encode())
try:
    decrypted_code = cipher.decrypt(encrypted_code)
except Exception as e:
    print(f"❌ Decryption error: {e}")
    sys.exit(1)

# Step 2: Execute the script (generates output.m3u)
exec(decrypted_code.decode())

# Step 3: Push output.m3u to private repo
REPO_DIR = "private_repo"

print(f"📥 Cloning private repo: {PRIVATE_REPO_URL}")
subprocess.run(["git", "clone", PRIVATE_REPO_URL, REPO_DIR], check=True)

dest_file = os.path.join(REPO_DIR, "output.m3u")
shutil.copy("output.m3u", dest_file)

print("📤 Pushing updated file to private repo...")
os.chdir(REPO_DIR)
subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
subprocess.run(["git", "add", "output.m3u"], check=True)
subprocess.run(["git", "commit", "-m", f"Update output.m3u at {datetime.utcnow().isoformat()}"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
