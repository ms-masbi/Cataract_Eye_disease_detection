from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from CEDD import app
from CEDD.com.dao.UploadimageDAO import ImageDAO
from CEDD.com.vo.UploadimageVO import ImageVO
import CEDD.com.controller.DetectionController as dc
from CEDD.com.controller.LoginController import LoginSession, LogoutSession


@app.route( '/user/loadImage', methods=[ 'GET' ] )
def userLoadImage():
	try:
		if LoginSession() == 'user':

			return render_template( 'user/uploadImage.html' )
		else:
			return redirect( url_for( 'LogoutSession' ) )
	except Exception as ex:
		print( ex )


@app.route( '/user/insertImage', methods=[ 'POST' ] )
def userInsertImage():
	try:
		if LoginSession() == 'user':
			image = request.files[ 'image' ]

			# image_crossroadId = request.form[ 'image_crossroadId' ]
			imagepath = "CEDD/static/images/"
			imagename = secure_filename( image.filename )
			# files = [ f for f in os.listdir( imagepath ) if os.path.isfile( os.path.join( imagepath, f ) ) ]
			# if files == []:
			# 	imagename = "1.jpg"
			# else:
			# 	imagename = "{}.jpg".format( int( files[ -1 ].split( "." )[ 0 ] ) + 1 )
			print( imagename )
			image.save( imagepath + imagename )
			imageVO = ImageVO()
			imageDAO = ImageDAO()
			imageVO.imageName = imagename
			imageVO.imagePath = imagepath
			# imageVO.image_crossroadId = image_crossroadId
			imageDAO.insertImage( imageVO )
			dc.IMAGE = imagepath + imagename
			return redirect( url_for( 'detect' ) )
		else:
			return redirect( url_for( 'LogoutSession' ) )

	except:
		# image_crossroadId = request.form[ 'image_crossroadId' ]
		imagepath = "CEDD/static/images/" + secure_filename( image.filename )
		dc.IMAGE = imagepath
		return redirect( url_for( 'detect' ) )


@app.route( '/user/startweb', methods=[ 'POST' ] )
def startweb():
	camera_id = request.form[ 'index' ]
	if camera_id == "":
		camera_id = 1
	dc.IMAGE = int( camera_id )
	return render_template( 'user/detection.html' )


@app.route( '/admin/viewImage', methods=[ 'GET' ] )
def adminViewImage():
	try:
		if LoginSession() == 'admin':
			imageDAO = ImageDAO()
			imageVOList = imageDAO.viewImage()
			print( "__________________", imageVOList )
			return render_template( 'admin/viewImage.html', imageVOList=imageVOList )
		else:
			return redirect( url_for( 'LogoutSession' ) )
	except Exception as ex:
		print( ex )


@app.route( '/admin/deleteImage', methods=[ 'GET' ] )
def adminDeleteImage():
	try:
		if LoginSession() == 'admin':
			imageVO = ImageVO()

			imageDAO = ImageDAO()

			imageId = request.args.get( 'imageId' )
			imagePath = request.args.get( 'imagePath' )
			os.remove( imagePath )
			imageVO.imageId = imageId
			imageDAO.deleteImage( imageVO )

			return redirect( url_for( 'adminViewImage' ) )
		else:
			return redirect( url_for( 'LogoutSession' ) )
	except Exception as ex:
		print( ex )


# @app.route('/Admin/editImage', methods=['GET'])
# def adminEditImage():
#    try:
#        crossroadDAO = CrossroadDAO()
#        crossroadVOList = crossroadDAO.viewCrossroad()
#        imageVO = ImageVO()
#
#        imageDAO = ImageDAO()
#
#        imageId = request.args.get('ImageId')
#
#        imageVO.ImageId = imageId
#
#        imageVOList = imageDAO.editImage(imageVO)
#
#        print("=======imageVOList=======", imageVOList)
#
#        print("=======type of imageVOList=======", type(imageVOList))
#
#        return render_template('Admin/AddImage.html', imageVOList=imageVOList,crossroadVOList=crossroadVOList)
#    except Exception as ex:
#        print(ex)
#
#
# @app.route('/Admin/updateImage', methods=['POST'])
# def adminUpdateImage():
#    try:
#        imageId = request.form['ImageId']
#        image = request.form['image']
#        image_crossroadId= request.form['image_crossroadId']
#
#        imageVO = ImageVO()
#        imageDAO = ImageDAO()
#
#        imageVO.ImageId = imageId
#        imageVO.ImageName= imagename
#        imageVO.Image_CrossroadId= image_crossroadId
#
#        imageDAO.updateImage(imageVO)
#
#        return redirect(url_for('adminViewImage'))
#    except Exception as ex:
#        print(ex)
