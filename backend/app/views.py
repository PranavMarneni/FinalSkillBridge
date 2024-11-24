from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import JobPostingURL
from .serializer import JobPostingURLSerializer
from .royce import getSkillSet
from .web_scrapper import main_method

# Store the URLs when submitted by the user
@api_view(['POST'])
def submit_url_api(request):
    if request.method == 'POST':
        serializer = JobPostingURLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Process the URLs when the user is done submitting
@api_view(['POST'])
def process_urls(request):
    # Retrieve all the URLs (you could filter based on the session or other identifier)
    urls = JobPostingURL.objects.all()
    # Assuming getSkillSet processes these URLs in your app
    processed_data = main_method(urls)  # Replace with your actual processing logic
    
    return Response({"message": "URLs processed", "data": processed_data}, status=200)


# View to list all submitted URLs
@api_view(['GET'])
def url_list(request):
    urls = JobPostingURL.objects.all()  # Fetch all submitted URLs
    serializer = JobPostingURLSerializer(urls, many=True)
    return Response(serializer.data, status=200)
