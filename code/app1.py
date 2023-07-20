from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from celery import Celery
import subprocess
import os
from filelock import FileLock
import time

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'  # Replace with your Redis URL
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'  # Replace with your Redis URL

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

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
        task = long_running_task.delay(directory_name)
        return render_template('page4.html', task_id = task.id)  # Pass task id to template

@celery.task(bind=True)
def long_running_task(self, directory_name):
    subprocess.Popen(['python', './code/test.py', '--dataset', 'imagepath', 
                    '--data_path', './code/'+directory_name, '--save_visualize'])
    # I removed the time.sleep here because it shouldn't be necessary with the async task
    # You can include it if you need it for some reason.
    with lock:
        global original_dir
        original_dir = 'E:\\MachVis\\GLPDepth-main\\code\\'+directory_name  # update this with your actual original images directory path
        original_images = set(os.listdir(original_dir))
        all_output_images = os.listdir(output_dir)
        new_output_images = [img for img in all_output_images if img in original_images]
        image_pairs = [(img, img) for img in new_output_images] #This line is used to find the pair of images with the same name
    return image_pairs

@app.route('/original_images/<filename>')
def serve_original_image(filename):
    global original_dir
    return send_from_directory(original_dir, filename)

@app.route('/run_script/<filename>')
def serve_output_image(filename):
    return send_from_directory(output_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)
