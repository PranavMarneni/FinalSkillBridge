from rest_framework import serializers
from .models import JobPostingURL

class JobPostingURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostingURL
        fields = ['id', 'url', 'created_at']
