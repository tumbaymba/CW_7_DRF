FROM python:3

WORKDIR /CW_7_DRF

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .