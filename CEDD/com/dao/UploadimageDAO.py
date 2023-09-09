from CEDD import db
from CEDD.com.vo.UploadimageVO import ImageVO


class ImageDAO:

	def insertImage( self, imageVo ):
		db.session.add( imageVo )
		db.session.commit()

	def viewImage( self ):
		#        ImageList = db.session.query(ImageVO, CrossroadVO).join(CrossroadVO,ImageVO.Image_CrossroadId == CrossroadVO.categoryId).all()

		imageList = db.session.query( ImageVO ).all()

		return imageList

	def deleteImage( self, imageVO ):

		imageList = ImageVO.query.get( imageVO.imageId )

		db.session.delete( imageList )

		db.session.commit()

	def editImage( self, imageVO ):

		# categoryList = CrossroadVO.query.get(categoryVO.categoryId)

		# categoryList = CrossroadVO.query.filter_by(categoryId=categoryVO.categoryId)

		imageList = ImageVO.query.filter_by( imageId=imageVO.imageId ).all()

		return imageList

	def updateImage( self, imageVO ):

		db.session.merge( imageVO )

		db.session.commit()

	def ajaxImageProduct( self, imageVO ):
		ajaxProductimageList = imageVO.query.filter_by( image_crossroadId=ImageVO.image_crossroadId ).all()
		return ajaxProductimageList
