# VX Ghost Diary - Rare Launch ++
# A secret diary that encrypts your notes, lets you decrypt them later, and search notes

from cryptography.fernet import Fernet
import os

# ---------- Key Handling ----------
def load_or_create_key():
    """Load the encryption key, or create one if it doesn't exist"""
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as f:
            f.write(key)
        print("🔑 New key generated and saved as key.key")
    else:
        with open("key.key", "rb") as f:
            key = f.read()
    return key

# ---------- Encrypt & Save ----------
def encrypt_and_save(note, cipher):
    """Encrypt note and save it to diary.txt"""
    encrypted = cipher.encrypt(note.encode())
    with open("diary.txt", "ab") as f:  # append mode
        f.write(encrypted + b"\n")
    print("✅ Note encrypted and saved!")

# ---------- Decrypt & Read ----------
def decrypt_and_read(cipher):
    """Read and decrypt all notes"""
    if not os.path.exists("diary.txt"):
        print("⚠️ No notes saved yet!")
        return
    with open("diary.txt", "rb") as f:
        lines = f.readlines()
    print("\n📖 Your Secret Notes:")
    for i, line in enumerate(lines, start=1):
        try:
            decrypted = cipher.decrypt(line.strip())
            print(f"{i}. {decrypted.decode()}")
        except:
            print(f"{i}. [Failed to decrypt]")
    print("---------------------\n")

# ---------- Search Notes ----------
def search_notes(cipher, keyword):
    """Search decrypted notes by keyword"""
    if not os.path.exists("diary.txt"):
        print("⚠️ No notes saved yet!")
        return
    with open("diary.txt", "rb") as f:
        lines = f.readlines()

    print(f"\n🔍 Search results for '{keyword}':")
    found = False
    for i, line in enumerate(lines, start=1):
        try:
            decrypted = cipher.decrypt(line.strip()).decode()
            if keyword.lower() in decrypted.lower():
                print(f"{i}. {decrypted}")
                found = True
        except:
            continue
    if not found:
        print("❌ No matching notes found.")
    print("---------------------\n")

# ---------- Main ----------
def main():
    key = load_or_create_key()
    cipher = Fernet(key)

    while True:
        print("\n--- VX Ghost Diary ---")
        print("1. Write a secret note")
        print("2. Read all notes")
        print("3. Search notes")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            note = input("Enter your secret note: ")
            encrypt_and_save(note, cipher)

        elif choice == "2":
            decrypt_and_read(cipher)

        elif choice == "3":
            keyword = input("Enter keyword to search: ")
            search_notes(cipher, keyword)

        elif choice == "4":
            print("👻 Closing Ghost Diary Man...")
            break

        else:
            print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
