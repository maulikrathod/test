from rest_framework import serializers, fields
from twitterApp.models import DatewiseTweets

# SERIALIZER CLASS TO SERIALIZE MODEL
class GetUserAndStoreTweetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatewiseTweets
        fields = '__all__'
