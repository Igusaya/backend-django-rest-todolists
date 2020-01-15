from django.test import TestCase

from todo_lists_api.models import Card


class CardTests(TestCase):
    def test_card_create(self):
        """
        Insert test record test.
        """
        card = Card()
        card.name = 'test_name'
        card.position = '100'

        card.save()

        saved_card = Card.objects.all().order_by('-id')[0:1][0]
        self.assertEqual(saved_card.name, 'test_name')
        self.assertEqual(saved_card.position, 100)
        self.assertEqual(saved_card.color, '#FFFFFF')

