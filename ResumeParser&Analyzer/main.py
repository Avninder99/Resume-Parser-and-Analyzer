import os
import nltk
import fitz
from docx import Document
import textdistance as td
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from pyresparser import ResumeParser
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']


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
    text = ''.join(map(str, text))
    return text


def match(resume, job_des):
    j = td.jaccard.similarity(resume, job_des)
    s = td.sorensen_dice.similarity(resume, job_des)
    c = td.cosine.similarity(resume, job_des)
    o = td.overlap.normalized_similarity(resume, job_des)
    total = round((j + s + c + o) / 4, 5)
    return total * 100


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
        path = f'C:\\Users\\NISHU\\PycharmProjects\\Resume-Parser-and-Analyzer\\ResumeParser&Analyzer\\static\\files\\{filename}'
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return render_template("extension.html")

            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                   secure_filename(file.filename)))  # then save the file

            tx = process_resume(path)

        resume = open_file(path)
        resume = stopwords_removal(resume)

        jd = request.form['jd']
        # jd = stopwords_removal(jd)

        similarity_percentage = match(jd, resume)
        return render_template('result.html', jd=jd, tx=tx, similarity_percentage=similarity_percentage)

    return render_template('home.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
