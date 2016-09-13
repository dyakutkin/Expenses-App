from django.contrib.auth.models import User, Group

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from expenses.models import Expense


class ItemsAPITestCase(APITestCase):
    list_link = '/expenses/'
    detail_link = '/expenses/{}/'

    def setUp(self):
        self.admin_user = User.objects.create(username='testing_admin', password='123123')
        self.admin_user.groups.add(Group.objects.get(name='admin'))
        self.client.force_login(self.admin_user)

        self.regular_user = User.objects.create_user(username='st', password='st')

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
        item_data = self.client.post(self.list_link, {'text': 'bread', 'cost': 10}).json()
        response = self.client.delete(
            self.detail_link.format(item_data['id']))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_expenses_permissions(self):
        expense = Expense.objects.create(user=self.regular_user, text='food', cost=66)

        self.client.force_login(self.admin_user)
        response = self.client.delete(self.detail_link.format(expense.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_regular_user_expenses_permissions(self):
        expense = Expense.objects.create(user=self.admin_user, text='fish', cost=666)

        self.client.force_login(self.regular_user)
        response = self.client.delete(self.detail_link.format(expense.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UsersAPITestCase(APITestCase):
    list_link = '/users/'
    detail_link = '/users/{}/'

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

    def test_delete_user(self):
        user_data = self.client.post(
            self.list_link, {'username': 'dog1', 'password': 123}, format='json').json()
        response = self.client.delete(
            self.detail_link.format(user_data['id']))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)