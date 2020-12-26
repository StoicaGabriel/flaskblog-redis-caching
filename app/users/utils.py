import os
import secrets
import inspect
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f'{random_hex}{f_ext}'
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        subject='Password Reset Request',
        sender='noreply@demo.com',
        recipients=[user.email]
    )
    msg.body = inspect.cleandoc(
        f"""To reset your password, visit the following link:
        {url_for('users.reset_token', token=token, _external=True)}

        If you did not request this email, you can simply ignore this email.
        You should consider changing your password.
        """
    )
    # TODO: this ain't working since the email and password env vars are not set
    mail.send(message=msg)
