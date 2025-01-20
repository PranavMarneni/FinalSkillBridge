from django.db import models

class UploadedPDF(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

class JobPostingURL(models.Model):
    url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
