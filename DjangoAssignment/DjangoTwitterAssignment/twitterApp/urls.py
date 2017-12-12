from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from twitterApp import views
from rest_framework import routers
# ROUTER MODULE
router = routers.DefaultRouter()
router.register(r'savetweetcount', views.GetUserAndStoreTweetsView, 'getuserandstoretweet')
router.register(r'tweettrends', views.GetUserAndStoreTweetsfilterView, 'GetUserAndStoreTweetsfilterView')

urlpatterns = [
    url(r'^/follower/(?P<twitterhandle>\w+)', views.FollowerView.as_view()),
    url(r'^follower/', views.FollowerView.as_view()),
    url(r'^following/', views.FollowingView.as_view()),
    url(r'^toptweets/', views.TopTweetsView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
