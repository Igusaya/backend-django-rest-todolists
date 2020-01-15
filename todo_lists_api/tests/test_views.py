import json
from rest_framework.exceptions import ErrorDetail

from django.test import TestCase
from django.urls import reverse
from django.http import Http404
from rest_framework import status

from todo_lists_api.models import Card
from todo_lists_api.views import CardDetail
from todo_lists_api.tests.utils import Cleater


class CardTests(TestCase):

    def test_get(self):
        """
        Nomal test.
        Throw a get request.
        """
        url = '/cards/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_post(self):
        """
        Nomal test.
        Assign the maximum value to each item.
        """
        url = '/cards/'
        data = {
                'name': 'test name ########################################',
                'position': 100,
                'color': '#191919',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(Card.objects.get().name, 'test name ########################################')
        self.assertEqual(Card.objects.get().color, '#191919')


    def test_validate_color_max_value(self):
        """
        Boundary value abnomarl test.
        Assign 8 characters to color
        """
        url = '/cards/'
        data = {
                'name': 'test name',
                'position': 100,
                'color': '#1919191',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Card.objects.count(), 0)
        self.assertIn('color', response.data)
        self.assertEqual(response.data['color'][0].code, 'max_length')


    def test_validate_name_max_value(self):
        """
        Boundary value abnomarl test.
        Assign 51 characters to name
        """
        url = '/cards/'
        data = {
                'name': 'test name ########################################1',
                'position': 100,
                'color': '#191919',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Card.objects.count(), 0)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'][0].code, 'max_length')


    def test_get_object(self):
        """
        Nomal test of CardDetail.get_object methode.
        """
        creater = Cleater()
        id = creater.create_card()
        card_detail = CardDetail()
        object = CardDetail().get_object(pk=id)

        self.assertEqual(object.name, 'test_name')


    def test_get_object_abnomal(self):
        """
        Abnomal test of CardDetail.get_object methode.
        """
        with self.assertRaises(Http404):
            CardDetail().get_object(pk=0)


    def test_get_card_detail(self):
        """
        Nomal test of CardDetail.put methode.
        """
        id = Cleater().create_card()
        url = '/cards/' + str(id) + '/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_name')
        self.assertEqual(response.data['id'], 1)


    def test_put_card_detail(self):
        """
        Nomal test of CardDetail.put methode.
        """
        id = Cleater().create_card()
        url = '/cards/' + str(id) + '/'
        data = json.dumps({
                'name': 'update_name',
                'position': 999,
                'color': '#333333',
        })
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(Card.objects.get().name, 'update_name')
        self.assertEqual(Card.objects.get().position, 999)
        self.assertEqual(Card.objects.get().color, '#333333')


    def test_delete_card_detail(self):
        """
        Nomal test of CardDetail.delete methode.
        """
        id = Cleater().create_card()
        url = '/cards/' + str(id) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Card.objects.count(), 0)
