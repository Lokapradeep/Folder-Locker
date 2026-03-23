import os
import getpass
import hashlib
from cryptography.fernet import Fernet

# =========================
# HASH PASSWORD
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# CREATE FOLDER
# =========================
def create_folder():
    folder = input("Enter folder name: ")

    if not os.path.exists(folder):
        os.mkdir(folder)
        print(f"📁 Folder '{folder}' created successfully!")
    else:
        print("⚠️ Folder already exists!")

# =========================
# GENERATE KEY
# =========================
def generate_key(folder):
    key = Fernet.generate_key()
    with open(f"{folder}_key.key", "wb") as f:
        f.write(key)

def load_key(folder):
    return open(f"{folder}_key.key", "rb").read()

# =========================
# SAVE PASSWORD
# =========================
def save_password(folder, password):
    with open(f"{folder}_pass.txt", "w") as f:
        f.write(hash_password(password))

def verify_password(folder, password):
    with open(f"{folder}_pass.txt", "r") as f:
        stored = f.read()
    return stored == hash_password(password)

# =========================
# ENCRYPT FILES
# =========================
def encrypt_files(folder):
    key = load_key(folder)
    fernet = Fernet(key)

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if os.path.isfile(path):
            with open(path, "rb") as f:
                data = f.read()

            encrypted = fernet.encrypt(data)

            with open(path, "wb") as f:
                f.write(encrypted)

# =========================
# DECRYPT FILES
# =========================
def decrypt_files(folder):
    key = load_key(folder)
    fernet = Fernet(key)

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if os.path.isfile(path):
            with open(path, "rb") as f:
                data = f.read()

            try:
                decrypted = fernet.decrypt(data)

                with open(path, "wb") as f:
                    f.write(decrypted)
            except:
                pass

# =========================
# LOCK FOLDER
# =========================
def lock_folder():
    folder = input("Enter folder name to lock: ")

    if not os.path.exists(folder):
        print("❌ Folder does not exist!")
        return

    password = getpass.getpass("Set password: ")

    save_password(folder, password)
    generate_key(folder)
    encrypt_files(folder)

    locked_name = folder + "_LOCKED"
    os.rename(folder, locked_name)

    print(f"\n🔒 Folder '{locked_name}' is LOCKED")
    print("🔐 Files are encrypted!")

# =========================
# UNLOCK FOLDER
# =========================
def unlock_folder():
    folder = input("Enter locked folder name: ")

    if not os.path.exists(folder):
        print("❌ Locked folder not found!")
        return

    original_name = folder.replace("_LOCKED", "")
    password = getpass.getpass("Enter password: ")

    if verify_password(original_name, password):
        os.rename(folder, original_name)
        decrypt_files(original_name)

        print(f"\n🔓 Folder '{original_name}' is UNLOCKED")
        print("🔓 Files are decrypted!\n")

        # Show files
        files = os.listdir(original_name)
        if files:
            print("📂 Files inside folder:")
            for f in files:
                print(f" - {f}")
        else:
            print("📂 Folder is empty")

    else:
        print("❌ Wrong password!")

# =========================
# MENU
# =========================
def main():
    while True:
        print("\n===== Secure Folder System =====")
        print("1. Create Folder")
        print("2. Lock Folder")
        print("3. Unlock Folder")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            create_folder()
        elif choice == '2':
            lock_folder()
        elif choice == '3':
            unlock_folder()
        elif choice == '4':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
