#upload files ref: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
#http://flask.pocoo.org/
#http://www.cs.tut.fi/~jkorpela/forms/file.html

import os
from flask import Flask, request, redirect, flash, render_template, send_from_directory, current_app
import pandas as pd
from werkzeug.utils import secure_filename
from flask_debugtoolbar import DebugToolbarExtension


# FLASK_DEBUG=1

#declare variables and configurations
UPLOAD_FOLDER = r'C:\TEST\FOLDER\HERE'

ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.debug = True
app.config['SECRET_KEY'] = 'DontTellAnyone'
toolbar = DebugToolbarExtension(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/inputs', methods=['GET', 'POST'])
def inputs():
    error = None
    df = ''
    inputvalue1 = None
    inputvalue2 = None


    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        param1 = request.form.get('param1')


        # if user does not select file, browser also
        # submit a empty part without filename
        print(file.filename)
        print(param1)
        print("IS FILENAME NULL", file.filename == '')
        print("IS param1 NULL", param1 == '')

        if file.filename == '' or param1 == '':
            error = 'No selected file or input param1'

        elif allowed_file(file.filename) == False:
            error = 'Uploaded file is in wrong format'

        elif file and allowed_file(file.filename) and param1 != 'DEBRA':
            error = 'Param1 is not DEBRA'


        #else if everything is ok
        elif file and allowed_file(file.filename) and param1 == 'DEBRA':
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print("os.path.join(app.config['UPLOAD_FOLDER'], filename)  is ", os.path.join(app.config['UPLOAD_FOLDER'], filename))


            error = None
            #send_from_directory(directory=r'C:\Users\chood\Downloads', filename='Sacramentorealestatetransactions.csv', as_attachment=True)

            df = pd.read_csv(UPLOAD_FOLDER + '//' + file.filename)

            # print(df)
            inputvalue2 = df['csvparam2'][0]
            inputvalue1 = df['csvparam1'][0]
            # print(df['csvparam1'][0])
            # print(df['csvparam2'][0])
        else:
            error = 'Ends up here'

    return render_template('inputs.html', error=error, inputvalue1 = inputvalue1, inputvalue2 = inputvalue2 )


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    print ("uploads ", uploads)
    return send_from_directory(directory=uploads, filename=filename)


@app.route('/bootstrapTemplate')
def bootstrap():
    return render_template('bootstrapTemplate.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
