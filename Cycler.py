import LAL
import Input
import Renderer
import State
import State_Intro
import Timing



__Exist = False



def Initialize() : 

		__Exist = True

		State.SetEngineState(State_Intro.GetState())

		while __Exist :

			Timing.TakeStartSnapshot()

			Input.Update()

			State.GetEngineState().Update()

			Renderer.Update()

			Timing.TakeEndingSnapshot()

			Timing.Update()

			Renderer.ProcessTiming()


def Lapse() :

	__Exist = False