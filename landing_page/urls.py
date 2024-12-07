from django.urls import path
from .views import (
    SliderAPIView,
    ProductFeatureAPIView,
    TestimonialAPIView,
    ClientAPIView,
    AboutCompanyAPIView,
    HighlightAPIView
)

urlpatterns = [
    path('sliders/', SliderAPIView.as_view(), name='slider-list'),
    path('sliders/<int:id>/', SliderAPIView.as_view(), name='slider-detail'),

    path('product-features/', ProductFeatureAPIView.as_view(), name='product-feature-list'),
    path('product-features/<int:id>/', ProductFeatureAPIView.as_view(), name='product-feature-detail'),

    path('testimonials/', TestimonialAPIView.as_view(), name='testimonial-list'),
    path('testimonials/<int:id>/', TestimonialAPIView.as_view(), name='testimonial-detail'),

    path('clients/', ClientAPIView.as_view(), name='client-list'),
    path('clients/<int:id>/', ClientAPIView.as_view(), name='client-detail'),

    path('about-company/', AboutCompanyAPIView.as_view(), name='about-company-list'),
    path('about-company/<int:id>/', AboutCompanyAPIView.as_view(), name='about-company-detail'),

    path('highlights/', HighlightAPIView.as_view(), name='highlight-list'),
    path('highlights/<int:id>/', HighlightAPIView.as_view(), name='highlight-detail'),
]
