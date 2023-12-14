# Triton Inference Server ASR

P.S.

This project is a test task. The goal of the project is to show how the problem can be approached. Quality and results have a lower priority

______________________________________

## Task

1. Triton Inference Server with ASR model (container)
2. FastAPI service, which processes the incoming audio, converts it to tensors, sends it to inference, and generates the response text. (container)
3. Telegram Bot. To record a voice message, we receive its transcript

______________________________________

### ML Design

![ml_design](https://github.com/2Bye/mlops_asr/assets/45552093/30251b35-92b9-4ef8-99cb-04c05cc054d3)

______________________________________

### ML System design

![system_design](https://github.com/2Bye/mlops_asr/assets/45552093/28240199-26f0-4918-8589-b2121b174f82)

______________________________________

### Start

#### Triton Inference Server

You can create Triton Inference Server with command:

```
docker run -it --rm --detach -p 8000:8000 -p 8001:8001 -p 8002:8002 -v "$PWD"/model_repository:/models nvcr.io/nvidia/tritonserver:23.07-py3 tritonserver --model-repository=/models
```

### Container for FastAPI

Using DockerFile inside the project run the command

```
docker build -t fastapi_container .
```

<!-- #region -->
### Start Container for FastAPI and Triton Inference Server

To run containers, follow these steps:

1. Launching the container for FastAPI

```
docker run --name fastapi_tg --rm --detach --network host fastapi_container:latest
```

2. Launching the container for Triton

```
docker run --name triton --rm --detach --network host -v "$PWD"/model_repository:/models nvcr.io/nvidia/tritonserver:23.07-py3 tritonserver --model-repository=/models
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
______________________________________

### Quick Start

To quickly start the service, run the bash script

```sh start.sh```

______________________________________

### What can be improved or fixed

1. Add logging in each module.
2. Do not write an audio file to disk at the Telegram stage and at the FastAPI stage. I wrote them down for debugging.
3. Write tests/unit-tests
4. Reduce the size of the docker image for services (delete the cache for example)
5. Perhaps there are more competent ways to extract the necessary modules from the ASR model
(file: fast_api_module/utils/ASR_modules.py, function: get_modules)
6. Reduce Requirers for FastAPI
7. You can use guvicorn instead of uvicorn
8. Make another newt server for CTCDecoder to extract text
