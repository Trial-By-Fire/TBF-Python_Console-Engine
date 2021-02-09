from Platform_Windows import CreateCoord
from OSPlatform import Platform;


from Config import Debug;
from LAL    import constant;
from STL    import Arrays;
from STL    import Copy;
from STL import SYS;
from STL import OS;


CAttribute = Platform.CAttribute;


BufferWidth = 80;

if Debug.Enabled : BufferHeight = 48;
else             : BufferHeight = 24;

BorderLineRow   = 24;
DebugStart      = 25;
LogSize         = 18;
PersistentStart = 44;
PersistentSize  = 4;
GameEnd         = 23;



class Vec2D :

	X = int;
	Y = int;

class CellPacket :

	def WriteToBuffer(self) :

		global Buffer; 

		if (Buffer[0] == None) :

			Buffer[0] = self;

		else :

			Buffer = Arrays.append(Buffer, self);

	def Draw(self) :

		global ConsoleScreenBuffer;

		ConsoleScreenBuffer.SetConsoleTextAttribute(self.Attribute);
		
		ConsoleScreenBuffer.WriteConsoleOutputCharacter(Characters = self.String, WriteCoord = self.Position);	


	String    = "";
	Attribute = int;
	Position  = Platform.CreateCoord(X = 0, Y = 0);



GameBorder       = CellPacket();
PersistentBorder = CellPacket();

GameScanline       = CellPacket();
GameScanline_Pos   = Vec2D; 
GameScanline_Pos.X = 0; 
GameScanline_Pos.Y = 0;

ScreenCenter   = Vec2D;
ScreenCenter.X = int(Platform.MainScreenWidth  / 2);
ScreenCenter.Y = int(Platform.MainScreenHeight / 2);

ScreenPosition   = Vec2D;
ScreenPosition.X = (ScreenCenter.X - (int(BufferWidth / 2) * 8)) - 20;
ScreenPosition.Y = (ScreenCenter.Y - (int(BufferWidth / 2) * 8)) - 200;

ConsoleHandle       = int();
ConsoleScreenBuffer = None;
CoordSize           = Platform.CreateCoord( X = BufferWidth, Y = BufferHeight );
CSBI_Instance       = None; 
BufferSize          = BufferWidth * BufferHeight;
Console_Coord       = Platform.CreateSmallRect(Left = 0, Top = 0, Right = BufferWidth - 1, Bottom = BufferHeight - 1);
RefreshTimer        = 1.0 / 60.0;

Buffer = Arrays.empty(1, dtype = CellPacket);

Buffer;



def SetupConsole() :

	global ConsoleHandle, ConsoleScreenBuffer, CoordSize, Console_Coord, ScreenPosition;

	ConsoleHandle = Platform.RequestConsole();

	Platform.SetConsoleTitle("TBF Engine: Type Python");

	if ConsoleHandle == 0 :

		raise RuntimeError("Renderer: RequestConsole failed.");

	ConsoleScreenBuffer = Platform.CreateScreenBuffer();

	if ConsoleScreenBuffer == 0 :

		raise RuntimeError("Renderer: Failed to create a console screen buffer.");

	ConsoleScreenBuffer.SetConsoleActiveScreenBuffer();

	ConsoleScreenBuffer.SetConsoleTextAttribute(Platform.Console_WhiteCell);

	ConsoleScreenBuffer.WriteConsole(u"Renderer:: Console Created");

	ConsoleScreenBuffer.SetConsoleScreenBufferSize(Size = CoordSize);

	ConsoleScreenBuffer.SetConsoleCursorInfo(Size = Platform.Console_CursorMinSize, Visible = True);

	ConsoleScreenBuffer.SetConsoleWindowInfo(Absolute = True, ConsoleWindow = Console_Coord);

	ConsoleScreenBuffer.SetConsoleScreenBufferSize(Size = CoordSize);

	ConsoleScreenBuffer.SetConsoleWindowInfo(Absolute = True, ConsoleWindow = Console_Coord);

	ConsoleScreenBuffer.SetConsoleCursorInfo(Size = Platform.Console_CursorMinSize, Visible = True);

	Platform.SetWindowPosition(
		ConsoleHandle, 
		Platform.Handle_Top, 
		ScreenPosition.X, 
		ScreenPosition.Y,
		0,
		0,
		Platform.WindowFlag_NoSize
	);


def DrawGameScanline() :

	global GameEnd, GameScanline, GameScanline_Pos;

	GameScanline.Position = CreateCoord(X = 0, Y = GameScanline_Pos.Y);

	GameScanline.WriteToBuffer();

	GameScanline_Pos.Y += 1;

	if GameScanline_Pos.Y > GameEnd :

		GameScanline_Pos.Y = 0;


def ResetDrawPosition() :

	global ConsoleScreenBuffer; 
	
	ConsoleScreenBuffer.SetConsoleCursorPosition(Platform.CreateCoord(X = 0, Y = 0));


EmptyBuffer = "";

for index in range(BufferSize - 1) :

	EmptyBuffer += " ";

def Clear() :

	global Buffer, ConsoleScreenBuffer, EmptyBuffer; 
	
	Buffer = Arrays.empty(1, dtype = CellPacket);

	ConsoleScreenBuffer.SetConsoleTextAttribute(0);

	ConsoleScreenBuffer.WriteConsoleOutputCharacter(Characters = EmptyBuffer, WriteCoord = CreateCoord(X = 0, Y = 0) );


def RenderFrame() :

	global Buffer;

	for index in range(Buffer.size) :

		Buffer[index].Draw();


def LoadModule() :

	global GameBorder, PersistentBorder, Buffer, BufferSize, BorderLineRow, PersistentStart;

	GameBorder.Attribute = Platform.Console_WhiteCell;
	GameBorder.Position  = Platform.CreateCoord(X = 0, Y = BorderLineRow);

	for index in range(BufferWidth -1) :

		GameBorder.String = GameBorder.String + "=";

	PersistentBorder = Copy.copy(GameBorder);

	PersistentBorder.Position = Platform.CreateCoord(X = 0, Y = PersistentStart - 1);

	for index in range(BufferWidth - 1) :

		GameScanline.String = GameScanline.String + "-";

	GameScanline.Attribute = CAttribute.BG_Intensity;

	SetupConsole();


def UnloadModule() :

	Platform.ReleaseConsole();

totalDelta = 0.0;


def Update() :

	import time;

	global totalDelta, GameBorder, PersistentBorder;

	delta = 0.0;

	deltaSec = 0.0;

	deltaInterval = 1.0 / 60.0;

	cyclerTimeInit = time.time_ns();

	if Debug.Enabled and totalDelta > deltaInterval:

		totalDelta = 0.0;

		# OS.system('cls');

		Clear();	

		ResetDrawPosition();

		DrawGameScanline();

		GameBorder.WriteToBuffer();

		PersistentBorder.WriteToBuffer();

		RenderFrame();

	cyclerTimeEnd = time.time_ns();

	delta = cyclerTimeEnd - cyclerTimeInit;

	deltaSec = delta / 100000000;

	totalDelta += deltaSec;