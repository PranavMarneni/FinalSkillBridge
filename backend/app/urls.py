from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('api/submit-url/', views.submit_url_api, name='submit-url'),
    path('api/process-urls/', views.process_urls, name='process-urls'),
    path('api/url-list/', views.url_list, name='url-list'),
    path('api/store-pdf/', views.store_pdf_text, name='store-pdf'),
]
