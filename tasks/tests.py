from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Task


class TaskViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.task_data = {'title': 'Test Task', 'user_name': 'testuser'}

    def test_post_success(self):
        url = reverse('task-list')
        response = self.client.post(url, self.task_data)
        
        self.assertEqual(response.status_code, 201)

    def test_post_not_existing_user_name(self):
        url = reverse('task-list')
        task_data = {
            'title': self.task_data['title'],
            'user_name': 'non existing user name'
        }
        response = self.client.post(url, task_data)

        self.assertEqual(response.status_code, 400)


    def test_post_two_identical_tasks_for_same_user(self):
        url = reverse('task-list')
        self.client.post(url, self.task_data)
        response = self.client.post(url, self.task_data)

        self.assertEqual(response.status_code, 400)

    def test_get_request(self):
        task_data = {
            **self.task_data,
            'created_by': self.user
        }
        Task.objects.create(**task_data)
        url = reverse('task-list')
        response = self.client.get(url)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_delete_request(self):
        task_data = {
            **self.task_data,
            'created_by': self.user
        }
        task = Task.objects.create(**task_data)
        url = reverse('task-detail', kwargs={'pk': task.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

    def test_update_entire_object_request(self):
        task_data = {
            **self.task_data,
            'created_by': self.user
        }
        task = Task.objects.create(**task_data)
        url = reverse('task-detail', kwargs={'pk': task.id})
        updated_task_data = {'title': 'some other title', 'user_name': 'testuser'}
        response = self.client.put(url, updated_task_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], task.id)
        self.assertEqual(response.data['title'], updated_task_data['title'])
        self.assertEqual(response.data['user_name'], updated_task_data['user_name'])

    def test_update_object_partially_request(self):
        task_data = {
            **self.task_data,
            'created_by': self.user
        }
        task = Task.objects.create(**task_data)
        url = reverse('task-detail', kwargs={'pk': task.id})
        updated_task_data = {'title': 'some other title'}
        response = self.client.patch(url, updated_task_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], task.id)
        self.assertEqual(response.data['title'], updated_task_data['title'])
        self.assertEqual(response.data['user_name'], task.user_name)
