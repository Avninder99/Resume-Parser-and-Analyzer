from pyresparser import ResumeParser
from docx import Document
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from flask_wtf import FlaskForm
from flask_cors import CORS
from wtforms import StringField, FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, DataRequired
import nltk
import fitz
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.pdf', '.docx']


def open_file(filename):
    docs = fitz.open(filename)
    txt = ''
    for page in docs:
        txt = txt + str(page.get_text())
    tx = ' '.join(txt.split('\n'))
    return tx


@app.errorhandler(413)
def too_large(e):
    return render_template("size.html")


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()

    if form.validate_on_submit():
        file = form.file.data  # first grab the file

        filename = secure_filename(file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return render_template("extension.html")

            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                   secure_filename(file.filename)))  # then save the file

            tx = open_file(f'C:\\Users\\NISHU\\Desktop\\Copy\\ResumeParser&Analyzer\\static\\files\\{filename}')

        jd = request.form['jd']
        jd = jd.upper()
        return render_template('result.html', jd=jd, tx=tx)

    return render_template('home.html', form=form)


@app.route('/result', methods = ['GET', 'POST'])
def result():
    return render_template('result.html')


if __name__ == '__main__':
    app.run(debug=True)
