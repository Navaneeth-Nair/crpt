import os
import shutil
import hashlib

REFS_DIR = ".crpt/refs/heads"

def hash_file(file_path):
    with open(file_path, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()

def checkout_branch(branch_name):
    branch_path = f"{REFS_DIR}/{branch_name}"
    if not os.path.exists(branch_path):
        print(f"Branch '{branch_name}' does not exist.")
        return

    with open(branch_path, 'r') as f:
        commit_id = f.read().strip()

    # Load commit data
    commit_meta = f".crpt/commits/{commit_id}/meta.txt"
    if not os.path.exists(commit_meta):
        print(f"Commit data for {commit_id[:7]} is missing.")
        return

    # Clear working directory (simplified: just overwrite files)
    with open(commit_meta, 'r') as meta:
        for line in meta:
            if ":" in line and not line.startswith("Message"):
                file_path, file_hash = line.strip().split(":")
                blob = f".crpt/objects/{file_hash}"
                if os.path.exists(blob):
                    shutil.copy2(blob, file_path)

    # Update HEAD
    with open('.crpt/HEAD', 'w') as f:
        f.write(f"refs/heads/{branch_name}")

    print(f"Switched to branch '{branch_name}'")