from Platform_Windows import CAttribute, CreateCoord
from OSPlatform       import Platform


from Config import Debug
from LAL    import constant
from STL    import Arrays
from STL    import Copy
from STL    import SYS
from STL    import OS

import State
import Timing


CellAttribute = Platform.CAttribute


CBufferWidth = 80

if Debug.Enabled : CBufferHeight = 48
else             : CBufferHeight = 24

CBorderLineRow   = 24
CDebugStart      = 25
CLogSize         = 18
CPersistentStart = 44
CPersistentSize  = 4
CGameEnd         = 23



class Vec2D :

	X = int
	Y = int

class CellPacket :

	def SetAttribute(self, _attribute) :

		self._AttribBuf = []

		for index in range(len(self.String)) :

			self._AttribBuf.append(_attribute);


	def WriteToBuffer(self) :

		global _Buffer, _BufferSize

		if self.String == '' : return

		if _Buffer[0] == None :

			_Buffer[0] = self

		else :

			_Buffer = Arrays.append(_Buffer, self)


	def Draw(self) :

		global _CSB;
		
		_CSB.WriteConsoleOutputCharacter(Characters = self.String, WriteCoord = self.Position)

		_CSB.WriteConsoleOutputAttribute(Attributes = self._AttribBuf, WriteCoord = self.Position)


	String    = ""
	Position  = Platform.CreateCoord(X = 0, Y = 0)
	_AttribBuf = None



_GameBorder       = CellPacket()
_PersistentBorder = CellPacket()

_GameScanline   = CellPacket()
_GameScanline_Y = int()

_ScreenCenter   = Vec2D
_ScreenCenter.X = int(Platform.MainScreenWidth  / 2)
_ScreenCenter.Y = int(Platform.MainScreenHeight / 2)

_ScreenPosition   = Vec2D
_ScreenPosition.X = (_ScreenCenter.X - (int(CBufferWidth / 2) * 8)) - 20
_ScreenPosition.Y = (_ScreenCenter.Y - (int(CBufferWidth / 2) * 8)) - 200

_ConsoleHandle = int()
_CSB_Front     = None
_CSB_Back      = None;
_CSB           = None;
_CoordSize     = Platform.CreateCoord( X = CBufferWidth, Y = CBufferHeight )
_BufferSize    = CBufferWidth * CBufferHeight
_Console_Coord = Platform.CreateSmallRect(Left = 0, Top = 0, Right = CBufferWidth - 1, Bottom = CBufferHeight - 1)
_RefreshTimer  = Timing.Timer(1.0 / 30.0)

_Buffer = Arrays.empty(1, dtype = CellPacket)

_DebugLog = Arrays.empty(1, dtype = str)

_PersistentSection = Arrays.array([CellPacket(), CellPacket(), CellPacket(), CellPacket()])



def SetupConsole() :

	global _ConsoleHandle, _CSB_Front, _CSB_Back, _CSB, _CoordSize, _Console_Coord, _ScreenPosition

	_ConsoleHandle = Platform.RequestConsole()

	Platform.SetConsoleTitle("TBF Engine: Type Python")

	if _ConsoleHandle == 0 :

		raise RuntimeError("Renderer: RequestConsole failed.")

	_CSB_Front = Platform.CreateScreenBuffer()

	_CSB_Back = Platform.CreateScreenBuffer()

	if _CSB_Front == 0 or _CSB_Back == 0:

		raise RuntimeError("Renderer: Failed to create a console screen buffer.")

	_CSB_Front.SetConsoleActiveScreenBuffer()

	_CSB_Front.SetConsoleScreenBufferSize(Size = _CoordSize)

	_CSB_Front.SetConsoleCursorInfo(Size = Platform.CConsole_CursorMinSize, Visible = False)

	_CSB_Front.SetConsoleWindowInfo(Absolute = True, ConsoleWindow = _Console_Coord)

	_CSB_Front.SetConsoleScreenBufferSize(Size = _CoordSize)

	_CSB_Front.SetConsoleWindowInfo(Absolute = True, ConsoleWindow = _Console_Coord)

	_CSB_Front.SetConsoleCursorInfo(Size = Platform.CConsole_CursorMinSize, Visible = False)

	_CSB_Back.SetConsoleScreenBufferSize(Size = _CoordSize)

	_CSB_Back.SetConsoleCursorInfo(Size = Platform.CConsole_CursorMinSize, Visible = False)

	_CSB_Back.SetConsoleWindowInfo(Absolute = True, ConsoleWindow = _Console_Coord)

	_CSB_Back.SetConsoleScreenBufferSize(Size = _CoordSize)

	_CSB_Back.SetConsoleWindowInfo(Absolute = True, ConsoleWindow = _Console_Coord)

	_CSB_Back.SetConsoleCursorInfo(Size = Platform.CConsole_CursorMinSize, Visible = False)

	_CSB = _CSB_Front

	Platform.SetWindowPosition(
		_ConsoleHandle, 
		Platform.CHandle_Top, 
		_ScreenPosition.X, 
		_ScreenPosition.Y,
		0,
		0,
		Platform.CWindowFlag_NoSize
	)


def DrawGameScanline() :

	global CGameEnd, _GameScanline, _GameScanline_Y

	_GameScanline.Position = CreateCoord(X = 0, Y = _GameScanline_Y)

	_GameScanline.WriteToBuffer()

	_GameScanline_Y += 1

	if _GameScanline_Y > CGameEnd :

		_GameScanline_Y = 0


def WriteToLog(_string : str) :

	global _DebugLog 
	
	if Debug.Enabled : 

		_DebugLog = Arrays.append(_DebugLog, _string)


def WriteLogToBuffer() :

	global _DebugLog;

	if Debug.Enabled :

		logRange = CLogSize

		if _DebugLog.size < CLogSize : 
			
			logRange = _DebugLog.size

		for index in range(logRange - 1) :

			LogPacket = CellPacket()

			LogPacket.String = _DebugLog[index + 1]

			LogPacket.SetAttribute(Platform.CConsole_WhiteCell)

			LogPacket.Position = Platform.CreateCoord(X = 0, Y = index + CDebugStart)

			LogPacket.WriteToBuffer()


def WriteToPersistentSection(_index : int, _string : str) :

	global _PersistentSection

	_PersistentSection[_index - 1].String = _string

	_PersistentSection[_index - 1].SetAttribute(Platform.CConsole_WhiteCell)


def WritePersistentSectionToBuffer() :

	global _PersistentSection;

	_PersistentSection[0].WriteToBuffer()
	_PersistentSection[1].WriteToBuffer()
	_PersistentSection[2].WriteToBuffer()
	_PersistentSection[3].WriteToBuffer()


def ResetDrawPosition() :

	global _CSB; _CSB.SetConsoleCursorPosition(Platform.CreateCoord(X = 0, Y = 0))


_EmptyBuffer = CellPacket()

for index in range(_BufferSize) : _EmptyBuffer.String += " "

_EmptyBuffer.SetAttribute(0);

def Clear() :

	global _Buffer, _EmptyBuffer; _Buffer = Arrays.empty(1, dtype = CellPacket)

	_EmptyBuffer.WriteToBuffer()

	_EmptyBuffer.Draw();

	_Buffer = Arrays.empty(1, dtype = CellPacket)


def RenderFrame() :

	global _Buffer

	for index in range(_Buffer.size) : _Buffer[index].Draw()


def LoadModule() :

	global _GameBorder, _PersistentBorder, _Buffer, _BufferSize, CBorderLineRow, CPersistentStart, CPersistentSize, _PersistentSection

	_GameBorder.Position  = Platform.CreateCoord(X = 0, Y = CBorderLineRow)

	for index in range(CBufferWidth) :

		_GameBorder.String = _GameBorder.String + "="

	_GameBorder.SetAttribute(Platform.CConsole_WhiteCell)

	_PersistentBorder = Copy.copy(_GameBorder)

	_PersistentBorder.Position = Platform.CreateCoord(X = 0, Y = CPersistentStart - 1)

	for index in range(CBufferWidth) :

		_GameScanline.String = _GameScanline.String + "-"

	_GameScanline.SetAttribute(Platform.CConsole_WhiteCell)

	for index in range(CPersistentSize) :

		_PersistentSection[index].Position = Platform.CreateCoord(X = 0, Y = CPersistentStart + index)

	SetupConsole()


def UnloadModule() :

	Platform.ReleaseConsole()


def ProcessTiming() :

	_RefreshTimer.Tick()


test = False;

def Update() :

	global _GameBorder, _PersistentBorder, _CSB, _CSB_Front, _CSB_Back

	if _RefreshTimer.Ended():

		if _CSB == _CSB_Front : _CSB = _CSB_Back
		else                  : _CSB = _CSB_Front

		Clear()

		DrawGameScanline()

		WriteLogToBuffer()

		WritePersistentSectionToBuffer()

		State.GetEngineState().Render()

		_GameBorder.WriteToBuffer()

		_PersistentBorder.WriteToBuffer()

		RenderFrame()

		_CSB.SetConsoleActiveScreenBuffer();

		_RefreshTimer.Reset()