from celery import task
from post_office import mail

@task
def test_task():
    mail.send('testemail.te1@gmail.com', 'from@example.com', template='Email verification')
