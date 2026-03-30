from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile, Amenity, Review, Property, PropertyImage,Rules,Booking,City,Country

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','first_name','role']

class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','first_name','role']

class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'

class AmenityNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['name']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewListSerializer(serializers.ModelSerializer):
    guest = UserProfileSerializer()
    created_date = serializers.DateTimeField(format='%Y-%m-%d')
    class Meta:
        model = Review
        fields = ['id', 'guest', 'comment', 'rating', 'created_date']

class ReviewDetailSerializer(serializers.ModelSerializer):
    guest = UserProfileSerializer()
    created_date = serializers.DateTimeField(format='%Y-%m-%d')
    class Meta:
        model = Review
        fields = ['guest', 'comment', 'rating', 'created_date']

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'

class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rules
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']

class CityListSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = City
        fields = ['id', 'country', 'city_name',]

class CityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class CityNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']

class PropertyListSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    count_review = serializers.SerializerMethodField()
    class Meta:
        model = Property
        fields = ['id', 'title', 'images', 'price_per_night', 'max_guests', 'bedrooms', 'bathrooms', 'avg_rating', 'count_review']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_review(self, obj):
        return obj.get_count_review()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class PropertyDetailSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    amenity_property = AmenityNameSerializer(many=True, read_only=True)
    reviews_property = ReviewListSerializer(many=True, read_only=True)
    city = CityNameSerializer()
    country = CountrySerializer()
    avg_rating = serializers.SerializerMethodField()
    count_review = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ['title', 'images', 'price_per_night', 'property_type', 'city', 'country',
          'avg_rating', 'count_review', 'max_guests', 'bedrooms', 'bathrooms',
          'owner', 'description', 'amenity_property', 'is_active', 'reviews_property']