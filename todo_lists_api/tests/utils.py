from todo_lists_api.models import Card

class Cleater():
    def create_card(self):
        card = Card()
        card.name = 'test_name'
        card.position = '100'
        card.save()
        return Card.objects.all().order_by('-id')[0:1][0].id

