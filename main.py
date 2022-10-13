import nltk
from pyresparser import ResumeParser
from docx import Document
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

@app.route('/parse', methods=['POST','GET'])
def parse():
    if request.method=='POST':
        try:
            doc = Document()
            with open('static/files/Resume.pdf', 'r') as file:
                doc.add_paragraph(file.read())
                doc.save('text.docx')
                data = ResumeParser('text.docx').get_extracted_data()
                print(data['skills'])
        except:
            data = ResumeParser(filed).get_extracted_data()
            print(data['skills'])
        return render_template('index.html')
    else:
        return render_template('index.html')

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    
    if form.validate_on_submit():
        file = form.file.data # first grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename))) # then save the file
        return "File has been successfully uploaded."
    
    return render_template('index.html', form=form);

if __name__ == '__main__':
    app.run(debug = True)