from django.contrib import admin
from .models import JobPostingURL
from .models import UploadedPDF

@admin.register(JobPostingURL)
class JobPostingURLAdmin(admin.ModelAdmin):
    list_display = ('url', 'created_at')
    search_fields = ('url',)
    ordering = ('-created_at',)


@admin.register(UploadedPDF)
class UploadedPDFAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_at')
    search_fields = ('name',)