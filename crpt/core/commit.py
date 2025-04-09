import os
import hashlib
import time
import shutil

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

    timestamp = str(int(time.time()))
    commit_id = hashlib.sha1((message + timestamp).encode()).hexdigest()
    commit_dir = f".crpt/commits/{commit_id}"
    os.makedirs(commit_dir)

    # Copy files to objects and store file hashes
    with open(f"{commit_dir}/meta.txt", 'w') as meta:
        meta.write(f"Message: {message}\nTime: {timestamp}\n")

        for file in staged_files:
            if not os.path.exists(file): continue
            file_hash = hash_file(file)
            meta.write(f"{file}:{file_hash}\n")

            shutil.copy2(file, f".crpt/objects/{file_hash}")

    # Update HEAD (simplified)
    with open('.crpt/HEAD', 'w') as head:
        head.write(commit_id)

    # Clear staging area
    open('.crpt/index', 'w').close()

    print(f"Committed as {commit_id[:7]}")
