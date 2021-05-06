from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class YaTbStaticPagesURLTests(TestCase):
    """Проверить статичные страницы 'об авторе' 'о технолоиях'."""
    def setUp(self):
        # Неавторизованый клиент
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Проверить доступность адреса /about/author/."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200,
            'Нужно проверить доступность страницы /about/author'
            'для неавторизованного пользователя'
        )

    def test_tech_url_exists_at_desired_location(self):
        """Проверить доступность адреса /about/tech/."""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200,
            'Нужно проверить доступность страницы /about/tech'
            ' для неавторизованного пользователя'
        )

    def test_about_url_uses_correct_template(self):
        """Проверить шаблон для адреса /about/author/.
        
        Для страницы 'about/author' должен применяться
        шаблон 'about/author.html'"""
        response = self.guest_client.get('/about/author/')
        self.assertTemplateUsed(response, 'about/author.html', 
            'Нужно проверить, что для страницы "/about/author"'
            ' используется шаблон "about/author.html"'
        )

    def test_tech_url_uses_correct_template(self):
        """Проверить шаблон для адреса /about/tech/.
        
        Для страницы '/about/tech' должен применяться
        шаблон 'about/tech.html'"""
        response = self.guest_client.get('/about/tech/')
        self.assertTemplateUsed(response, 'about/tech.html', 
            'Нужно проверить, что для страницы "/about/tech"'
            ' используется шаблон "about/tech.html"'
        )

class YatubeURLTests(TestCase):
    """Проверить работу шаблонов приложения posts по url-адресам"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для проверки доступности
        # адреса group/group-slug/
        cls.test_group = Group.objects.create(
            title='Тестовый заголовок группы',
            description='Тестовое описание группы',
            slug='test_slug'
        )
        cls.test_user = User.objects.create_user(
            username='user_test'
        )
        cls.test_post = Post.objects.create(
            author=cls.test_user,
            text='Тестовый текст для теста',
            group=cls.test_group
        )
        
        # Шаблоны по адресам
        cls.templates_url_names = {
            'posts/index.html': '/',
            'posts/group_index.html': '/group/',
            'posts/new_post.html': '/new/',
            'posts/group.html': '/group/test_slug/',
        }

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        #self.user = User.objects.create_user(username='user_test')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(YatubeURLTests.test_user)

    def test_user_login(self):
        Login = self.guest_client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('index'))
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 700)


        response = self.guest_client.get('/')
        self.assertTrue(response.user.is_authenticated)
        
        response = self.authorized_client.get('/')
        self.assertTrue(response.user.is_authenticated)
    
    def test_home_url_exists_at_desired_location(self):
        """Страница '/' доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_slug_url_exists_at_desired_location(self):
        """Страница 'group/slug' доступна любому пользователю."""
        response = self.guest_client.get('/group/test_slug/')
        self.assertEqual(response.status_code, 200)

    # Проверяем доступность страниц для авторизованного пользователя
    # Страница нового поста /new
    # method=GET
    def test_post_added_url_exists_at_desired_location(self):
        """Страница GET /new/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/new/')
        self.assertEqual(response.status_code, 200)

    # method=POST
    def test_post_added_url_with_method_post(self):
            """Страница POST /new/ доступна авторизованному пользователю."""
            response = self.authorized_client.post('/new/')
            self.assertEqual(response.status_code, 200)

    # Страница редактирования поста /<str:username>/<int:id>/edit
    # method=GET
    def test_post_edit_url_exists_at_desired_location(self):
        """Страница GET /username/id/edit доступна авторизованному юзеру."""
        response = self.authorized_client.get(
            f'/user_test/{YatubeURLTests.test_post.id}/edit'
        )
        self.assertEqual(response.status_code, 200)

    # method=POST
    def test_post_edit_url_with_method_post(self):
        """Страница POST /username/id/edit доступна авторизованному юзеру."""
        response = self.authorized_client.post(
            f'/user_test/{YatubeURLTests.test_post.id}/edit'
        )
        self.assertEqual(response.status_code, 302)

    # Проверяем редиректы для неавторизованного пользователя
    # Страница нового поста /new
    # method=GET
    def test_post_added_url_redirect_anonymous_get_method(self):
        """Страница GET /new/ перенаправляет анонимного пользователя."""
        response = self.guest_client.get('/new/')
        self.assertEqual(response.status_code, 301)
        self.assertRedirects(response, '/auth/login/?next=/new/')

    # method=POST
    def test_post_added_url_redirect_anonymous_post_method(self):
        """Страница POST /new/ перенаправляет анонимного пользователя."""
        response = self.guest_client.post('/new/')
        self.assertEqual(response.status_code, 301)
        self.assertRedirects(response, '/auth/login/?next=/new/')

    # Страница редактирования поста /<str:username>/<int:id>/edit
    # method=GET
    def test_post_added_url_redirect_anonymous_get_method(self):
        """Страница GET /username/id/edit перенаправляет анонимного юзера."""
        url = f'/user_test/{YatubeURLTests.test_post.id}/edit'
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 301)
        self.assertRedirects(response, '/auth/login/?next='+url)

    # method=POST
    def test_post_added_url_redirect_anonymous_post_method(self):
        """Страница POST /username/id/edit перенаправляет анонимного юзера."""
        response = self.guest_client.post(
            f'/user_test/{YatubeURLTests.test_post.id}/edit'
        )
        self.assertEqual(response.status_code, 301)
        self.assertRedirects(response, '/auth/login/?next=/'
            f'/user_test/{YatubeURLTests.test_post.id}/edit'
        )

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for template, adress in YatubeURLTests.templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)

class YatbTmplTests(TestCase):
    """Проверить работу шаблонов приложения posts через reverse()"""
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
        cls.templts_pgs_names = {
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
        for template, reverse_name in YatbTmplTests.templts_pgs_names.items():

            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
