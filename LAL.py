import STL



def constant(_function) :

	def _functionset(self, value) : raise TypeError
	def _functionget(self       ) : return _function()

	return property(_functionget, _functionset)



# Do at the end...
class Bitfield :

	def __init__(self, _value) :

		self.Mask = _value