from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import subprocess
import os
from filelock import FileLock
import time

lock = FileLock("my_file.lock")
app = Flask(__name__)

output_dir = 'E:\\MachVis\\GLPDepth-main\\code\\results\\test'  # update this with your actual output images directory path

@app.route('/')
def home():
    return render_template('page2.html')  

@app.route('/select_directory', methods = ['POST'])
def select_directory():
    return render_template('page3.html')

@app.route('/run_script' , methods = ['POST'])
def run_script():
    if request.method == 'POST':
        file = request.files['file']
        directory_name = os.path.dirname(file.filename)
        subprocess.Popen(['python', './code/test.py', '--dataset', 'imagepath', 
                        '--data_path', './code/'+directory_name, '--save_visualize'])
        time.sleep(8)
        with lock:
            global original_dir
            original_dir = 'E:\\MachVis\\GLPDepth-main\\code\\'+directory_name  # update this with your actual original images directory path
            original_images = set(os.listdir(original_dir))
            all_output_images = os.listdir(output_dir)
            new_output_images = [img for img in all_output_images if img in original_images]
            image_pairs = [(img, img) for img in new_output_images] #This line is used to find the pair of images with the same name
    return render_template('page4.html', image_pairs = image_pairs)

@app.route('/original_images/<filename>')
def serve_original_image(filename):
    global original_dir
    return send_from_directory(original_dir, filename)

@app.route('/run_script/<filename>')
def serve_output_image(filename):
    return send_from_directory(output_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)


