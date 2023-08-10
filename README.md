# Triton Inference Server ASR

P.S.

This project is a test task. The goal of the project is to show how the problem can be approached. Quality and results have a lower priority

## Requirements

1. Triton Inference Server with ASR model (container)
2. FastAPI service, which processes the incoming audio, converts it to tensors, sends it to inference, and generates the response text. (container)
3. Telegram Bot. To record a voice message, we receive its transcript

### ML Design

![image.png](attachment:image.png)

______________________________________

### ML System design

![image-3.png](attachment:image-3.png)


### Start

#### Triton Inference Server

You can create Triton Inference Server with command:

```
docker run -it --rm --detach -p 8000:8000 -p 8001:8001 -p 8002:8002 -v "$PWD"/model_repository:/models nvcr.io/nvidia/tritonserver:23.07-py3 tritonserver --model-repository=/models```


If everything is fine, then you will see similar screen

![image.png](attachment:image.png)

#### Container for TG and FastAPI

Используя DockerFile внутри проекта запутить команду

```docker build -t fastapi_container .```

<!-- #region -->
#### Start Container for FastAPI and Triton Inference Server

Для того чтобы запустить контейнеры нужно выполнить следующие действия


1. Запускаем котейнер для FastAPI

```docker run --name fastapi_tg --rm --detach -p 5454:5454 --network host fastapi_container:latest```

2. Запускаем Тритон

```docker run --name triton --rm --detach --network host -p 8000:8000 -p 8001:8001 -p 8002:8002 -v "$PWD"/model_repository:/models nvcr.io/nvidia/tritonserver:23.07-py3 tritonserver --model-repository=/models```

#### Start Telegram Bot

Нужно создать файл **config.py** в папке **telegram_bot**. Пример конфига лежит там же : **telegram_bot/config_example.py**

1. Нужно установить пакеты

```pip install -r req_for_tg.txt```

2. Далее из корня запустить

```python main.py```

### Quick Start

Для быстрого запуска сервиса запустите баш скрипт

```sh start.sh```
<!-- #endregion -->

### Что можно улучшить исправить и тд

1. Добавить логгирование в каждом модуле. 
2. Если Телеграм и ФастАПИ будут находится в одном сервисе (как у меня), то можно не писать на диск аудиофайл на этапе Телеграма и на этапе ФастАПИ. Я записывал их для отладки. 
3. Написать тесты/unit-tests
4. Уменьшить размеры docker image для сервисов (удалить кеш например)
5. Возможно есть способы более грамотные для извлечения нужных модулей из ASR модели 
(файл : fast_api_module/utils/ASR_modules.py, функция : get_modules)
6. Сократить Рекваеры для FastAPI
7. Пробовал собрать докер вместе с Телеграмом. Докер собирается, однако run uvicorn у меня не работал. Были проблемы с Соединением к FastAPI серверу. Поэтому остановился на варианте, который описан в репозитории

DockerFile для билда одного контейнера с телегой
```
FROM python:3.8.11-bullseye
WORKDIR app
COPY fast_api_module .
RUN pip install -r requirements.txt
EXPOSE 5454
CMD [ "python", "main.py"]
```

8. Можно использовать guvicorn вместо uvicorn

```python

```
