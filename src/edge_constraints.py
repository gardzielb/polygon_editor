from enum import Enum

from pathlib import Path

img_path = str( Path( __file__ ).parent.parent.absolute() ).replace( '\\', '/' ) + '/img'


class EdgeConstraint( Enum ):
	VERTICAL = f'{img_path}/vertical.png'
	HORIZONTAL = f'{img_path}/horizontal.png'
	FIXED_LENGTH = f'{img_path}/ruler.png'
