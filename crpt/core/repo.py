import os

def init_repo():
    if os.path.exists('.crpt'):
        print("Repository already initialized.")
        return

    os.makedirs('.crpt/objects')
    os.makedirs('.crpt/commits')
    with open('.crpt/HEAD', 'w') as f:
        f.write("refs/heads/main")
    with open('.crpt/index', 'w') as f:
        f.write("")

    print("Initialized empty CRPT repository in .crpt/")
