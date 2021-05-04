import sys, os, unittest
from django.test import TestCase, Client

sys.path.append(os.path.abspath('../../posts'))
from .models import Group, Post


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        test_group = Group
        test_group.title = 'test group name'
        test_post = Post
        test_post.text = 'test text for test post'


    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass
        

    def test_return_str_group(self):
        
        self.assertEqual(test_group.str, 'test group name')

    def test_return_str_post(self):
        
        self.assertEqual(test_post.str, 'test text for t')

