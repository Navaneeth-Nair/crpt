from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RepositorySerializer, CommitSerializer, BlobSerializer
from .models import Repository, Commit, Blob
import os
import json
import base64

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def upload_page(request):
    return render(request, 'remote/upload.html')

@csrf_exempt
@api_view(['POST'])
def push(request):
    if request.FILES.get('file'):
        # Handle file upload case
        uploaded_file = request.FILES.get('file')
        filepath = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(filepath, 'wb+') as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)
        return Response({"status": "ok", "filename": uploaded_file.name})
    
    # Handle JSON push from CLI or frontend
    try:
        data = request.data
        repo_name = data.get("repo", "default")
        commit_data = data.get("commit")
        
        if not commit_data:
            return Response({"error": "No commit data provided"}, status=400)
            
        # Get or create repository
        repo, created = Repository.objects.get_or_create(name=repo_name)
        
        # Create commit
        commit = Commit(
            repo=repo,
            commit_id=commit_data["id"],
            message=commit_data["message"],
            branch=commit_data["branch"],
            parent=commit_data.get("parent")
        )
        commit.save()
        
        # Save blobs
        for blob_data in commit_data.get("blobs", []):
            blob = Blob(
                commit=commit,
                path=blob_data["path"],
                hash=blob_data["hash"],
                content=base64.b64decode(blob_data["content"])
            )
            blob.save()
        
        # Also save to file system for compatibility with old approach
        repo_dir = os.path.join(UPLOAD_DIR, repo_name)
        os.makedirs(repo_dir, exist_ok=True)
        os.makedirs(os.path.join(repo_dir, "refs", "heads"), exist_ok=True)
        os.makedirs(os.path.join(repo_dir, "commits", commit_data["id"]), exist_ok=True)
        os.makedirs(os.path.join(repo_dir, "objects"), exist_ok=True)
        
        # Save branch reference
        with open(os.path.join(repo_dir, "refs", "heads", commit_data["branch"]), 'w') as f:
            f.write(commit_data["id"])
            
        # Save commit message
        with open(os.path.join(repo_dir, "commits", commit_data["id"], "message.txt"), 'w') as f:
            f.write(commit_data["message"])
            
        # Save commit metadata
        with open(os.path.join(repo_dir, "commits", commit_data["id"], "meta.txt"), 'w') as f:
            if commit_data.get("parent"):
                f.write(f"Parent: {commit_data['parent']}\n")
            f.write(f"Message: {commit_data['message']}\n")
            for blob_data in commit_data.get("blobs", []):
                f.write(f"{blob_data['path']}:{blob_data['hash']}\n")
                
                # Save blob content
                with open(os.path.join(repo_dir, "objects", blob_data["hash"]), 'wb') as bf:
                    bf.write(base64.b64decode(blob_data["content"]))
            
        return Response({"status": "ok", "commit_id": commit_data["id"]})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@csrf_exempt
@api_view(['GET', 'POST'])
def pull(request):
    try:
        if request.method == "GET":
            # Handle GET request from frontend
            repos = Repository.objects.all()
            
            # If no repositories in database, check filesystem
            if not repos.exists():
                # Check if any repositories exist in the filesystem
                try:
                    repo_dirs = [d for d in os.listdir(UPLOAD_DIR) 
                                if os.path.isdir(os.path.join(UPLOAD_DIR, d))]
                    
                    # Create Repository objects for filesystem repos
                    for repo_name in repo_dirs:
                        if os.path.exists(os.path.join(UPLOAD_DIR, repo_name, "refs", "heads")):
                            Repository.objects.get_or_create(name=repo_name)
                    
                    # Re-query after possibly creating new repos
                    repos = Repository.objects.all()
                except:
                    pass
            
            # Serialize and return repositories
            response_data = []
            for repo in repos:
                response_data.append({
                    "id": repo.id,
                    "name": repo.name
                })
            return Response(response_data)
        
        # Handle POST request from CLI or frontend
        if request.method == "POST":
            data = request.data
            repo_name = data.get("repo", "default")
            branch = data.get("branch", "main")
            
            try:
                # First try to get from database
                repo = Repository.objects.get(name=repo_name)
                commit = Commit.objects.filter(repo=repo, branch=branch).order_by('-timestamp').first()
                
                if commit:
                    serializer = CommitSerializer(commit)
                    return Response({"commit": serializer.data})
            except (Repository.DoesNotExist, Commit.DoesNotExist):
                pass
                
            # If not in database, try to get from file system (backward compatibility)
            repo_dir = os.path.join(UPLOAD_DIR, repo_name)
            branch_file = os.path.join(repo_dir, f"refs/heads/{branch}")
            
            if not os.path.exists(branch_file):
                return Response({"error": f"Branch {branch} not found"}, status=404)
                
            with open(branch_file, 'r') as f:
                commit_id = f.read().strip()
                
            # Read commit data
            commit_dir = os.path.join(repo_dir, f"commits/{commit_id}")
            if not os.path.exists(commit_dir):
                return Response({"error": f"Commit {commit_id} not found"}, status=404)
                
            # Read message
            with open(os.path.join(commit_dir, "message.txt"), 'r') as f:
                message = f.read().strip()
                
            # Read metadata
            parent_id = None
            blobs = []
            with open(os.path.join(commit_dir, "meta.txt"), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("Parent:"):
                        parent_id = line.split(":", 1)[1].strip()
                    elif ":" in line and not line.startswith("Message"):
                        path, blob_hash = line.strip().split(":")
                        blob_path = os.path.join(repo_dir, f"objects/{blob_hash}")
                        
                        # Read and encode blob content
                        with open(blob_path, "rb") as bf:
                            encoded = base64.b64encode(bf.read()).decode()
                            
                        blobs.append({
                            "path": path,
                            "hash": blob_hash,
                            "content": encoded
                        })
            
            response_data = {
                "commit": {
                    "id": commit_id,
                    "commit_id": commit_id,  # For serializer compatibility
                    "message": message,
                    "parent": parent_id,
                    "branch": branch,
                    "blobs": blobs
                }
            }
            
            return Response(response_data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@csrf_exempt
@api_view(['GET'])
def branches(request, repo_name):
    try:
        # Try getting branches from database
        repo = Repository.objects.get(name=repo_name)
        branches = Commit.objects.filter(repo=repo).values('branch').distinct()
        branch_names = [b['branch'] for b in branches]
        
        # Also check filesystem for backward compatibility
        repo_dir = os.path.join(UPLOAD_DIR, repo_name)
        refs_dir = os.path.join(repo_dir, "refs", "heads")
        if os.path.exists(refs_dir):
            try:
                fs_branches = os.listdir(refs_dir)
                for branch in fs_branches:
                    if branch not in branch_names:
                        branch_names.append(branch)
            except:
                pass
                
        return Response({"branches": branch_names})
    except Repository.DoesNotExist:
        # If repo doesn't exist in DB, check filesystem
        repo_dir = os.path.join(UPLOAD_DIR, repo_name)
        refs_dir = os.path.join(repo_dir, "refs", "heads")
        
        if not os.path.exists(refs_dir):
            return Response({"error": f"Repository {repo_name} not found"}, status=404)
            
        try:
            branch_names = os.listdir(refs_dir)
            return Response({"branches": branch_names})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
