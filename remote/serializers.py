from rest_framework import serializers
from .models import Repository, Commit, Blob

class BlobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blob
        fields = ['path', 'hash', 'content']

class CommitSerializer(serializers.ModelSerializer):
    blobs = BlobSerializer(many=True, read_only=True)
    
    class Meta:
        model = Commit
        fields = ['commit_id', 'message', 'branch', 'parent', 'timestamp', 'blobs']

class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ['id', 'name']