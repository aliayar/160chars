from rq import get_current_job
from app import create_app
from app.models import Task
from flask import render_template
from app.email import send_mail
import sys
import json

app = create_app()
app.app_context().push()

def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification('task_progress', {'task_id': job.get_id(),
                                                    'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()


def export_posts(user_id):
    try:
        user = User.query.get(user_id)
        _set_task_progress(0)
        data = []
        i = 0
        total_posts = user.posts.count()
        for post in user.posts.order_by(Post.timestamp.asc()):
            data.append({'body': post.body,
                        'timestamp': post.timestamp.isoformat() + 'Z'})
            time.sleep(5)
            i += 1
            _set_task_progress(100 * i // total_posts)
        send_email('[160Chars] Your blog posts',
                    sender=app.config['ADMINS'][0], recipients=[user.email],
                    text_body=render_template('email/export_posts.txt', user=user),
                    html_body=render_template('email/export_posts.html', user=user),
                    attachments=[('posts_json', 'application/json',
                                json_dumps({'posts: data'}, indent=4))],
                                sync=True)
    except:
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    finally:
        _set_task_progress(100)