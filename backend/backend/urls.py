from django.urls import path
from app import views  # Replace 'app' with the correct name of your app
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface
    path('api/submit-url/', views.submit_url_api, name='submit-url-api'),  # Submit URLs API
    path('api/process-urls/', views.process_urls, name='process-urls'),  # Process URLs API
    path('urls/', views.url_list, name='url_list'),  # List all submitted URLs
    path('', views.submit_url_api, name='home'),  # Home route for submitting URLs
]
