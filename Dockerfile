FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
RUN apt update && apt install -y libsm6 libxext6 libgl1-mesa-glx libpoppler-cpp-dev pkg-config
RUN apt-get -y install tesseract-ocr

COPY . /app
WORKDIR /app

RUN pip3 install pillow
RUN pip3 install pytesseract
RUN pip3 install opencv-python
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]
