from flask import Flask, request, render_template, redirect, url_for
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  

@app.route('/select_directory', methods = ['POST'])
def select_directory():
    return render_template('select_directory.html')

@app.route('/run_script' , methods = ['POST'])
def run_script():
    if request.method == 'POST':
        file = request.files['file']
        directory_name = os.path.dirname(file.filename)
        subprocess.Popen(['python', './code/test.py', '--dataset', 'imagepath', 
                        '--data_path', './code/'+directory_name, '--save_visualize'])
    return render_template('go_back.html')

if __name__ == "__main__":
    app.run(debug=True)


