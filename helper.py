import random
import string
from flask import Flask, flash, redirect, request
import os
from werkzeug.utils import secure_filename
def generate_product_code(prefix, length=6):
    characters = string.ascii_uppercase + string.digits
    unique_id = ''.join(random.choice(characters) for _ in range(length))
    return f"{prefix}-{unique_id}"

def allowed_file(app, filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def upload_file(app: Flask, file):
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(app, file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        return file_path
    else:
        return False