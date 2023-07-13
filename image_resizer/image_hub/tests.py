from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import ResizedImage
import os


class ResizePictureViewTestCase(TestCase):
    '''
    Тест-кейс для приложения image_hub
    '''
    def test_resize_picture_view_with_valid_parameters(self):
        # Создание тестовых данные
        folder_path = '../media/resized_images/'
        image_files = [file for file in files if
                       file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        first_image = image_files[0]
        first_image_path = os.path.join(folder_path, first_image)

        image = first_image_path
        width = 200
        height = 300

        # Отправка POST-запроса на URL-адрес, соответствующий представлению
        response = self.client.post(
            reverse('image_hub:resize_picture'),
            data={'width': width, 'height': height, 'file': image},
            format='multipart'
        )

        # Проверка, что ответ имеет ожидаемый статус код
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        # Проверка, что запись об измененном изображении была создана в базе данных
        resized_image = ResizedImage.objects.last()
        self.assertIsNotNone(resized_image)
