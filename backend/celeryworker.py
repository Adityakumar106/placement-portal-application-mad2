from celery import Celery

from App import app as flask_app

celery = Celery("placement_portal")

celery.config_from_object("celeryconfig")


class FlaskTask(celery.Task):

    def __call__(self, *args, **kwargs):

        with flask_app.app_context():

            return self.run(*args, **kwargs)


celery.Task = FlaskTask

app = celery

import tasks
