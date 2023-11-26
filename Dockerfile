FROM python:3.9

WORKDIR /usr/app/src
COPY . ./
RUN pip install -r requirements.txt
CMD [ "python", "./fuckWoffu.py"]