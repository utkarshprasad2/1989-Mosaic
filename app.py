import os
from PIL import Image
from scipy import spatial
import numpy as np
import base64
from flask import Flask, request, jsonify, render_template, url_for

app = Flask(__name__)

@app.route('/', methods=["GET"])
def GET_index():
    '''Route for "/" (frontend)'''
    return render_template("index.html")


def is_image(filename):
    return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))  

def makeMosaic(tiles_folder, tilesAcross, renderedTileSize, f):
    image_location = []
    image_pixels = []
    pixel_color = []

    for image_file in os.listdir(tiles_folder):
        image_location.append(os.path.join(tiles_folder, image_file))
        
    for location in image_location:
      if is_image(location):
        image = Image.open(location)
        resized_image = image.resize((renderedTileSize, renderedTileSize))
        image_pixels.append(resized_image)
        mean_color = np.array(resized_image).mean(axis=0).mean(axis=0)
        pixel_color.append(mean_color)

    mosaic_image = Image.open(request.files["image"])
    img_width, img_height = mosaic_image.size
    tile_size = int(img_width / tilesAcross)
    num_tiles_x = tilesAcross
    num_tiles_y = int(img_height / tile_size)
    mosaic_width = tile_size * num_tiles_x
    mosaic_height = tile_size * num_tiles_y
    color_kd_tree = spatial.KDTree(pixel_color)
    color_result = np.zeros((num_tiles_x, num_tiles_y), dtype=np.uint32)

    for row_tile in range(num_tiles_y):
        for col_tile in range(num_tiles_x):
            x1 = col_tile * tile_size
            y1 = row_tile * tile_size
            x2 = x1 + tile_size
            y2 = y1 + tile_size
            tile_region = (x1, y1, x2, y2)
            tile_image = mosaic_image.crop(tile_region)
            color = color_kd_tree.query(np.array(tile_image).mean(axis=0).mean(axis=0))
            color_result[col_tile, row_tile] = color[1]

    output_image = Image.new('RGB', (mosaic_width, mosaic_height))

    for row_tile in range(num_tiles_y):
        for col_tile in range(num_tiles_x):
            index = color_result[col_tile, row_tile]
            output_image.paste(image_pixels[index], (col_tile * tile_size, row_tile * tile_size))

    output_file_name = f"output_{tiles_folder}.jpg"
    output_image.resize((img_width, img_height)).save(output_file_name)
    return url_for('static', filename=output_file_name)

@app.route('/makeMosaic', methods=["POST"])
def POST_makeMosaic():

    f = request.files["image"]
    output_fizaa = makeMosaic("fizaa", 200, 32, f)
    output_illinois = makeMosaic("illinois", 200, 32, f)
    output_family = makeMosaic("family", 200, 32, f)
    output_friends = makeMosaic("friends", 200, 32, f)
    output_girlfriend = makeMosaic("girlfriend", 200, 32, f)
    output_dance = makeMosaic("dance", 200, 32, f)
    output_nature = makeMosaic("nature", 200, 32, f)
    output_taylorswift = makeMosaic("taylorswift", 200, 32, f)
    output_tigers = makeMosaic("tigers", 200, 32, f)


    response = []
    with open("output_fizaa.jpg", "rb") as f:
      buffer = f.read()
    b64 = base64.b64encode(buffer)
    response.append({
      "image": "data:image/png;base64," + b64.decode('utf-8')
    })

    with open("output_tigers.jpg", "rb") as f:
      buffer = f.read()
    b64 = base64.b64encode(buffer)
    response.append({
      "image": "data:image/png;base64," + b64.decode('utf-8')
    })

    with open("output_taylorswift.jpg", "rb") as f:
      buffer = f.read()
    b64 = base64.b64encode(buffer)
    response.append({
      "image": "data:image/png;base64," + b64.decode('utf-8')
    })

    with open("output_dance.jpg", "rb") as f:
      buffer = f.read()
    b64 = base64.b64encode(buffer)
    response.append({
      "image": "data:image/png;base64," + b64.decode('utf-8')
    })

    with open("output_nature.jpg", "rb") as f:
      buffer = f.read()
    b64 = base64.b64encode(buffer)
    response.append({
      "image": "data:image/png;base64," + b64.decode('utf-8')
    })

    with open("output_illinois.jpg", "rb") as f:
      buffer = f.read()
    b64 = base64.b64encode(buffer)
    response.append({
      "image": "data:image/png;base64," + b64.decode('utf-8')
    })

    with open("output_friends.jpg", "rb") as f:
      buffer = f.read()
    b64 = base64.b64encode(buffer)
    response.append({
      "image": "data:image/png;base64," + b64.decode('utf-8')
    })

    with open("output_family.jpg", "rb") as f:
      buffer = f.read()
    b64 = base64.b64encode(buffer)
    response.append({
      "image": "data:image/png;base64," + b64.decode('utf-8')
    })

    with open("output_girlfriend.jpg", "rb") as f:
      buffer = f.read()
    b64 = base64.b64encode(buffer)
    response.append({
      "image": "data:image/png;base64," + b64.decode('utf-8')
    })

    return jsonify(response)