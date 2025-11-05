import os
import sys
from cryptography.fernet import Fernet

# Load encryption key from env secret
FERNET_KEY = os.environ.get("FERNET_KEY")
if not FERNET_KEY:
    print("❌ FERNET_KEY is not defined. Add it to GitHub Secrets.")
    sys.exit(1)

# Load and decrypt script
with open("encrypted_main.py", "rb") as enc_file:
    encrypted_code = enc_file.read()

fernet = Fernet(FERNET_KEY.encode())
try:
    decrypted_code = fernet.decrypt(encrypted_code)
    exec(decrypted_code, globals())
except Exception as e:
    print(f"❌ Error during decryption/execution: {e}")
    sys.exit(1)
