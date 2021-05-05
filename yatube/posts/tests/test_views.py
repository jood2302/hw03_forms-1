from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class YatbPgsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим записи в БД:
        cls.group = Group.objects.create(
            title='Тестовая подборка записей',
            description='Тестирующая шаблоны подборка',
            slug='test-slug',
        )

        cls.test_post = Post.objects.create(
            author=User.objects.create(username='Test_user'),
            text='Проверочный текст для тестового поста',
            group=cls.group
        )
        cls.post_count = Post.objects.all().count()

        # Собираем в словарь пары "имя_html_шаблона: name"
        cls.templts_pags_names = {
            'posts/index.html': reverse('index'),
            'posts/group_index.html': reverse('group_index'),
            'posts/new_post.html': reverse('new_post'),
            'posts/group.html': (
                reverse('group', kwargs={'slug': 'test-slug'})
            ),
            'posts/profile.html': (
                reverse('profile', kwargs={'username': 'Test_user'})
            ),
            'posts/post.html': (
                reverse('post',
                        kwargs={'username': 'test_user',
                                'post_id': cls.post_count})
            ),
        }

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='CoherentuS')
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем используемые шаблоны
    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Проверяем, что при обращении к name вызывается
        # соответствующий HTML-шаблон
        for template, reverse_name in YatbPgsTests.templts_pags_names.items():

            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


class YaTbPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.COUNT_ITEMS_FOR_PAGINATOR = 10
        # Создаём записи в БД
        # Групп > 2.5 страницы пагинатора
        for i in range(1, int(cls.COUNT_ITEMS_FOR_PAGINATOR * 2.5 + 1) + 1):
            cls.group = Group.objects.create(
                title='Тестовая подборка записей №' + str(i),
                description='Тестирующая контекст подборка №' + str(i),
                slug='test-slug' + str(i),
            )
            cls.group.save()

        # Постов > 5.5 страницы пагинатора
        for i in range(1, int(cls.COUNT_ITEMS_FOR_PAGINATOR * 5.5 + 1) + 1):
            cls.test_post = Post.objects.create(
                author=User.objects.create(username='Test_user' + str(i)),
                text='Проверочный текст для поста проверки контекста' + str(i),
            )
            # каждый третий пост без группы
            tmp_ind_div3 = (i + 2) % 3
            if tmp_ind_div3:
                group = Group.objects.get(id=tmp_ind_div3)
                cls.test_post.group = group
            cls.test_post.save()

        cls.post_count = Post.objects.all().count()

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='CoherentuS')
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверка словаря контекста главной страницы
    def test_index_page_shows_correct_context(self):
        """Шаблон index сформирован с правильным контекстом.

        Ожидаемый контекст должен содержать словарь page с кол-вом постов,
        прописанным при конструировании paginator-а. Посты должны содержать
        поля post.author post.text post.group . Показ всего содержимого
        'index' не требует и не зависит от авторизации пользователя.
        На метод "POST" не реагирует.
        """
        response = self.authorized_client.get(reverse('index'))
        posts_per_page = response.context.get('page').object_list
        self.assertEqual(len(posts_per_page),
                         YaTbPagesTests.COUNT_ITEMS_FOR_PAGINATOR)
        """Количество постов, выводимых на странице равно пагинатору"""

        for post in posts_per_page:
            """self.assertEqual(post.text, ):
            self.assertEqual(, ):
            self.assertEqual(post.group, ):"""
            self.assertTrue(post.author.get_full_name in response.context)
            self.assertTrue(post.text in response.context)
            self.assertTrue(post.group in response.context)

