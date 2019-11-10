from flask import Flask,request,jsonify,render_template
import os
from fastai import *
from fastai.vision import *
from skimage import measure, filters
import cv2
from scipy import ndimage
import numpy




app = Flask(__name__, static_url_path='/static')

@app.route('/')
def render_page():
    return render_template('index.html')

@app.route('/count',  methods=['POST'])
def count():
	#Read the Image
	#file = request.files['file']

	#image = cv2.imread(file.filename)
	image = cv2.imdecode(numpy.fromstring(request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	k = 7
	blur = cv2.GaussianBlur(src = gray, ksize = (k, k), sigmaX = 0)
	val = filters.threshold_otsu(blur)

	colony_centroids = ndimage.binary_fill_holes(blur < val)

	labels = measure.label(colony_centroids)
	result = labels.max()
	return render_template('result.html', result = result)

#render_template('count.html')

@app.route('/classify', methods=['POST'])
def classify():
	learner = load_learner('model/')
	file = request.files['file']
    
    #image_extensions=['ras','xwd', 'bmp', 'jpe', 'jpg', 'jpeg', 'xpm', 'ief', 'pbm', 'tif', 'gif', 'ppm', 'xbm', 'tiff', 'rgb', 'pgm', 'png', 'pnm']    
    
    #if file.filename.split('.')[1] not in image_extensions:
        #return jsonify('Please upload an appropriate image file')
	img = open_image(file)
	pred = learner.predict(img)
	result = str(pred[0])

	return render_template('result.html', result = result)
    #your application logic here


if(__name__ == '__main__'):
	app.run(debug=True,port=os.getenv('PORT',5000))