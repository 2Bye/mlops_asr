# Triton Inference Server ASR

P.S.

This project is a test task. The goal of the project is to show how the problem can be approached. Quality and results have a lower priority

## Requirements

1. Triton Inference Server with ASR model (container)
2. FastAPI service, which processes the incoming audio, converts it to tensors, sends it to inference, and generates the response text. (container)
3. Telegram Bot. To record a voice message, we receive its transcript

### ML Design

![Service_ASR-2](https://github.com/2Bye/mlops_asr/assets/45552093/f9b63b88-a56e-41e5-a191-350c256b1fa2)

______________________________________

### ML System design

![Service_ASR_more-2](https://github.com/2Bye/mlops_asr/assets/45552093/a38b723e-cfa1-48e3-bcd0-ccdeca4d3c05)

### Start

#### Triton Inference Server

You can create Triton Inference Server with command:

```
docker run -it --rm --detach -p 8000:8000 -p 8001:8001 -p 8002:8002 -v "$PWD"/model_repository:/models nvcr.io/nvidia/tritonserver:23.07-py3 tritonserver --model-repository=/models
```

If everything is fine, then you will see similar screen

<img width="768" alt="image" src="https://github.com/2Bye/mlops_asr/assets/45552093/be077ab5-a7e7-43d3-a765-f7a9c5180db4">


### Container for TG and FastAPI

Using DockerFile inside the project run the command

```
docker build -t fastapi_container .
```

<!-- #region -->
### Start Container for FastAPI and Triton Inference Server

To run containers, follow these steps:

1. Launching the container for FastAPI

```
docker run --name fastapi_tg --rm --detach -p 5454:5454 --network host fastapi_container:latest
```

2. Launching the container for Triton

```
docker run --name triton --rm --detach --network host -p 8000:8000 -p 8001:8001 -p 8002:8002 -v "$PWD"/model_repository:/models nvcr.io/nvidia/tritonserver:23.07-py3 tritonserver --model-repository=/models
```

#### Start Telegram Bot

You need to create a **config.py** file in the **telegram_bot** folder. An example of a config is in the same place: **telegram_bot/config_example.py**

1. Need to install packages

```
pip install -r req_for_tg.txt
```

2. Next from the root run

```
python main.py
```

### Quick Start

To quickly start the service, run the bash script

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
