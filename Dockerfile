# syntax=docker/dockerfile:1
FROM python
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src /code/src
COPY ./database /code/database
COPY ./main.py /code/main.py
CMD uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000} --reload --ws websockets
EXPOSE 5000