from .models import Users
from rest_framework import serializers

class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ('img_profile', 'gender', 'like_posts', 'username', 'password')
