from CEDD import db
import datetime


class ImageVO( db.Model ):
	__tablename__ = 'imagemaster'
	imageId = db.Column( 'imageId', db.Integer, primary_key=True, autoincrement=True )
	imagePath = db.Column( 'imagePath', db.String( 100 ) )
	imageName = db.Column( 'imageName', db.String( 100 ), unique=True )
	imageDate = db.Column( 'imageDate', db.String( 100 ), default=datetime.datetime.now().strftime( "%d-%m-%Y" ) )
	imageTime = db.Column( 'imageTime', db.String( 100 ), default=datetime.datetime.now().strftime( "%H:%M:%S" ) )

	# image_crossroadId = db.Column( 'image_crossroadId', db.Integer, db.ForeignKey( CrossroadVO.crossroadId ) )

	def as_dict( self ):
		return {
		    'imageId': self.imageId,
		    'imageName': self.imageName,
		    'imageDate': self.imageDate,
		    'imageTime': self.imageTime
		    # 'image_crossroadId': self.image_crossroadId
		    }


db.create_all()
