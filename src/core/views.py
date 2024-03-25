from flask import Blueprint, render_template, request, jsonify, render_template_string
import math
import os

core = Blueprint('core', __name__)

def loadGallery():
    images_dir = os.path.join(os.getcwd(), 'src', 'static', 'images')
    print(images_dir)
    media_list = []

    for i, filename in enumerate(os.listdir(images_dir)):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            image_info = {
                "id": i,
                "title": filename.split('.')[0].replace('pexels-',''),
                "thumbnail": filename,
                "description": f"Description for {filename.split('.')[0]}",
                "url": 'sample_video.mp4'
            }

            media_list.append(image_info)

    return media_list

videos = loadGallery()

@core.route('/', methods=['GET'])
def index():
    per_page = 5
    total_pages = math.ceil(len(videos)/per_page)
    return render_template('index.html', 
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
    page = int(request.args.get('current_page'))
    per_page = int(request.args.get('per_page'))
    total_pages = int(request.args.get('total_pages'))

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_videos = videos[start_idx:end_idx]

    return render_template('video_list.html',videos=paginated_videos, current_page=page, per_page=per_page, total_pages=total_pages)