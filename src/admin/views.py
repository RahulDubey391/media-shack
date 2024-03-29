from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_required, current_user
from src import db, app
from src.models import MediaPost
from src.admin.forms import AddContentForm
from src.admin.decorator import admin_required
from werkzeug.utils import secure_filename
import os

from PIL import Image
from io import BytesIO

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/add_content', methods=['GET', 'POST'])
@login_required
@admin_required
def add_content():
    form = AddContentForm()
    if form.validate_on_submit():
        thumbnail_file = form.thumbnail.data
        if thumbnail_file:
            # Open the uploaded image file
            image = Image.open(thumbnail_file)
            
            # Set the desired width and height for resizing
            desired_width = 300
            desired_height = 200
            
            # Resize the image
            image.thumbnail((desired_width, desired_height))
            
            # Convert the resized image to bytes
            image_bytes = BytesIO()
            image.save(image_bytes, format='JPEG')  # You can change the format as needed
            
            # Save the resized image to the server
            filename = secure_filename(thumbnail_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(filepath, 'wb') as f:
                f.write(image_bytes.getvalue())
            
            # Get the URL of the resized image
            thumbnail_url = url_for('static', filename='uploads/' + filename)
        else:
            thumbnail_url = None

        new_post = MediaPost(
            content_id=form.content_id.data,
            user_id=current_user.id,
            content_title=form.content_title.data,
            thumbnail_url=thumbnail_url,
            video_url=form.video_url.data
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Content added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_content.html', form=form)

