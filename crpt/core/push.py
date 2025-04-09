import os
import json
import base64
import requests

def push(repo_name="default", remote_url="http://127.0.0.1:8000/push/"):
    if not os.path.exists('.crpt/HEAD'):
        print("No repo found.")
        return

    # get current branch
    with open('.crpt/HEAD', 'r') as f:
        ref = f.read().strip()
    branch = ref.split("/")[-1]

    # get latest commit
    head_ref_path = f".crpt/{ref}"
    if not os.path.exists(head_ref_path):
        print("Nothing to push.")
        return

    with open(head_ref_path, 'r') as f:
        commit_id = f.read().strip()

    commit_dir = f".crpt/commits/{commit_id}"
    if not os.path.exists(commit_dir):
        print("Commit not found.")
        return

    # parse commit metadata
    with open(f"{commit_dir}/meta.txt") as f:
        lines = f.readlines()

    blobs = []
    parent_id = None
    for line in lines:
        if line.startswith("Parent:"):
            parent_id = line.split(":", 1)[1].strip()
        elif ":" in line and not line.startswith("Message"):
            path, blob_hash = line.strip().split(":")
            blob_path = f".crpt/objects/{blob_hash}"
            with open(blob_path, "rb") as bf:
                encoded = base64.b64encode(bf.read()).decode()
            blobs.append({
                "path": path,
                "hash": blob_hash,
                "content": encoded
            })

    with open(f"{commit_dir}/message.txt") as f:
        message = f.read().strip()

    payload = {
        "repo": repo_name,
        "commit": {
            "id": commit_id,
            "message": message,
            "branch": branch,
            "parent": parent_id,
            "blobs": blobs
        }
    }

    response = requests.post(remote_url, json=payload)
    if response.status_code == 200:
        print("✅ Push successful.")
    else:
        print("❌ Push failed:", response.text)
