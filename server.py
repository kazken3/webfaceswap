import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
import subprocess


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('select_2nd_file',
                                    filename=filename))

    return render_template('1st.html')


@app.route('/2nd', methods=['GET', 'POST'])
def select_2nd_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'firstimg' not in request.form or 'secondimg' not in request.files:
            flash('No file part')
            return redirect(request.url)
        firstfilename = request.form.get('firstimg')
        secondfile = request.files['secondimg']
        if firstfilename == '' or secondfile.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if secondfile and allowed_file(secondfile.filename):
            secondfilename = secure_filename(secondfile.filename)
            secondfile.save(os.path.join(app.config['UPLOAD_FOLDER'], secondfilename))
            return redirect(url_for('check_all_file',  firstimg=firstfilename, secondimg=secondfilename))
    filename = request.args.get('filename')
    img_url = './uploads/' + filename
    return render_template('2nd.html', filename=img_url, firstimg=filename)


@app.route('/check', methods=['GET', 'POST'])
def check_all_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'firstimg' not in request.form or 'secondimg' not in request.form:
            flash('No file part')
            return redirect(request.url)
        firstfilename = request.form.get('firstimg')
        secondfilename = request.form.get('secondimg')
        if firstfilename == '' or secondfilename == '':
            flash('No selected file')
            return redirect(request.url)
        img_url1 = './uploads/' + firstfilename
        img_url2 = './uploads/' + secondfilename
        subprocess.call(["python", "./faceswap.py", img_url1, img_url2])
        return redirect(url_for('finish_file'))
    filename1 = request.args.get('firstimg')
    filename2 = request.args.get('secondimg')
    img_url1 = './uploads/' + filename1
    img_url2 = './uploads/' + filename2
    return render_template('check.html', img_url1=img_url1, filename1=filename1, img_url2=img_url2, filename2=filename2)


@app.route('/finish', methods=['GET'])
def finish_file():
    file_url = './output/output.jpg'
    return render_template('finish.html', file_url=file_url)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/output/<filename>')
def oupput_file(filename):
    return send_from_directory('output', filename)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8888, threaded=True)
