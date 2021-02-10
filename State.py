
from STL import AClass



class AState (AClass.ABC) :

	def Load  (self) : pass
	def Unload(self) : pass
	def Update(self) : pass
	def Render(self) : pass



class State (AState) :

	def Set(self, _state : AState) : 
		
		if (self._CurrentState != None) : 
			
			self._CurrentState.Unload()

		self._CurrentState = _state

		self._CurrentState.Load()
		

	def Load  (self) : self._CurrentState.Load()
	def Unload(self) : self._CurrentState.Unload()

	
	def Update(self) : 
		
		if self._CurrentState != None : 
			
			self._CurrentState.Update()


	def Render(self) : 

		if self._CurrentState != None : 

			self._CurrentState.Render()


	_CurrentState = None



_EngineState = State();



def GetEngineState() : 
	
	return _EngineState


def SetEngineState(_state : AState) :
	
	_EngineState.Set(_state)
