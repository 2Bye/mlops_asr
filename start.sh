### Build container from Dockerfile
docker build -t fastapi_container .
### Start FastAPI container
docker run --name fastapi_tg --rm --detach -p 5454:5454 --network host fastapi_container:latest
### Start Triton Inference Server
docker run --name triton --rm --detach --network host -p 8000:8000 -p 8001:8001 -p 8002:8002 -v "$PWD"/model_repository:/models nvcr.io/nvidia/tritonserver:23.07-py3 tritonserver --model-repository=/models
### Start Telegram Bot
python main.py
