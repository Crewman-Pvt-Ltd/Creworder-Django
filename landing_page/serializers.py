from rest_framework import serializers
from .models import Slider, ProductFeature, Testimonial, Client, AboutCompany, Highlight

class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'

class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class SocialMediaSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    logo = serializers.ImageField()  # Or use URLField if you want to allow URL inputs
    url = serializers.URLField()

class AboutCompanySerializer(serializers.ModelSerializer):
    socialmedia = SocialMediaSerializer(many=True)  # Allows multiple social media entries

    class Meta:
        model = AboutCompany
        fields = '__all__'


class HighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlight
        fields = '__all__'
