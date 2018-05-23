from flask import Flask
from flask import render_template, request

app = Flask(__name__)



@app.route( '/', methods=['GET', 'POST'])
def index():
    # https://stackoverflow.com/questions/35649770/how-to-upload-multiple-files-using-flask-in-python/39443137
    print ':::', request.method
    if request.method == 'GET':
        return render_template( 'index.html')
    else:
        print 'a'
        for f in request.files.getlist('img'):
            print f.filename
            #print dir( f)
            f.save( './' + f.filename)
        return '32,42'
        


if __name__ == '__main__':
    app.run()
