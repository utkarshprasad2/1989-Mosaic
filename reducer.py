from PIL import Image
from flask import Flask, request, make_response, jsonify
import requests
import math
import numpy as np

app = Flask(__name__)

mg = "http://127.0.0.1:4014/reduceMosaic"

middleware_server = "http://127.0.0.1:5000"

test_server = "http://sp23-cs340-adm.cs.illinois.edu:1989/"
my_url = "http://sp23-cs340-114.cs.illinois.edu:4014/reduceMosaic"

r = requests.put(f"{middleware_server}/registerReducer", data={
    "name": "reducer",
    "url" : mg,
    "author" : "Utkarsh Prasad"})

app = Flask(__name__)

def reduce_helper(baseImage, mosaic1, mosaic2, renderedTileSize, tilesAcross, fileFormat):
    img_width = baseImage.width
    img_height = baseImage.height
    pixels_per_tile = img_width / tilesAcross
    tiles_down = math.floor(img_height / pixels_per_tile)

    mosaic_width = math.floor(tilesAcross * renderedTileSize)
    mosaic_height = math.floor(tiles_down * renderedTileSize)
    mosaic_reduction = Image.new('RGB', (mosaic_width, mosaic_height))

    i = 0
    while i < tiles_down:
        for j in range(tilesAcross):
            base = baseImage.crop((j * pixels_per_tile, i * pixels_per_tile, (j + 1) * pixels_per_tile, (i + 1) * pixels_per_tile))

            base_mean_color = np.array(base).mean(axis=0).mean(axis=0)

            mosaic1_tile = mosaic1.crop((j * renderedTileSize, i * renderedTileSize, (j + 1) * renderedTileSize, (i + 1) * renderedTileSize))
            mosaic1_tile_mean_color = np.array(mosaic1_tile).mean(axis=0).mean(axis=0)

            mosaic2_tile = mosaic2.crop((j * renderedTileSize, i * renderedTileSize, (j + 1) * renderedTileSize, (i + 1) * renderedTileSize))
            mosaic2_tile_mean_color = np.array(mosaic2_tile).mean(axis=0).mean(axis=0)

            if (np.linalg.norm(base_mean_color[:3] - mosaic1_tile_mean_color[:3])) > (np.linalg.norm(base_mean_color[:3] - mosaic2_tile_mean_color[:3])):
                mosaic_reduction.paste(mosaic2_tile, ((j * renderedTileSize), (i * renderedTileSize), (j * renderedTileSize) + renderedTileSize, (i * renderedTileSize) + renderedTileSize))
            else:
                mosaic_reduction.paste(mosaic1_tile, ((j * renderedTileSize), (i * renderedTileSize), (j * renderedTileSize) + renderedTileSize, (i * renderedTileSize) + renderedTileSize))
        i += 1

    mosaic_reduction.save(f"reduced_output.{fileFormat}")

@app.route("/reduceMosaic", methods=["POST"])
def reduce():
    try:
        Image.open((request.files['baseImage']).stream)
    except:
        return jsonify({"error": "Failed to open input image file"}), 422

    baseImage = Image.open(request.files["baseImage"]).convert("RGB")
    mosaic1 = Image.open(request.files["mosaic1"]).convert("RGB")
    mosaic2 = Image.open(request.files["mosaic2"]).convert("RGB")

    renderedTileSize = int(request.args.get("renderedTileSize"))
    tilesAcross = int(request.args.get("tilesAcross"))
    fileFormat = request.args.get("fileFormat")

    reduce_helper(baseImage, mosaic1, mosaic2, renderedTileSize, tilesAcross, fileFormat)
    
    with open(f"reduced_output.{fileFormat}", 'rb') as f:
        buffer = f.read()
    
    return make_response(buffer)