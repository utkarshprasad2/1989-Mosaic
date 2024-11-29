First, I created some empty lists to store information. image_location will store the location of all the images in the tiles_folder image_pixels will store the pixels of each image after they have been resized, and pixel_color will store the average color of each image after they have been resized.

Next, I looped through all the images in the tiles_folder and added their location to the image_location list. If the current image is an actual image file (as opposed to a system file or something else), I opened it using a function I made, resized it, added the resized image pixels to image_pixels, and calculated its average color, which was added to pixel_color.

Then, I opened the mosaic image that the user uploaded and got its width and height. I calculated the size of each tile based on how many tiles across (tiles_across) the user wants in the final mosaic, and figured out how many tiles there will be vertically (num_tiles_y). I also resized the mosaic image to be the correct size based on the tile size and number of tiles (rendered).

Next, I created a KDTree object to store the average color of each image from the pixel_color list. Then, I looped through each tile in the mosaic, found the average color of that tile, and used the KDTree to find the closest matching image. The index of that image was stored in the color_result list.

Finally, I created a new image to hold the final mosaic (output_image), and looped through each tile in the mosaic again. For each tile, I got the corresponding index from color_result and pasted the corresponding resized image from image_pixels onto the output image. I then returned the image and saved it locally so I could look at it for debugging purposes.

Currently, when python3 -m run flask is run, the server will be running on port 5000. Each folder has an app.py file that gets run when this is called through the script in the main app.py file, and then when the user makes a request to the server, the app.py file in the folder that corresponds to the request is run. The app.py file in each folder contains the routes for that microservice.

The following routes are available:
/family_app
/friends_app
/girlfriend_app
/illinois_app
/fizaa_app

The request must include a JSON payload containing the following information:

name: The name of the microservice (e.g., "fizaa", "illinois", "family", "friends", "girlfriend").
tiles_folder: The path to the folder containing the tile images for the microservice.
tiles_across: The number of tiles to use across the width of the mosaic.
tile_size: The size (in pixels) to use for each tile in the mosaic.