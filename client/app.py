

from flask import Flask, render_template, request, redirect
#from werkzeug.security import secure_filename
from . import rekog_client as helper

app     = Flask(__name__)
#app.config.from_object("config")


@app.route("/")
def index():
    return render_template("index.html", files=[  ] )

@app.route("/", methods=["POST"])
def upload_file():

    if "user_file" not in request.files:
        return "No user_file key in request.files"

    file    = request.files["user_file"]

    if file.filename == "":
        return "Please select a file"

    if file :
        print 'begin upload ', file.filename
        helper.upload_file_to_s3( file, 'steel-bucket')

        print 'upload completed'
        moderation_result = helper.get_moderation_result( file.filename)
        print 'result', moderation_result
    
        mod_html = '<br>'.join( [x['Name'] + "("+str(x['Confidence'])+")" for x in eval(moderation_result['Item']['moderation'])])

        print mod_html

        #mod_html = moderation_result
        return render_template("index.html", files=[ {'name': + file.filename, 'status':mod_html} ] )

    else:
        return redirect("/")




if __name__ == "__main__":
    app.run()



