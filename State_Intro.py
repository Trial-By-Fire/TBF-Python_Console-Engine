from Platform_Windows import CAttribute
from OSPlatform import Platform

import Engine
import State
import Renderer
import Timing



class IntroState (State.AState) :

	def Load(self) :

		Renderer.WriteToLog("Intro State: Loaded")

		if self.Loaded == False :

			self.Title_Cells  .String = self.IntroTitle
			self.Version_Cells.String = self.EngineVersion

			self.Title_Cells  .SetAttribute(Renderer.CAttribute.FG_Intensity)
			self.Version_Cells.SetAttribute(Renderer.CAttribute.FG_Intensity)

			startingCell   = Renderer.Vec2D()
			startingCell.Y = 9
			startingCell.X = int(Renderer.CBufferWidth / 2) - int(len(self.IntroTitle) / 2) - 1

			self.Title_Cells.Position = Platform.CreateCoord(X = startingCell.X, Y = startingCell. Y)

			startingCell.Y = 11
			startingCell.X = int(Renderer.CBufferWidth / 2) - int(len(self.EngineVersion) / 2) - 1

			self.Version_Cells.Position = Platform.CreateCoord(X = startingCell.X, Y = startingCell.Y)

			self.Loaded = True


	LogTitle                 = True
	LogTitle_ChangeToWhite   = True
	LogVersion               = True
	LogVersion_ChangeToWhite = True
	Log_FadeToGrey           = True
	Log_Fade                 = True
	Log_End                  = True

	def Unload(self) :

		Renderer.WriteToLogs("Intro State: Unloaded")


	def Update(self) : 

		self.IntroTimer.Tick()
		self.TillTitle .Tick()

		Renderer.WriteToPersistentSection(4, "Intro Time Elapsed: " + str(self.IntroTimer.Elapsed))

		if self.TillTitle.Ended() :

			if self.LogTitle : 

				Renderer.WriteToLog("Title Appears: Grey")

				self.RenderTitle = True
				self.LogTitle    = False

			self.TillTitle_ToWhite.Tick()

			if self.LogTitle_ChangeToWhite and self.TillTitle_ToWhite.Ended() :

				self.Title_Cells.SetAttribute(Platform.CConsole_WhiteCell)

				Renderer.WriteToLog("Title Appears: White")

				self.LogTitle_ChangeToWhite = False
			
			self.TillVersion.Tick()

			if self.LogVersion and self.TillVersion.Ended() :

				Renderer.WriteToLog("Version Appears: Grey")

				self.LogVersion    = False
				self.RenderVersion = True

			if self.RenderVersion :

				self.TillVersion_ToWhite.Tick()

				if self.LogVersion_ChangeToWhite and self.TillVersion_ToWhite.Ended() :

					Renderer.WriteToLog("Version Appears: White") 

					self.Version_Cells.SetAttribute(Platform.CConsole_WhiteCell)

					self.LogVersion_ChangeToWhite = False

		self.TillFadeToGrey.Tick()

		if self.TillFadeToGrey.Ended() :

			self.Title_Cells  .SetAttribute(Renderer.CAttribute.FG_Intensity)
			self.Version_Cells.SetAttribute(Renderer.CAttribute.FG_Intensity)

			if self.Log_FadeToGrey :

				Renderer.WriteToLog("Fading")

				self.Log_FadeToGrey = False

			self.TillFadeOut.Tick()

			if self.Log_Fade and self.TillFadeOut.Ended() :

				Renderer.WriteToLog("Faded out")

				self.RenderTitle   = False
				self.RenderVersion = False

				self.Log_Fade = False

		if self.Log_End and self.IntroTimer.Ended() :

			Renderer.WriteToLog("Intro Ended")

			self.Log_End = False
			
			if Engine.LoadGame == None :

				Renderer.WriteToLog("Engine: LoadGame has not been set.")

			else : State.SetEngineState(Engine.LoadGame())


	def Render(self) :

		if self.RenderTitle   : self.Title_Cells  .WriteToBuffer()
		if self.RenderVersion : self.Version_Cells.WriteToBuffer()


	IntroTimer = Timing.Timer(float(7.0))

	TillTitle      = Timing.Timer(2.0)
	TillVersion    = Timing.Timer(1.2)
	TillFadeToGrey = Timing.Timer(TillTitle.EndTime + 4.2)

	TillTitle_ToWhite   = Timing.Timer(0.134)
	TillVersion_ToWhite = Timing.Timer(0.134)

	TillFadeOut = Timing.Timer(0.134)

	Loaded = False

	IntroTitle    = "Trial By Fire Engine"
	EngineVersion = "Type Python"

	RenderTitle   = False
	RenderVersion = False

	Title_Cells   = Renderer.CellPacket()
	Version_Cells = Renderer.CellPacket()



StateObj = IntroState()



def GetState() : return StateObj