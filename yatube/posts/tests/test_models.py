from django.test import TestCase, Client

from posts.models import Group, Post


class StrModelTests(TestCase):

    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()

        self.test_group = Group()
        self.test_group.title = 'first_test_group'
        self.test_group.slug = 'first_test_group'

        self.test_post = Post()
        self.test_post.text = 'test post text for test __str__'

    def test_smoke(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_str(self):
        self.assertEqual(f'{self.test_group}', 'first_test_group')

    def test_post_str(self):
        self.assertEqual(f'{self.test_post}', 'test post text ')
