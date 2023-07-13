from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ResizedImage
from PIL import Image
import hashlib
import io
import os


def log_info(message):
    """
    Записывает информационное сообщение в лог.

    Args:
        message (str): Информационное сообщение.
    """
    # Определяем путь к файлу лога
    log_file_path = os.path.join(settings.BASE_DIR, 'image_hub.log')
    # Открываем файл в режиме добавления и записываем информацию
    with open(log_file_path, 'a') as f:
        f.write(f'INFO - {message}\n')


def log_error(message):
    """
    Записывает сообщение об ошибке в лог.

    Args:
        message (str): Сообщение об ошибке.
    """
    # Определяем путь к файлу лога
    log_file_path = os.path.join(settings.BASE_DIR, 'image_hub.log')
    # Открываем файл в режиме добавления и записываем информацию
    with open(log_file_path, 'a') as f:
        f.write(f'ERROR - {message}\n')


class ResizePictureView(APIView):
    """
    Класс представления для изменения размера изображения.
    """

    def post(self, request):
        """
        Обрабатывает POST-запрос для изменения размера изображения.

        Args:
            request (HttpRequest): POST-запрос.

        Returns:
            Response: Ответ API с информацией об измененном изображении или ошибкой.
        """
        # Получаем параметры ширины, высоты и файл изображения из запроса
        width = request.data.get('width')
        height = request.data.get('height')
        file = request.FILES.get('file')

        # Проверяем валидность параметров
        if not width or not file:
            return Response({'error': 'Invalid parameters'})

        try:
            width = int(width)
            if not height:
                height = width  # Если высота пустая, устанавливаем равной ширине
            else:
                height = int(height)
        except ValueError:
            return Response({'error': 'Invalid width or height'})

        # Вычисляем хеш от содержимого файла для уникального имени файла
        file_hash = hashlib.md5(file.read()).hexdigest()

        # Проверяем наличие уже созданного изображения с такими параметрами
        original_image = ResizedImage.objects.filter(width=width, height=height,
                                                     file_hash=file_hash).first()

        if original_image:
            # Если изображение уже было создано ранее, возвращаем сообщение пользователю
            return Response({'message': 'This image has already been resized.',
                             'image_url': original_image.file_path})

        try:
            # Создаем новое измененное изображение на основе переданных параметров
            image = Image.open(file)
            resized_image = image.resize((width, height))
            # Получаем размер изображения в байтах
            image_buffer = io.BytesIO()
            resized_image.save(image_buffer, format='JPEG')
            image_buffer.seek(0)
            image_size = len(image_buffer.getvalue())

            # Сохраняем измененное изображение
            modified_filename = f'{file_hash}_{width}x{height}.jpg'
            resized_image_path = os.path.join(settings.MEDIA_ROOT,
                                              '../media/resized_images',
                                              modified_filename)
            resized_image.save(resized_image_path)

            # Создаем запись об измененном изображении в базе данных
            original_image = ResizedImage(
                file_path=os.path.relpath(resized_image_path,
                                          settings.MEDIA_ROOT),
                file_hash=file_hash,
                size=image_size,
                width=width,
                height=height)
            original_image.save()

            image_url = reverse('image_hub:resized_image', args=[
                os.path.basename(original_image.file_path)])

            # Записываем информацию о созданном изображении в лог
            log_info(f'Image resized successfully: {image_url}')

            # Редирект на страницу с измененным изображением
            return redirect(image_url)

        except Exception as e:
            # Записываем ошибку в лог
            log_error(f'Error while resizing image: {str(e)}')
            return Response({'error': str(e)})

    def get(self, request):
        """
        Обрабатывает GET-запрос для отображения формы загрузки изображения.

        Args:
            request (HttpRequest): GET-запрос.

        Returns:
            HttpResponse: Ответ сервера с HTML-шаблоном для отображения формы загрузки изображения.
        """
        # Возвращаем шаблон HTML для отображения формы загрузки изображения
        return render(request, 'image_hub/resize_picture.html')


def resized_image_view(request, filename):
    """
    Обрабатывает запрос для отображения измененного изображения.

    Args:
        request (HttpRequest): Запрос.
        filename (str): Имя файла измененного изображения.

    Returns:
        HttpResponse: Ответ сервера с содержимым измененного изображения.
    """
    # Полный путь до измененного изображения
    image_path = os.path.join(settings.MEDIA_ROOT, 'resized_images', filename)

    # Открываем файл и считываем его контент
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Устанавливаем правильный Content-Type для изображения
    content_type = 'image/jpeg'  # Предполагая, что все измененные изображения в формате JPEG

    # Возвращаем контент изображения в HTTP-ответе
    return HttpResponse(image_data, content_type=content_type)
