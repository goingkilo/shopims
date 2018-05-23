import boto3,botocore

from flask import Flask, render_template, request, redirect
#from werkzeug.security import secure_filename

s3 = boto3.client(
   "s3",
   aws_access_key_id='key',
   aws_secret_access_key='secret'
)

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='key',
    aws_secret_access_key='secret'
                          )

table = dynamodb.Table('image_metadata_w_tags')


app     = Flask(__name__)
#app.config.from_object("config")

def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e


def get_moderation_result( filename):
    a = table.get_item( Key={'image_name': filename})
    return a



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
        #print file, type( file), dir( file)
        #file.filename = secure_filename( file.filename)
        print 'begin upload ', file.filename
        upload_file_to_s3( file, 'shopmatic-bucket')
        print 'upload completed'
        moderation_result = get_moderation_result( file.filename)
        print moderation_result
    
        try :
            mod_html = '<br>' +  moderation_result + '</br>'
        except:
            mod_html = '<b> no tags </b>'
        print type(moderation_result), mod_html
        #mod_html = moderation_result
        return render_template("index.html", files=[ {'name':  file.filename, 'status':mod_html} ] )

    else:
        return redirect("/")




if __name__ == "__main__":
    app.run()



