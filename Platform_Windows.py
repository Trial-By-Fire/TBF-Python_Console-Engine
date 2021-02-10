from LAL import constant
from STL import Enum
from STL import OS
from STL import SYS


import pyuac        as UAC
import win32api     as API
import win32con     as Con
import win32console as Console
import win32event   as Event
import win32gui     as GUI    
import win32process as Process



ConsoleScreenBufferType = Console.PyConsoleScreenBufferType
CreateCoord             = Console.PyCOORDType
CreateSmallRect         = Console.PySMALL_RECTType

SetWindowPosition  = GUI.SetWindowPos
SetConsoleTitle    = Console.SetConsoleTitle
CreateScreenBuffer = Console.CreateConsoleScreenBuffer

MainScreenWidth  = API.GetSystemMetrics(Con.SM_CXSCREEN)
MainScreenHeight = API.GetSystemMetrics(Con.SM_CYSCREEN)


class EKeyCode () :

	None_       = 0x00
	Arrow_Up    = Con.VK_UP
	Arrow_Down  = Con.VK_DOWN
	Arrow_Left  = Con.VK_LEFT
	Arrow_Right = Con.VK_RIGHT
	Enter       = Con.VK_RETURN
	Tab         = Con.VK_TAB


class CAttribute () :

	FG_Red       = Console.FOREGROUND_RED
	FG_Green     = Console.FOREGROUND_GREEN
	FG_Blue      = Console.FOREGROUND_BLUE
	FG_Intensity = Console.FOREGROUND_INTENSITY
	BG_Red       = Console.BACKGROUND_RED
	BG_Green     = Console.BACKGROUND_GREEN
	BG_Blue      = Console.BACKGROUND_BLUE
	BG_Intensity = Console.BACKGROUND_INTENSITY



__AllocatedConsole = False



CConsole_WhiteCell     = int(CAttribute.FG_Red | CAttribute.FG_Green | CAttribute.FG_Blue | CAttribute.FG_Intensity)
CConsole_CursorMinSize = int(1)
CHandle_Top            = int(Con.HWND_TOP)
CWindowFlag_NoSize     = int(Con.SWP_NOSIZE)



def RequestConsole() :

	if Console.GetConsoleWindow() == 0 :

		print("Need to allocate console...")

		Console.AllocConsole()

		__AllocatedConsole = True

	return Console.GetConsoleWindow()


def ReleaseConsole() :

	if __AllocatedConsole :

		Console.FreeConsole()


def GetKeySignal(_keyCode) :

	if API.GetAsyncKeyState(_keyCode) == 0 : return False
	else                                   : return True


def Main() :

	import Execution

	Execution.Entrypoint()

	input()