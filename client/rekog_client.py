
import boto3, botocore

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

def upload_file_to_s3( file, bucket_name, acl="public-read"):
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



def moderate_file( file, bucket_name='steel-bucket'):

    upload_file_to_s3( file, bucket_name)

    moderation_result = get_moderation_result( file.filename)

    return moderation_result

    #mod_html = '<br>'.join( [x['Name'] + "("+str(x['Confidence'])+")" for x in eval(moderation_result['Item']['moderation'])])
    return render_template("index.html", files=[ {'name': + file.filename, 'status':mod_html} ] )



if __name__ == "__main__":
    app.run()



