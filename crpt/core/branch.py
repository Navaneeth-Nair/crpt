import os

REFS_DIR = ".crpt/refs/heads"

def ensure_refs_dir():
    os.makedirs(REFS_DIR, exist_ok=True)

def get_current_branch():
    if not os.path.exists('.crpt/HEAD'):
        return None
    with open('.crpt/HEAD', 'r') as f:
        ref = f.read().strip()
    if ref.startswith("refs/heads/"):
        return ref[len("refs/heads/"):]
    return ref

def list_branches():
    ensure_refs_dir()
    branches = os.listdir(REFS_DIR)
    current = get_current_branch()
    for b in branches:
        prefix = "*" if b == current else " "
        print(f"{prefix} {b}")

def create_branch(branch_name):
    ensure_refs_dir()

    # Get current HEAD commit
    current = get_current_branch()
    head_path = f"{REFS_DIR}/{branch_name}"

    if os.path.exists(head_path):
        print(f"Branch '{branch_name}' already exists.")
        return

    if not os.path.exists('.crpt/HEAD'):
        print("Repository not initialized.")
        return

    with open('.crpt/HEAD', 'r') as f:
        current_ref = f.read().strip()

    current_commit = None
    if current_ref.startswith("refs/heads/"):
        ref_path = f".crpt/{current_ref}"
        if os.path.exists(ref_path):
            with open(ref_path, 'r') as rf:
                current_commit = rf.read().strip()
    else:
        current_commit = current_ref

    with open(head_path, 'w') as f:
        if current_commit:
            f.write(current_commit)

    print(f"Created branch '{branch_name}'")