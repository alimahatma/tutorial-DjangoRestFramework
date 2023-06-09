# from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Movie, Rating
from .serializer import MovieSerializer, RatingSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:

            movie=Movie.objects.get(id=pk)
            stars=request.data['stars']
            user=request.user

            #update method on Django RestApi
            try:
                rating=Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars =stars
                rating.save()

                #add rating for serializers
                serializer=RatingSerializer(rating, many=False)
                response = {'message':'Rating is Update..','result':serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating=Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer=RatingSerializer(rating, many=False)
                response={'message':'Rating is Created ', 'result':serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            
        else:
            response = {'message':'You need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        response = {'message':'You can update rating like tahat'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        response = {'message':'You can create rating like tahat'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )

    def update(self, request, *args, **kwargs):
        response = {'message':'You can update rating like tahat'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        response = {'message':'You can create rating like tahat'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)




