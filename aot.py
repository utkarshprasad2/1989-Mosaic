import os
from PIL import Image
from scipy import spatial
import numpy as np
from flask import Flask, request, jsonify, render_template, send_file
import requests
import math

app = Flask(__name__)

FLASK_RUN_HOST = "0.0.0.0"

mg = "http://127.0.0.1:4011/makeMosaic"

middleware_server = "http://127.0.0.1:5000"

test_server = "http://sp23-cs340-adm.cs.illinois.edu:1989/"
my_url = "http://sp23-cs340-114.cs.illinois.edu:4011/makeMosaic"

r = requests.put(f"{middleware_server}/addMMG", data={
    "name": "aot",
    "url" : mg,
    "author" : "Utkarsh Prasad",
    "tileImageCount" : 60})

@app.route('/', methods=["GET"])
def GET_index():
    '''Route for "/" (frontend)'''
    return render_template("index.html")

def is_image(filename):
    return filename.lower().endswith(('.png', '.jpeg', '.jpg'))

def makeMosaic(tiles_folder, tilesAcross, renderedTileSize, fileFormat):
    image_location = []
    image_pixels = []
    pixel_color = []

    renderedTileSize = int(renderedTileSize)
    tilesAcross = int(tilesAcross)

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
    tile_size = img_width / tilesAcross
    num_tiles_x = tilesAcross
    num_tiles_y = int(img_height / tile_size) 
    mosaic_width = int(renderedTileSize * num_tiles_x)
    mosaic_height = int(renderedTileSize * num_tiles_y)
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
            output_image.paste(image_pixels[index], (int(col_tile * renderedTileSize), int(row_tile * renderedTileSize)))

    output_file_name = f"output_{tiles_folder}.{fileFormat.lower()}"
    output_image.save(output_file_name)
    return output_file_name


@app.route('/makeMosaic', methods=["POST"])
def POST_makeMosaic():
    tilesAcross = int(request.args.get("tilesAcross"))
    renderedTileSize = int(request.args.get("renderedTileSize"))
    fileFormat = request.args.get("fileFormat")

    input_image = request.files.get("image")
    try:
        Image.open(input_image.stream)
    except:
        return jsonify({"error": "Failed to open input image file"}), 422

    output_aot = makeMosaic("aot", tilesAcross, renderedTileSize, fileFormat)

    return send_file(output_aot), 200