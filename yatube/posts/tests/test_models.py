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

        self.test_post = Post(text='test post text for test __str__')

    def test_smoke(self):
        """'Дымовой тест'. Проверить, что на запрос '/' ответ 200."""
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200,
            'Неавторизованный пользователь не получает стартовую страницу'
        )

    def test_group_str(self):
        """Проверить, что Group.__str__ возвращает название группы."""
        self.assertEqual(f'{self.test_group}', 'first_test_group',
            'Нужно проверить, как работает метод Group.__str__'
        )

    def test_post_str(self):
        """Проверить, что Post.__str__ возвращает первые 15 символов поста."""
        self.assertEqual(f'{self.test_post}', 'test post text ',
            'Нужно проверить, как работает метод Post.__str__'
        )
