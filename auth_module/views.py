from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import (
                                        IsAuthenticated,
                                        AllowAny,
                                        )
from rest_framework import status
from rest_framework.response import Response
from auth_module.models import(
    City,
    Movie,
    Showtime,
    Cinema,
)
from rest_framework.viewsets import(
                                    ViewSet,
                                    )
from django.db import IntegrityError
from auth_module.serializers import(
    CitySerializer,
    MovieSerializer,
    CinemaSerializer,
    ShowtimeSerializer,
)

User = get_user_model()

class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        try:
            user = User(
                    username = request.data.get('username'),
                    first_name = request.data.get('first_name'),
                    last_name = request.data.get('last_name'),
                )
            user.set_password(request.data.get('password'))
            user.save()
            return Response({
                'message':'User registered'
            },status=status.HTTP_200_OK)
        except:
            return Response({
                'message':'User exists'
            },status=status.HTTP_200_OK)

class CityView(ViewSet):
    def create(self,request):
        try:
            City.objects.create(
                name = request.data.get('name'),
            )
            return Response({
                'message':'City added'
            },status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({
                'message':'City exists'
            },status=status.HTTP_200_OK)
    
    def list(self,request):
        city = City.objects.all()
        serializer = CitySerializer(city,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class MovieView(ViewSet):
    def create(self,request):
        try:
            movie = Movie.objects.create(
                name = request.data.get('name'),
            )
            try:
                city = City.objects.get(name = request.data.get('city'))
                movie.city.add(city)
                movie.save()
            except City.DoesNotExist:
                return Response({
                    'message':'City does not exist.'
                },status=status.HTTP_200_OK)
            return Response({
                    'message':'Movie added'
                },status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({
                'message':'City already added'
            },status=status.HTTP_200_OK)
        
    def retrieve(self,request,pk=None):
        movie = Movie.objects.filter(city__name = pk)
        serializer = MovieSerializer(movie,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class CinemaView(ViewSet):
    def create(self,request):
        try:
            cinema = Cinema.objects.create(
                name = request.data.get('name'),
            )
            cinema.movie.append(request.data.get('movie'))
            cinema.save()
            return Response({
                    'message':'Cinema added'
                },status=status.HTTP_200_OK)
        except IntegrityError:
            cinema = Cinema.objects.get(
                name = request.data.get('name'),
            )
            cinema.movie.append(request.data.get('movie'))
            cinema.save()
            return Response({
                'message':'Movie added'
            },status=status.HTTP_200_OK)
        
    def retrieve(self,request,pk=None):
        cinema = Cinema.objects.filter(movie__contains = [pk])
        serializer = CinemaSerializer(cinema,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ShowtimeView(ViewSet):
    def create(self,request):
        try:
            movie = Movie.objects.get(name = request.data.get('movie'))
            Showtime.objects.create(
                movie = movie,
                time = request.data.get('time'),
                seats = request.data.get('seats'),
            )
            return Response({
                'message':'Showtime saved'
            },status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({
                'message':'Movie does not exist.'
            },status=status.HTTP_200_OK)
        
    def retrieve(self,request,pk=None):
        movie = Movie.objects.get(name = pk)
        showtime = Showtime.objects.filter(movie = movie)
        serializer = ShowtimeSerializer(showtime,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)