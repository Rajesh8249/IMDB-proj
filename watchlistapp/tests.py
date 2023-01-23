
from urllib import response
from django.contrib.auth.models import User
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlistapp.api import serializers
from watchlistapp import models



class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testcase",password="password@123",is_staff=True,is_superuser=True)
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="netflix",about="No1 streaming plaatform",website="https://www.Netflix.com")
    
    
    def test_streamplatform_craeate(self):
        data = {
            "name": "netflix",
            "about": "No1 streaming plaatform",
            "website": "https://www.Netflix.com"
        }
        response = self.client.post(reverse('streamplatform-list'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_streamplatform_list(self):
            response = self.client.get(reverse('streamplatform-list'))
            self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_streamplatform_ind(self):
            response = self.client.get(reverse('streamplatform-detail',args=(self.stream.id,)))
            self.assertEqual(response.status_code,status.HTTP_200_OK)



class WatchListTestCase(APITestCase):
    def setUp(self):
            self.user = User.objects.create_user(username="testcase",password="password@123",is_staff=True,is_superuser=True)
            self.token = Token.objects.get(user__username=self.user)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

            self.stream = models.StreamPlatform.objects.create(name="netflix",about="No1 streaming plaatform",website="https://www.Netflix.com")
            self.watchlist =  models.watchlist.objects.create(platform=self.stream,tittle="example movie",storyline="example story",active=True)
    
    def test_watchlist_create(self):
       data = {
        "platform": self.stream,
        "tittle": "example movie",
        "storyline": "example story",
        "active": True
       }
       response = self.client.post(reverse('movie_list'),data)
       self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_watchlist_list(self):
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie_details',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(models.watchlist.objects.get().tittle,'example movie')


class ReviewTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(username="testcase",password="password@123",is_staff=True,is_superuser=True)
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="netflix",about="No1 streaming plaatform",website="https://www.Netflix.com")
    
        self.watchlist =  models.watchlist.objects.create(platform=self.stream,tittle="example movie",storyline="example story",active=True)
        self.watchlist2 =  models.watchlist.objects.create(platform=self.stream,tittle="example movie",storyline="example story",active=True)
        self.review = models.Review.objects.create(review_user=self.user,rating = 5 ,description  = "great wall",watchlist = self.watchlist2,active=True)

    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "great wall",
            "watchlist": self.watchlist,
            "active": True            

        }

        response = self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(),2)
        # self.assertEqual(models.Review.objects.get().rating,5)

        response = self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


    def test_review_create_unauth(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "great wall",
            "watchlist": self.watchlist,
            "active": True            

        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "great wall-updated",
            "watchlist": self.watchlist,
            "active": False           

        }
        response = self.client.put(reverse('review-details',args=(self.review.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('review-list',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_ind(self):
        response = self.client.get(reverse('review-details',args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_delete(self):
        response = self.client.delete(reverse('review-details',args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get('/movie/review/?username' + self.user.username)
        self.assertEqual(response.status_code,status.HTTP_200_OK)