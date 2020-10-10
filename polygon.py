class Polygon:
	def __init__( self, points: list ):
		self.points = points

	def vertices( self ) -> int:
		return len( self.points )
