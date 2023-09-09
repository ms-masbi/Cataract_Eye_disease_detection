import cv2
import os
import tensorflow as tf
from tensorflow import keras

from roboflow import Roboflow
import cv2
import math
import numpy as np

import random
import os
import numpy as np


class CataractDetect:

	def __init__(
	    self,
	    input=1,
	    ):
		self.input = input
		self.capture = None
		self.detect = 1
		self.frame = None
		self.image_dir = "CEDD/static/images"
		self.model = keras.models.load_model( "CEDD/static/model/model" )
		self.current_img = None
		rf = Roboflow( api_key="dHg9mKRRDSCBTlbaEl8w" )
		project_eye = rf.workspace().project( "eyes-dpurk" )
		self.model_eye = project_eye.version( 2 ).model
		project_iris = rf.workspace().project( "iris_120_set" )
		self.model_iris = project_iris.version( 7 ).model

	def start_detection( self, VIDEO ):
		self.capture = cv2.ImageCapture( VIDEO )
		self.detect = 1
		while self.detect:

			_, self.frame = self.capture.read()

			if self.frame is None:
				print( "End of stream" )
				break

			( flag, encodedImage ) = cv2.imencode( ".jpg", self.frame )

			if not flag:
				continue

			yield ( b'--frame\r\n'
			        b'Content-Type: image/jpeg\r\n\r\n' + bytearray( encodedImage ) + b'\r\n' )
		self.capture.release()

	def get_results( self, image ):
		self.detect = 0
		if str( image ).isdigit():
			files = [ f for f in os.listdir( self.image_dir ) if os.path.isfile( os.path.join( self.image_dir, f ) ) ]
			if files == []:
				filename = "1.jpg"
			else:
				filename = "{}.jpg".format( int( files[ -1 ].split( "." )[ 0 ] ) + 1 )
			self.current_img = os.path.join( self.image_dir, filename )
			cv2.imwrite( os.path.join( self.image_dir, filename ), self.frame )
		else:
			filename = image.split( "/" )[ -1 ]
			print( filename )

		result = self.predict( os.path.join( self.image_dir, filename ) )
		result = cv2.cvtColor( result, cv2.COLOR_BGR2RGB )
		cv2.imwrite( os.path.join( self.image_dir, filename ), result )

		# cv2.putText( self.frame, "hello", ( 0, 0 ) )
		return [ os.path.join( "images", filename ) ]

	def extract_eye( self, img ):
		eye_predictions = self.model_eye.predict( img, confidence=20, overlap=40 ).json()[ 'predictions' ]
		eyes = []
		if eye_predictions != []:
			for prediction in eye_predictions:
				if prediction[ "class" ] == "Open Eyes":
					X, Y, W, H = int( prediction[ 'x' ] ), int( prediction[ 'y' ]
					                                           ), int( prediction[ 'width' ]
					                                                  ), int( prediction[ 'height' ] )

					H = int( H / 2 )
					W = int( W / 2 )

					cropped_image = img[ Y - H : Y + H, X - W : X + W ]
					eyes.append( [ cropped_image, X, Y, W, H ] )

		return eyes

	def extract_iris( self, img ):
		predictions_iris = self.model_iris.predict( img, confidence=50, overlap=40 ).json()[ 'predictions' ]
		iris = None
		if predictions_iris != []:
			for prediction in predictions_iris:
				if prediction[ "class" ] == "0":
					flag = False
					X, Y, W, H = int( prediction[ 'x' ] ), int( prediction[ 'y' ]
					                                           ), int( prediction[ 'width' ]
					                                                  ), int( prediction[ 'height' ] )

					H = int( H / 2 )
					W = int( W / 2 )

					iris = img[ Y - H : Y + H, X - W : X + W ]

		return iris

	def predict( self, img ):
		img = cv2.imread( img )
		img = cv2.cvtColor( img, cv2.COLOR_BGR2RGB )
		eyes = self.extract_eye( img )

		for eye in eyes:
			X, Y, W, H = eye[ 1 : ]
			iris = self.extract_iris( eye[ 0 ] )
			image_resized = cv2.resize( iris, ( 120, 120 ) )
			image = np.expand_dims( image_resized, axis=0 )
			model_pred = self.model.predict( image )[ 0 ][ 0 ]
			start_point = ( int( X - W ), int( Y - H ) )
			end_point = ( int( X + W ), int( Y + H ) )
			if model_pred < 0.5:
				cv2.rectangle( img, start_point, end_point, color=( 255, 0, 0 ), thickness=4 )
				print( "Sorry to tell you that your eye might affected with Cataract !" )

			else:
				cv2.rectangle( img, start_point, end_point, color=( 0, 255, 0 ), thickness=4 )

				print( "Hurrey! You Have Normal Eye." )

			print( model_pred )
		if eyes == []:
			raise Exception( "No Eyes Detected" )
		return img
