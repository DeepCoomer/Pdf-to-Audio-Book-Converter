from flask import Flask, render_template, send_file, request
import pyttsx3
import PyPDF2
# from englisttohindi.englisttohindi import EngtoHindi
import os

app = Flask(__name__)



@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def get_pred():
    download = False
    name = ""
    if request.method == "POST":
        file = request.files['my_file']

        file_path = "static/" + file.filename
        file.save(file_path)

        pdffile = file_path

        book = open(pdffile, 'rb')
        pdfReader = PyPDF2.PdfReader(book)
        pages = pdfReader.pages

        speaker = pyttsx3.init()

        finaltext = ""

        for num in range(0,len(pages)):
            page = pdfReader.pages[num]
            text = page.extract_text()

            finaltext += text
        
        # print(finaltext)

        # res = EngtoHindi(finaltext)
        # print(res.convert)

        voice = speaker.getProperty('voices')
        speaker.setProperty('voice', voice[3].id)

        name = file.filename
        name = name.split('.')
        name = name[0]
# speaker.setProperty('rate', 149)
        speaker.save_to_file(finaltext, 'downloads\\' + name+'.mp3')
        speaker.runAndWait()
        download = True
        
    return render_template('index.html', download = download, name = name)

@app.route("/dw/<name>", methods=['GET', 'POST'])
def download(name=None):

    path = 'downloads/'+name+'.mp3'
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.debug = False
    app.run(debug=False)