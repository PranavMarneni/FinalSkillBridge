from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import JobPostingURL, UploadedPDF
from .serializer import JobPostingURLSerializer, UploadedPDFSerializer
from .api.job_processing import process_job_urls
from django.http import HttpResponse


@api_view(['POST'])
def submit_url_api(request):
    serializer = JobPostingURLSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


def homepage(request):
    return HttpResponse("<h1>Welcome to SkillBridge Backend!</h1><p>API is running successfully.</p>")

@api_view(['POST'])
def process_urls(request):
    urls = JobPostingURL.objects.all()
    if not urls.exists():
        return Response({"error": "No job URLs found."}, status=400)
    
    try:
        processed_data = process_job_urls(urls)
        if 'error' in processed_data:
            return Response({"error": processed_data['error']}, status=400)
        
        return Response({
            "message": "URLs processed successfully.",
            "study_plan": processed_data['study_plan']
        }, status=200)
    except Exception as e:
        return Response({"error": f"Processing failed: {str(e)}"}, status=500)


@api_view(['GET'])
def url_list(request):
    urls = JobPostingURL.objects.all()
    serializer = JobPostingURLSerializer(urls, many=True)
    return Response(serializer.data, status=200)


@api_view(['POST'])
def store_pdf_text(request):
    try:
        pdf_text = request.data.get('pdf_text', '')
        pdf_name = request.data.get('pdf_name', 'Unnamed PDF')

        if not pdf_text:
            return Response({"error": "No PDF text provided"}, status=400)

        # Store in the database
        UploadedPDF.objects.create(name=pdf_name, text=pdf_text)
        return Response({"message": "PDF uploaded successfully. You can now submit job links."}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
