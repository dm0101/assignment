from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from auth_module.models import(
    City,
    Movie,
    Showtime,
    Cinema,
    Booking,
)

import logging
from logging import Logger

from pycdi import Inject, Singleton, Producer
from pycdi.shortcuts import call


@Producer(_context='app_name')
def get_app_name() -> str:
    return 'PyCDI'


@Singleton()
@Inject(logger_name='app_name')
def get_logger(logger_name: str) -> Logger:
    return logging.getLogger(logger_name)


@Inject(name='app_name')
def main(name: str, logger: Logger):
    logger.info('I\'m starting...')
    print('Hello World!!!\nI\'m an example of %s' % name)
    logger.debug('I\'m finishing...')


call(main)

class CityAPITestCase(APITestCase):

    def test_create(self):
        data = {"name":"Pune"}
        response = self.client.post('/auth/city/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get(self):
        data = {"name":"Pune"}
        response = self.client.get('/auth/city/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class MovieAPITestCase(APITestCase):

    def test_create(self):
        data = {"name":"Movie 2","city":"Nagpur"}
        response = self.client.post('/auth/movie/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get(self):
        response = self.client.get(reverse('auth_module:movie', kwargs={"pk":'Nagpur'}), format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)