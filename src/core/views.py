from flask import Blueprint, render_template, request, jsonify, render_template_string
from src.models import MediaPost
from flask import current_app
from src import app
import math
import os

core = Blueprint('core', __name__)

def loadGallery(page, per_page):
    media_list = []

    with app.app_context():
        # Calculate the start and end indices for pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page

        # Query MediaPost objects from the database with pagination
        media_posts = MediaPost.query.offset(start_idx).limit(per_page).all()

        for post in media_posts:
            # Assuming thumbnail_url is the field in MediaPost representing the image thumbnail
            image_info = {
                "id": post.content_id,
                "title": post.content_title,
                "thumbnail": post.thumbnail_url.split('/')[-1],
                "description": f"Description for {post.content_title}",
                "url": post.video_url
            }
            media_list.append(image_info)

    return media_list

@core.route('/', methods=['GET'])
def index():
    per_page = 5
    total_pages = math.ceil(MediaPost.query.count() / per_page)
    current_page = int(request.args.get('page', 1))

    videos = loadGallery(current_page, per_page)
    return render_template('index.html',
                           videos=videos,
                           total_pages=total_pages, 
                           per_page=per_page, 
                           current_page=1)

@core.route('/about',methods=['GET'])
def about():
    return render_template('about.html')

@core.route('/vidplayer')
def getVidPlayer():
    title = request.args.get('video_name')
    url = request.args.get('url')
    return render_template('video_player.html', video=title, url=url)

@core.route('/page')
def getPage():
    per_page = int(request.args.get('per_page'))
    total_pages = math.ceil(MediaPost.query.count() / per_page)
    current_page = int(request.args.get('current_page', 1))

    paginated_videos = loadGallery(current_page, per_page)

    return render_template('video_list.html', 
                           videos=paginated_videos, 
                           current_page=current_page, 
                           per_page=per_page, 
                           total_pages=total_pages)