FROM python:3

COPY stream.py /usr/src/myapp/

RUN pip install requests

WORKDIR /usr/src/myapp/

CMD ["python3", "stream.py"]