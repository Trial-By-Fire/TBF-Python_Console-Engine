from STL import Time



_TimeSnapshot_Start = int;
_TimeSnapshot_End   = int;
_DeltaTime_NS       = int;
_DeltaTime_S        = float();



def TakeStartSnapshot() :

	global _TimeSnapshot_Start; _TimeSnapshot_Start = Time.time_ns()


def TakeEndingSnapshot() :

	global _TimeSnapshot_End; _TimeSnapshot_End = Time.time_ns()

def GetDeltaTime() -> float :

	global _DeltaTime_S; 
	
	return _DeltaTime_S

def Update() :

	global _DeltaTime_NS, _DeltaTime_S, _TimeSnapshot_End, _TimeSnapshot_Start

	_DeltaTime_NS = _TimeSnapshot_End - _TimeSnapshot_Start
	_DeltaTime_S  = _DeltaTime_NS / 1000000000



class Timer :

	def __init__(self, _endTime : float) :

		self.EndTime = _endTime

	def Ended(self) -> bool :

		return self.Elapsed >= self.EndTime

	def Reset(self) :

		self.Elapsed = 0.0

	def Tick(self) :

		delta = GetDeltaTime();

		self.Elapsed = float(self.Elapsed) + delta


	Elapsed = 0.0
	EndTime = 0.0

