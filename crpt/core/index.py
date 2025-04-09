import os

def stage_file(file_path):
    if not os.path.exists('.crpt/index'):
        print("Repository not initialized.")
        return

    with open('.crpt/index', 'a') as index_file:
        index_file.write(f"{file_path}\n")
    print(f"Staged {file_path}")
