FROM python:3.10

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV IS_PRODUCTION 1


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

CMD ["python3", "./manage.py", "collectstatic"]
CMD ["python3", "./manage.py", "runserver", "0.0.0.0:8000"]