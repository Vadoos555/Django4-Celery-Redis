# tasks.py
from celery import shared_task
from web_app.celery import app


@shared_task()
def show_task1():
    print('this is 1 task for celery')


@app.task
def add(x, y):
    return x + y


@app.task
def multiply(x, y):
    return x * y


@shared_task()
def mult_3(x, y, z):
    return x * y * z