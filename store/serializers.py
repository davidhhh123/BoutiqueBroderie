from django.contrib.auth.models import User
from rest_framework import serializers
from store.models import counter_props, products,products_commets_images,products_comment,checkout_products,delivery_check


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    online = serializers.ReadOnlyField(source='userprofile.online')

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'online']


class CounterSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = counter_props
        fields = '__all__'
class ArticleSerializer(serializers.ModelSerializer):
    counter_props = CounterSerializer(many=True, read_only=True)

    class Meta:
        model = products
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):
    

    class Meta:
        model = delivery_check
        fields = '__all__'
class CheckoutSerializer(serializers.ModelSerializer):
    delivery_check = DeliverySerializer(read_only=True)

    class Meta:
        model = checkout_products
        fields = '__all__'
        

class products_commets_imagesSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = products_commets_images
        fields = '__all__'
class CommentsSerializer(serializers.ModelSerializer):
    products_commets_images = products_commets_imagesSerializer(many=True, read_only=True)

    class Meta:
        model = products_comment
        fields = '__all__'