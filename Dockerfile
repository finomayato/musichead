FROM python:3.7
COPY Makefile /Makefile
COPY requirements.txt /requirements.txt
COPY core /core
RUN pip install -r requirements.txt
CMD make run