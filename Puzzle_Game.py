import pygame
from pathlib import Path
pygame.init()
pygame.display.set_caption("Puzzle Game")

#ObjectsColor
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WALLColor = (102, 82, 31)
PLAYERColor = (255, 0, 0)
GOALColor = (63, 239, 242)
BOXColor =(67, 128, 24)

window = pygame.display.set_mode((600, 600))
window.fill(WHITE)

levels_folder = Path("Levels/")
#ReadingTheGameMapFromFile
def load(Level):
    level_to_open = levels_folder / Level
    l= list(level_to_open.read_text())
    Grid=[]
    while "\n" in l:
        i=l.index("\n") 
        Grid.append(l[:i])
        del l[0:i+1]
    del Grid[-1]
    return Grid

#TurningGridIntoPositionsOfObjects
def GridToPos(Grid,Object):
    Positions=[]
    for i in range(10):
        for j in range(10):
            if Grid[i][j]==Object:
                Positions.append([j,i])
    return Positions

#LoadingDifferentLevels
def LevelUp():
    global isRunning
    global GRID
    if level==1:
        GRID=load("Level1.txt")
    elif level==2:
        GRID=load("Level2.txt")
    elif level==3:
        GRID=load("Level3.txt")
    else:
        isRunning = False
    window.fill(WHITE)
    Wall= GridToPos(GRID,"w")
    Box= GridToPos(GRID,"b")
    Moves=GridToPos(GRID,"p")
    Goal=GridToPos(GRID,"g")
    return Wall,Box,Moves,Goal

#DrawingFunctions
def Movement(Position,Color,Radius):
    pygame.draw.circle(window,Color,(Position[0]*60+30,Position[1]*60+30),Radius)
    pygame.display.update()

def linedraw(start,end):
    pygame.draw.line(window,BLACK,start,end,1)

def rectdraw(Rect,Color):
    pygame.draw.rect(window,Color,Rect)

def circledraw(Position,Color):
    pygame.draw.circle(window,Color,Position,30)

#StartingWithTheFirstLevel
level=1
Wall,Box,Moves,Goal=LevelUp()


#PushingFunctions
def PushPos(Pusher,Pushed):
    NewPlace=[]
    if Pushed[1]>Pusher[1]:
        NewPlace=[Pushed[0],Pushed[1]+1]
    elif Pushed[1]<Pusher[1]:
        NewPlace=[Pushed[0],Pushed[1]-1]
    elif Pushed[0]>Pusher[0]:
        NewPlace=[Pushed[0]+1,Pushed[1]]
    elif Pushed[0]<Pusher[0]:
        NewPlace=[Pushed[0]-1,Pushed[1]]
    return NewPlace

def PushDraw(Pusher,Pushed,PusherColor,PushedColor,PusherRadius,PushedRadius):
    NPlace=PushPos(Pusher,Pushed)
    if (NPlace not in Wall) and (NPlace not in Goal): #BlockingBoxesByWallsAndGoal
        Box.append(NPlace)
        Movement(NPlace,PushedColor,PushedRadius)
        Movement(Pushed,WHITE,PushedRadius)
        Box.remove(Pushed)
        Movement(Pushed,PusherColor,PusherRadius)
        Movement(Pusher,WHITE,PusherRadius)
    else:
        Moves.remove(Moves[-1])

def BoxPushBox(Box1,Box2):
    if PushPos(Box1,Box2) not in Box:
        PushDraw(Box1,Box2,BOXColor,BOXColor,30,30)
    else:
        BoxPushBox(Box2,PushPos(Box1,Box2))

isRunning = True
while isRunning:

    #DrawingTheGame
    circledraw((Goal[0][0]*60+30,Goal[0][1]*60+30),GOALColor)
    for eachwall in Wall:
        rectdraw((eachwall[0]*60, eachwall[1]*60, 60, 60),WALLColor)
    for eachbox in Box:
        circledraw((eachbox[0]*60+30,eachbox[1]*60+30),BOXColor)
    for row in range(10):
        linedraw((0,row*60),(600,row*60))
    for column in range(10):
        linedraw((column*60,0),(column*60,600))

    #KeysControl
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type==pygame.KEYDOWN:
            moveDir=[]
            if event.key==pygame.K_DOWN:
                moveDir=[Moves[-1][0],Moves[-1][1]+1]
            elif event.key==pygame.K_UP:
                moveDir=[Moves[-1][0],Moves[-1][1]-1]
            elif event.key==pygame.K_LEFT:
                moveDir=[Moves[-1][0]-1,Moves[-1][1]]
            elif event.key==pygame.K_RIGHT:
                moveDir=[Moves[-1][0]+1,Moves[-1][1]]
            Moves.append(moveDir)

            if event.key==pygame.K_z:
                Moves.remove(Moves[-1])
                Movement(Moves[-1],WHITE,30)
                Moves.remove(Moves[-1])
                Movement(Moves[-1],PLAYERColor,20)

    #ReachingTheGoal
    if Moves[-1] in Goal:
        level+=1
        Wall,Box,Moves,Goal=LevelUp()
        
    #BlockingPlayerByWalls
    elif Moves[-1] in Wall:
        Moves.remove(Moves[-1])

    #MovingPlayerInEmptySpace
    elif Moves[-1] not in Box:
        Movement(Moves[-1],PLAYERColor,20)
        if len(Moves)>1:
            Movement(Moves[-2],WHITE,20)       

    #PushingBoxesByPlayer
    else:
        j = Box[Box.index(Moves[-1])]
        NNPlace= PushPos(Moves[-2],j)
        if NNPlace not in Box:
            PushDraw(Moves[-2],j,PLAYERColor,BOXColor,20,30)
        else:
            BoxPushBox(j,NNPlace)

    pygame.display.update()

