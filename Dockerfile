# В качестве среды исполнения используем Python runtime
FROM python:3.9-slim
# Указываем рабочую директорию для контейнера
WORKDIR /app
# Копируем файл с библиотеками в контейнер
COPY requirements.txt .
# Устанавливаем зависимости для python
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
# Копируем все файлы программы в контейнер
COPY . .
# Запускаем основной файл программы при запуске контейнера
CMD ["python", "main.py"]