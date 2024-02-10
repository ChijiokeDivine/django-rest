from rest_framework import serializers
from dataclasses import fields
from .models import (Niche, Category, Product, ProductReview, CartOrder, CartOrderItems, ProductImages, wishlist, Address )
from userauths.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Check if the provided credentials are valid
        user = authenticate(email=email, password=password)

        if not user or not user.is_active:
            raise serializers.ValidationError("Incorrect credentials. Please try again.")

        data['user'] = user
        return data
    
    
class NicheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niche
        fields = ['id','vid','user', 'address','title','description', 'contact','chat_resp_time', 'date_joined', 'authentic_rating','warranty_period','shipping_in_time','days_return','image','cover_image']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['cid', 'image','title']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pid','user', 'category','title','image', 'image2','description', 'price', 'old_price','type','stock_count','life','mfd','specifications', 'product_status','status', 'in_stock', 'featured','digital','sku','date', 'updated']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = instance.category.title
        return representation
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['product', 'images','date']


class NicheDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niche
        fields = ['id','user', 'address']




class CartOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartOrder
        fields = ['user', 'price', 'paid_status','order_date', 'product_status']


class CartOrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartOrderItems
        fields = ['id','item', 'image','qty','price','total']


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['user','product','review','rating', 'date']

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model  = wishlist
        fields = ['user', 'product','date']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['user', 'address', 'status']