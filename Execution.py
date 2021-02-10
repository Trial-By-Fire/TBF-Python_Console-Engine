from Config import Debug
from STL    import SYS

import Cycler
import Renderer



def PrepareModules() :

	Renderer.LoadModule()


def Entrypoint() :

	if Debug.Enabled :

		try :

			PrepareModules()

			Renderer.WriteToLog("TBF Python Engine")

			Cycler.Initialize()

			Renderer.UnloadModule()

		except Exception as _what :

			SYS.stderr.write("Error: " + repr(_what))

			SYS.stderr.flush()

			SYS.exit(1)
	else :

		PrepareModules()

		Renderer.WriteToLog("TBF Python Engine")

		Cycler.Initialize()

		Renderer.UnloadModule()