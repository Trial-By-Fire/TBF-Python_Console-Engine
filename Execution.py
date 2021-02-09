from STL import SYS;

from Config import Debug;

import Cycler;
import Renderer;




def PrepareModules() :

	Renderer.LoadModule();



def Entrypoint() :

	if Debug.Enabled :

		try :

			PrepareModules();

			Cycler.Initialize();

		except Exception as _what :

			SYS.stderr.write("Error: " + repr(_what));

			SYS.stderr.flush();

			SYS.exit(1);
	else :

		PrepareModules();

		Cycler.Initialize();