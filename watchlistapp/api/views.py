


from platform import platform
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError 
from rest_framework.permissions import AllowAny
#from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
#from watchlistapp.api import serializers
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
# from .permissions import ReviewUserOrReadOnly
from rest_framework.authentication import  BasicAuthentication
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from django.shortcuts import get_object_or_404

# from asyncio import mixins
# from rest_framework import mixins
from watchlistapp.api.permissions import IsAdminOrReadOnly,IsReviewUserOrReadOnly
from watchlistapp.models import watchlist, StreamPlatform,Review

from watchlistapp.api.serializers import (StreamPlatformSerializer, 
                                            watchlistSerializer,
                                            ReviewSerializer)
from watchlistapp.api.throttling import ReviewCreateThrottle,ReviewListThrottle 
from watchlistapp.api.pagination import watchListPagination,watchListLOpagination,watchListCurPagination                                 

# concrete view
class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle,AnonRateThrottle]



    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)


    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)



class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self,serializer,pk=None):
        pk = self.kwargs.get('pk')
        watchlist1 = watchlist.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist1,review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("you have already reviewed done")


        if watchlist1.number_rating == 0:
            watchlist1.avg_rating = serializer.validated_data['rating']
        else:
            watchlist1.avg_rating = (watchlist1.avg_rating + serializer.validated_data['rating'])/2

        watchlist1.number_rating = watchlist1.number_rating + 1
        watchlist1.save()

        serializer.save(watchlist=watchlist1,review_user=review_user)



class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)



class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'



# mixins
# class ReviewDetail(mixins.RetrieveModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class StreamPlatformVS(viewsets.ModelViewSet):


    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]
# class StreamPlatformVS(viewsets.ViewSet):
    
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)






# APIView
class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform,many=True)

        return Response(serializer.data)
    def post(self,request):
        serializer = StreamPlatformSerializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

  
class StreamPlatfromdetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk=None):
 
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error:platform not found'},status=status.HTTP_400_BAD_REQUEST)
        serializer=StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self,request,pk=None):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer=StreamPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk=None):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)            


class watchList(generics.ListAPIView):
    queryset = watchlist.objects.all()
    serializer_class = watchlistSerializer
    # pagination_class = watchListPagination
    # pagination_class = watchListLOpagination
    pagination_class = watchListCurPagination
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle,AnonRateThrottle]
    filter_backends = [filters.SearchFilter,]
    search_fields= ['tittle', 'platform__name']


class watchlistAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        movie1 = watchlist.objects.all()
        serializer = watchlistSerializer(movie1,many=True)
        return Response(serializer.data)

    def post(self,request):
        print(request.data)
        serializer = watchlistSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            print("@@@@",serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class watchlistdetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk=None):
 
        try:
            movie1 = watchlist.objects.get(pk=pk)
        except movie1.DoesNotExist:
            return Response({'error:movie1 not found'},status=status.HTTP_400_BAD_REQUEST)
        serializer=watchlistSerializer(movie1)
        return Response(serializer.data)

    def put(self,request,pk=None):
        movie1 = watchlist.objects.get(pk=pk)
        serializer=watchlistSerializer(movie1,data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk=None):
        movie1 = watchlist.objects.get(pk=pk)
        movie1.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        



# @api_view(['GET','POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movie1 = movie.objects.all()
#         serializer = MovieSearializer(movie1,many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = MovieSearializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()

#             return Response(serializer.data)
#         else:

#             return Response(serializer.errors)

# @api_view(['GET','PUT','DELETE'])
# def movie_details(request,pk):
#     if request.method == 'GET':
#         try:
#             movie1=movie.objects.get(pk=pk)
#         except movie.DoesNotExist:
#             return Response ({'error': 'movie1 not found'},status=status.HTTP_404_NOT_FOUND)
#             serializer=MovieSearializer(movie1)
#             return Response(serializer.data)
#     if request.method == 'PUT':
#         movie1=movie.objects.get(pk=pk)
#         serializer = MovieSearializer(movie1,data=request.data)
#         if serializer.is_valid():
#             serializer.save()

#             return Response(serializer.data)
#         else:

#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         movie1=movie.objects.get(pk=pk)
#         movie1.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

