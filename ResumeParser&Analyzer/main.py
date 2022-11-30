import os
import nltk
import fitz
from docx import Document
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from difflib import SequenceMatcher
from pyresparser import ResumeParser
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired

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


def process_resume(resume):
    try:
        doc = Document()
        with open(resume, 'r') as file:
            doc.add_paragraph(file.read())
        doc.save('text.docx')
        data = ResumeParser('text.docx').get_extracted_data()
        output = data
    except:
        data = ResumeParser(resume).get_extracted_data()
        output = data
    return output


def stopwords_removal(text):
    text = nltk.sent_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    for i in range(len(text)):
        words = nltk.word_tokenize(text[i])
        words = [lemmatizer.lemmatize(word) for word in words if word not in set(stopwords.words('english'))]
        text[i] = ' '.join(words)
    return text


def similarity(tx, jd):
    s = SequenceMatcher(None, tx, jd).ratio() * 100
    return s


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

            tx = process_resume(f'C:\\Users\\NISHU\\Desktop\\Copy\\ResumeParser&Analyzer\\static\\files\\{filename}')

        filename = f'C:\\Users\\NISHU\\Desktop\\Copy\\ResumeParser&Analyzer\\static\\files\\{filename}'
        resume = open_file(filename)
        resume = stopwords_removal(resume)

        jd = request.form['jd']
        # jd = stopwords_removal(jd)

        similarity_percentage = similarity(jd, resume)
        return render_template('result.html', jd=jd, tx=tx, similarity_percentage=similarity_percentage)

    return render_template('home.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
