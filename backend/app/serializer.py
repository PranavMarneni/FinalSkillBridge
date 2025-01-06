from rest_framework import serializers
from .models import UploadedPDF, JobPostingURL


class UploadedPDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedPDF
        fields = ['id', 'name', 'uploaded_at']


class JobPostingURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostingURL
        fields = ['url', 'created_at']
