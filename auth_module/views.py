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
    Booking,
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
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

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
            logger.error('Something went wrong!')
            return Response({
                'message':'City already added'
            },status=status.HTTP_200_OK)
        
    def retrieve(self,request,pk=None):
        movie = Movie.objects.filter(city__name = pk)
        serializer = MovieSerializer(movie,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class CinemaView(ViewSet):
    permission_classes = (AllowAny,)

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
            logger.error('Something went wrong!')
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
    permission_classes = (AllowAny,)

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
            logger.error('Something went wrong!')
            return Response({
                'message':'Movie does not exist.'
            },status=status.HTTP_200_OK)
        
    def retrieve(self,request,pk=None):
        movie = Movie.objects.get(name = pk)
        showtime = Showtime.objects.filter(movie = movie)
        serializer = ShowtimeSerializer(showtime,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class SeatView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        showtime = Showtime.objects.filter(
            movie = request.data.get('movie'),
            time = request.data.get('time'),
        )
        serializer = ShowtimeSerializer(showtime,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class BookView(ViewSet):
    def create(self,request):
        try:
            showtime = Showtime.objects.get(
                movie = request.data.get('movie'),
                time = request.data.get('time'),
            )
            Booking.objects.create(
                showtime = showtime,
                user = request.user,
            )
            showtime.seats -= request.data.get('number_of_seats',0)
            if showtime.seats >= 0:
                showtime.save()
                return Response({'message':'booked'},status=status.HTTP_200_OK)
            else:
                return Response({'message':'Tickets unavailable'},status=status.HTTP_200_OK)
        except Showtime.DoesNotExist:
            logger.error('Something went wrong!')
            return Response({'message':'Showtime unavailable'},status=status.HTTP_200_OK)