# 🖼️ 1989 Mosaics Project

Welcome to the 1989 Mosaics Project! This project is a creative implementation of a mosaic generator using Python and Flask, inspired by Taylor Swift's "1989" album. The mosaic generator utilizes a MapReduce-based design to create stunning mosaics from a collection of images. This README provides an overview of the project and highlights the key skills developed during its creation.

# 🎯 Project Overview

The 1989 Mosaics project was developed as part of CS 340: Introduction to Computer Systems. The goal was to experience developing a small but integral part of a complex software system. The project features:
- Microservice-Based Design: Each student contributed multiple backend microservices.
- Simultaneous Microservices: All microservices run simultaneously during deployment.
- Collaborative Components: Middleware, frontend, and other components were designed collaboratively.

Project Highlights
- 13 Microservice Mosaic Generators (MMGs): Each MMG includes at least 60 unique tile images.
- Mosaic Reducer: A reducer that takes two mosaics and finds the best possible tile for each tile in the mosaic.
- Creative Themes: The mosaics were inspired by personal interests, such as Attack on Titan, nature, friends, and more.

# 🛠️ Skills Learned
1. Python Programming 🐍
- Image Processing: Used the Pillow (PIL) library for image manipulation and processing.
- Data Structures: Managed arrays and data structures to handle image data efficiently.
- Algorithm Development: Implemented the MapReduce algorithm for mosaic generation.
2. Flask Web Framework 🌐
- Web Application Development: Created a web interface for uploading images and displaying mosaics.
- Routing and Request Handling: Managed HTTP requests and defined routes for different functionalities.
- Template Rendering: Used Jinja2 templates to render HTML pages dynamically.
3. Image Processing and Manipulation 🖌️
- Image Resizing and Cropping: Manipulated images to fit into the mosaic tiles.
- Color Analysis: Calculated mean colors of images for accurate tile placement.
Spatial Data Structures: Utilized KD-Trees from SciPy for efficient nearest-neighbor searches.
4. Web Development (Frontend) 🎨
- HTML & CSS: Developed the frontend interface for user interactions.
- JavaScript: Handled client-side scripting for dynamic content updates.
- Bootstrap: Styled the web application for a responsive design.
5. File Handling and I/O 📁
- File Uploads: Managed image file uploads from users.
- File System Navigation: Read and processed images from directories.
- Data Encoding: Encoded images in Base64 for web display.
6. Problem-Solving & Debugging 🐞
- Error Handling: Identified and fixed issues related to image processing and data handling.
- Optimization: Improved the performance of the mosaic generation algorithm.
- Testing: Tested the application to ensure reliability and correctness.
7. Collaboration & Integration 🤝
- Microservices Integration: Worked on integrating individual microservices into the larger system.
- Version Control: Used Git and GitHub for code management and collaboration.
- Communication: Coordinated with peers to align on project goals and infrastructure.

📋 Features in Detail
Mosaic Generation 🧩
- Multiple Themes: Generate mosaics using various image sets like Attack on Titan, nature, friends, and more.
- MapReduce Algorithm: Efficiently processes large numbers of images to create high-quality mosaics.
- Custom Tile Sizes: Adjust the number of tiles across and rendered tile sizes for different mosaic resolutions.
Web Interface 🌐
- User-Friendly Design: Simple interface to upload images and display results.
- Dynamic Content: Displays multiple mosaic outputs on the same page.
- Image Previews: Shows generated mosaics directly in the browser using Base64 encoding.
Code Structure 🗂️
- Modular Design: Organized code into functions for readability and maintenance.
- Error Handling: Includes checks for valid image files and handles exceptions gracefully.
- Comments and Documentation: Well-documented code for understanding and future development.