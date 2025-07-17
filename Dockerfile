FROM python:3.9

WORKDIR /usr/app
COPY ./fuckWoffu.py ./
COPY ./src/*.py ./src/
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
CMD [ "python", "./fuckWoffu.py"]