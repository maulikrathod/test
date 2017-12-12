#  IMPORT REST_FRAMEWORK MODULES
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
# IMPORT DJANGO CORE MODULES
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from django.shortcuts import render
from django.http import HttpResponse
# IMPORT LOCAL FILES FROM APP
from twitterApp.models import DatewiseTweets
from twitterApp.serializers import *
# twitterFucntions FILE
from twitterFucntions import (find_followers, following, get_tweet_from_name, get_tweets)


class FollowerView(APIView):
    """
    This GET request will take a twitter handle (i.e., netflix) and return the response
    in JSON format with total number of followers for the given twitter handle.
    """
    def get(self, request, *args):
        name = request.GET.get('twitterhandle')
        followers = find_followers(name)
        return Response({'Twitter Handle': name, 'followers': followers})

class FollowingView(APIView):
    """
    This GET request will take a twitter handle (i.e., netflix) and return the response
    in JSON format with total number of twitter account the given twitter handle is following.
    """
    def get(self, request, *args):
        name = request.GET.get('twitterhandle')
        total_following = following(name)
        return Response({'Twitter Handle': name, 'following': total_following})

class TopTweetsView(APIView):
    """
    This GET request will take a twitter handle(i.e., netflix) and return the response in JSON format with top 10 tweets of the given twitter handle.
    """
    def get(self, request, *args):
        name = request.GET.get('twitterhandle')
        top_tweets = get_tweet_from_name(name)
        return Response({'Twitter Handle': name, 'top_tweets': top_tweets})

class GetUserAndStoreTweetsView(viewsets.ModelViewSet):
    """
    This PUT/POST request will take a twitter handle (i.e., netflix) as input in JSON
    format and save the number of tweet of the given twitter handle day wise in the Database.
    """
    serializer_class = GetUserAndStoreTweetsSerializer
    queryset = DatewiseTweets.objects.all()

    def get_queryset(self):
        return DatewiseTweets.objects.all()

    def create(self, request):
        tweets_obj = get_tweets(request.POST.get('name'),10)
        for tweets in tweets_obj:
            serializer = self.serializer_class(data=tweets)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(tweets_obj, status=status.HTTP_201_CREATED)

class GetUserAndStoreTweetsfilterView(viewsets.ModelViewSet):
    """
    This GET request will take a twitter handle (i.e., netflix) and format a JSON with
    number of tweet of the given twitter handle day wise from the Database.
    """
    serializer_class = GetUserAndStoreTweetsSerializer
    queryset = DatewiseTweets.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = {
        'name': ['exact']
    }
    http_method_names = ['get']
    def get_queryset(self):
        return DatewiseTweets.objects.all()
