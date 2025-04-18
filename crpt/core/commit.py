import os
import hashlib
import time
import shutil
from .encrypt import encrypt_file_content, get_or_create_encryption_key

def hash_file(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()

def create_commit(message):
    if not os.path.exists('.crpt/index'):
        print("Repository not initialized.")
        return

    with open('.crpt/index', 'r') as f:
        staged_files = f.read().splitlines()

    if not staged_files:
        print("No files staged.")
        return

    # Get encryption key or create one
    encryption_key = get_or_create_encryption_key()

    timestamp = str(int(time.time()))
    commit_id = hashlib.sha1((message + timestamp).encode()).hexdigest()
    commit_dir = f".crpt/commits/{commit_id}"
    os.makedirs(commit_dir)

    # Store parent commit if exists
    if os.path.exists('.crpt/HEAD'):
        with open('.crpt/HEAD', 'r') as head:
            parent_commit = head.read().strip()
            if parent_commit:
                with open(f"{commit_dir}/meta.txt", 'w') as meta:
                    meta.write(f"Parent: {parent_commit}\n")

    # Copy and encrypt files to objects and store file hashes
    with open(f"{commit_dir}/meta.txt", 'a') as meta:
        meta.write(f"Message: {message}\nTime: {timestamp}\n")

        # Make sure objects directory exists
        os.makedirs(".crpt/objects", exist_ok=True)
        
        for file in staged_files:
            if not os.path.exists(file): continue
            file_hash = hash_file(file)
            meta.write(f"{file}:{file_hash}\n")

            # Read file content and encrypt it
            with open(file, 'rb') as f:
                content = f.read()
                
            # Encrypt the content - we use file_hash as the password for extra security
            encrypted_content = encrypt_file_content(content, file_hash)
                
            # Save encrypted content
            with open(f".crpt/objects/{file_hash}", 'wb') as f:
                f.write(encrypted_content)

    # Record commit message separately for easier access
    with open(f"{commit_dir}/message.txt", 'w') as f:
        f.write(message)

    # Get current branch
    current_branch = 'main'  # Default branch
    if os.path.exists('.crpt/HEAD'):
        with open('.crpt/HEAD', 'r') as f:
            head_content = f.read().strip()
            if head_content.startswith('ref:'):
                current_branch = head_content.split('/')[-1]

    # Ensure refs/heads directory exists
    os.makedirs(".crpt/refs/heads", exist_ok=True)

    # Update branch reference
    with open(f".crpt/refs/heads/{current_branch}", 'w') as f:
        f.write(commit_id)

    # Update HEAD to point to the branch reference
    with open('.crpt/HEAD', 'w') as head:
        head.write(f"ref: refs/heads/{current_branch}")

    # Clear staging area
    open('.crpt/index', 'w').close()

    print(f"✅ Committed as {commit_id[:7]} on branch {current_branch}")
