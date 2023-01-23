from django.urls import path,include
# from watchlistapp.api.views import  movie_list,movie_details
from rest_framework.routers import DefaultRouter

from watchlistapp.api.views import  (ReviewDetail, 
                                     ReviewList,ReviewCreate, 
                                    StreamPlatformAV, 
                                    StreamPlatfromdetailAV,
                                    watchlistAV,
                                    watchlistdetailAV,StreamPlatformVS,UserReview,watchList)

router = DefaultRouter()
router.register('streamview',StreamPlatformVS,basename='streamplatform')


urlpatterns = [
    path('list/',watchlistAV.as_view(),name='movie_list'),
    path('<int:pk>',watchlistdetailAV.as_view(),name='movie_details'),
    path('list2/',watchList.as_view(),name='watch-list'),


    # path('',include('router.urls')),
    path('stream/',StreamPlatformAV.as_view(),name='stream-list'),
    path('stream/<int:pk>',StreamPlatfromdetailAV.as_view(),name='stream-details'),
    path('watchlist/',watchlistAV.as_view(),name='watch-list'),
    path('watchlist/<int:pk>',watchlistdetailAV.as_view(),name='watch-details'),
    path('review',ReviewList.as_view(),name='review-list'),
    path('review/<int:pk>',ReviewDetail.as_view(),name='review-details'),
    path('<int:pk>/review-create',ReviewCreate.as_view(),name='review-create'),
    path('<int:pk>/review',ReviewList.as_view(),name='review-list'),
    path('review/<int:pk>',ReviewDetail.as_view(),name='review-details'),
    path('review/',UserReview.as_view(),name='user-review-detail'),
 ]
 
urlpatterns += router.urls