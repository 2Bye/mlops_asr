FROM python:3.8.11-bullseye
WORKDIR app
RUN apt update && apt install -y ffmpeg
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY fast_api_module .
# EXPOSE 5454
# CMD [ "python", "main.py"]
CMD uvicorn fast_api_server:app --port=5454 --host=0.0.0.0