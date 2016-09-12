import time

from django.contrib.auth.models import User, Group

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from expenses.models import Expense


class ItemsAPITestCase(APITestCase):
    list_link = '/expenses/items/'
    detail_link = '/expenses/item/{}/'

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testing_admin', password='123123')
        self.client.force_login(self.user)

    def test_expense_create(self):
        response = self.client.post(self.list_link)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_expense_update(self):
        item_data = self.client.post(self.list_link).json()
        item_data['text'] = 'testing_item'
        response = self.client.patch(
            self.detail_link.format(item_data['id']), item_data, format='json')
        self.assertEqual(response.json(), item_data)

    def test_expense_delete(self):
        item_data = self.client.post(self.list_link).json()
        response = self.client.delete(
            self.detail_link.format(item_data['id']))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UsersAPITestCase(APITestCase):
    list_link = '/expenses/users/'
    detail_link = '/expenses/user/{}/'

    def setUp(self):
        self.manager_user = User.objects.create(username='testing_user_manager', password='123123')
        manager_group = Group.objects.get(name='user_manager')
        self.manager_user.groups.add(manager_group)
        self.client.force_login(self.manager_user)

    def test_create_user(self):
        response = self.client.post(
            self.list_link, {'username': 'cat', 'password': 123}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_user(self):
        user_data = self.client.post(
            self.list_link, {'username': 'dog', 'password': 123}, format='json').json()
        user_data['username'] = 'dog1'
        response = self.client.put(
            self.detail_link.format(user_data['id']), user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_item_delete(self):
        user_data = self.client.post(
            self.list_link, {'username': 'dog1', 'password': 123}, format='json').json()
        response = self.client.delete(
            self.detail_link.format(user_data['id']))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# class E2ETestCase(APITestCase):
#     app_link = 'localhost:8000/expenses/'
#     username = 't1'
#     password = '123'
#
#     def setUp(self):
#         user = User.objects.create_user(username=self.username, password=self.password)
#         user.is_active = True
#         item = Expense.objects.create(text='bread', cost=10, user=user)
#         user.save()
#         self.user = user
#         self.driver = webdriver.Chrome()
#
#     def test_login(self):
#         self.driver.get(self.app_link)
#
#         username_input = self.driver.find_element_by_name('username')
#         username_input.send_keys(self.username)
#         password_input = self.driver.find_element_by_name("password")
#         password_input.send_keys(self.password)
#         login_button = self.driver.find_element_by_name("loginButton")
#         time.sleep(3)
#         login_button.click()
#         time.sleep(3)
#
#     def tearDown(self):
#         self.driver.close()
