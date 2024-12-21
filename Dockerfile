FROM python:3.12

RUN mkdir /code

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN playwright install \
    && playwright install-deps

CMD ["pytest"]