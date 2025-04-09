from django.db import models

class Repository(models.Model):
    name = models.CharField(max_length=100)

class Commit(models.Model):
    repo = models.ForeignKey(Repository, on_delete=models.CASCADE)
    commit_id = models.CharField(max_length=40, unique=True)
    message = models.TextField()
    branch = models.CharField(max_length=100)
    parent = models.CharField(max_length=40, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Blob(models.Model):
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE, related_name='blobs')
    path = models.CharField(max_length=255)   # e.g. README.md
    hash = models.CharField(max_length=40)
    content = models.BinaryField()
