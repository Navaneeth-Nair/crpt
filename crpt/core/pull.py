import os
import base64
import requests

def pull(repo_name="default", remote_url="http://127.0.0.1:8000/pull/"):
    if not os.path.exists('.crpt/HEAD'):
        print("No repo found.")
        return

    # get current branch
    with open('.crpt/HEAD', 'r') as f:
        ref = f.read().strip()
    branch = ref.split("/")[-1]

    payload = {
        "repo": repo_name,
        "branch": branch
    }

    response = requests.post(remote_url, json=payload)
    if response.status_code != 200:
        print("❌ Pull failed:", response.text)
        return

    data = response.json()["commit"]
    commit_id = data["id"]
    commit_dir = f".crpt/commits/{commit_id}"
    os.makedirs(commit_dir, exist_ok=True)

    # write message
    with open(f"{commit_dir}/message.txt", "w") as f:
        f.write(data["message"])

    # write meta
    with open(f"{commit_dir}/meta.txt", "w") as f:
        f.write(f"Parent: {data.get('parent')}\n")
        f.write(f"Message: {data['message']}\n")
        for blob in data["blobs"]:
            f.write(f"{blob['path']}:{blob['hash']}\n")

    # write blobs
    for blob in data["blobs"]:
        blob_path = f".crpt/objects/{blob['hash']}"
        os.makedirs(".crpt/objects", exist_ok=True)
        with open(blob_path, "wb") as f:
            f.write(base64.b64decode(blob["content"]))

        # write to working directory
        with open(blob["path"], "wb") as f:
            f.write(base64.b64decode(blob["content"]))

    # update HEAD reference
    with open(f".crpt/refs/heads/{branch}", "w") as f:
        f.write(commit_id)

    print(f"✅ Pulled latest commit: {commit_id[:7]}")
