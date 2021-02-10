from numpy import ndarray
from STL        import Enum
from STL        import Copy
from STL        import Arrays
from STL        import Typing
from OSPlatform import Platform

import LAL

EKeyCode = Platform.EKeyCode



class EState () :

	None_    = 0
	Released = 1
	Pressed  = 2
	Held     = 3



CKeys_NumTracked = 6



class KeySignals :

	Up    = False
	Down  = False
	Left  = False
	Right = False
	Enter = False
	Tab   = False

	def GetViaIndex(self, _index) :

		switcher = {
			0 : self.Up,
			1 : self.Down,
			2 : self.Left,
			3 : self.Right,
			4 : self.Enter,
			5 : self.Tab
		}

		return switcher.get(_index, -1)

	@staticmethod
	def GetIndexViaKeyCode(_key) :

		switcher = {
			EKeyCode.Arrow_Up    : 0,
			EKeyCode.Arrow_Down  : 1,
			EKeyCode.Arrow_Left  : 2,
			EKeyCode.Arrow_Right : 3,
			EKeyCode.Enter       : 4,
			EKeyCode.Tab         : 5,
		}

		return switcher.get(_key, -1)

	@staticmethod
	def GetKeyCodeViaIndex(_index) :

		switcher = {
			0 : EKeyCode.Arrow_Up,
			1 : EKeyCode.Arrow_Down,
			2 : EKeyCode.Arrow_Left,
			3 : EKeyCode.Arrow_Right,
			4 : EKeyCode.Enter,
			5 : EKeyCode.Tab
		}

		return switcher.get(_index, -1)



__CurrentSignalState  = KeySignals()
__PreviousSignalState = KeySignals()

__KeyStates    = Arrays.empty(CKeys_NumTracked, dtype = EState )
__KeyEventSubs = Arrays.empty(CKeys_NumTracked, dtype = ndarray)



def Update() :

	global __CurrentSignalState, __PreviousSignalState, __KeyStates, __KeyEventSubs

	__PreviousSignalState = Copy.copy(__CurrentSignalState)

	for index in range(CKeys_NumTracked) :

		current  = __CurrentSignalState.GetViaIndex(index)

		current = Platform.GetKeySignal(__CurrentSignalState.GetKeyCodeViaIndex(index))

		previous = __PreviousSignalState.GetViaIndex(index)

		currentState = __KeyStates[index]

		latestState = EState.None_

		if current == previous :

			if   current      == True        : latestState = EState.Held
			elif currentState != EState.Held : latestState = EState.None_

		else :

			if   current      == False : latestState = EState.Released
			else                       : latestState = EState.Pressed

		if latestState != currentState : 

			currentState = latestState

			if __KeyEventSubs[index] == None : return

			for sub in __KeyEventSubs[index] : 
				
				if sub != None : sub()


def Subscribe(_key = EKeyCode, _callback = Typing.Callable) :

	global __KeyEventSubs
	
	subs = __KeyEventSubs[KeySignals.GetIndexViaKeyCode(_key)]

	for sub in subs :

		if sub == None :

			sub = _callback

			return

	subs = Arrays.append(subs, _callback)


def Unsubscribe(_key = EKeyCode, _callback = Typing.Callable) :

	global __KeyEventSubs

	subs = __KeyEventSubs[KeySignals.GetIndexViaKeyCode(_key)]

	for sub in subs :

		if sub == _callback :

			sub = None
