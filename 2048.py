import pygame,random,time
from copy import deepcopy

SIZE = (450,450)
WHITE = (255,255,255)
BLACK = (0,0,0)
EMPTYCELLBACKGROUND = (204,204,179)
NUMBERCELLBACKGROUND = (191,242,155)
BACKGROUND = (255,153,153)
BOARDX, BOARDY = 4,4

CELLCOLOURS = {
    1:(204,204,179),
    2:(239,239,200),
    4:(228,228,161),
    8:(255,174,25),
    16:(255,64,0),
    32:(255,26,0),
    64:(255,0,0),
    128:(255,231,102),
    256:(255,227,76),
    512:(255,223,50),
    1024:(255,219,25),
    2048:(255,215,0),
    4096:(223,66,97),
    8192:(227,24,64),
    16384:(169,12,12),
    32768:(31,199,223),
    65536:(71,161,174)
    }

class BoardCell():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = ((SIZE[0] - ( (BOARDX+1) * 10 )) / BOARDX)
        self.height = ((SIZE[1] - ( (BOARDY+1) * 10 )) / BOARDY)
        self.value = 1
    def getImage(self):
        pygame.draw.rect(screen,CELLCOLOURS[self.value],(self.x,self.y,self.width,self.height),0)
        if self.value != 1:
            renderText(str(self.value),20,BLACK,self.x + self.width/2 - 5,self.y + self.height / 2)
    def getAnimateImage(self,x,y):
        pygame.draw.rect(screen,CELLCOLOURS[self.value],(x,y,self.width,self.height),0)
        if self.value != 1:
            renderText(str(self.value),20,BLACK,x + self.width/2 - 5,y + self.height / 2)
    def increaseValue(self):
        self.value *= 2
    def getValue(self):
        return self.value
    def setValue(self,n):
        self.value = n
    def getX(self):
        return self.x
    def getY(self):
        return self.y
        
def renderText(text,fontSize,colour,x,y):
    font = pygame.font.SysFont("monospace", fontSize)
    text = screen.blit((font.render(text, 1, colour)),(x,y))
    return text

def setBoard():
    x = 10
    y = 10
    for i in range(BOARDY):
        for k in range(BOARDX):
            board[i][k] = BoardCell(x,y)
            x+= ((SIZE[0] - ( (BOARDX+1) * 10 )) / BOARDX) + 10
        x = 10
        y+= ((SIZE[1] - ( (BOARDY+1) * 10 )) / BOARDY) + 10

def showBoard():
    for i in range(BOARDY):
        for k in range(BOARDX):
            board[i][k].getImage()

def getRandomCell():
    cells = []
    for i in range(BOARDY):
        for k in range(BOARDX):
            if board[i][k].getValue() == 1:
                cells.append(board[i][k])
    return random.choice(cells)

def getNumberOfValidMoves():
    possible_moves = 0
    for i in range(BOARDY):
        for k in range(BOARDX):
            if board[i][k].getValue() != 1:
                if i - 1 >= 0:
                    if board[i-1][k].getValue() == board[i][k].getValue() or board[i-1][k].getValue() == 1:
                        possible_moves += 1
                if i + 1 < BOARDX:
                    if board[i+1][k].getValue() == board[i][k].getValue() or board[i+1][k].getValue() == 1:
                        possible_moves += 1
                if k - 1 >= 0:
                    if board[i][k-1].getValue() == board[i][k].getValue() or board[i][k-1].getValue() == 1:
                        possible_moves += 1
                if k + 1 < BOARDY:
                    if board[i][k+1].getValue() == board[i][k].getValue() or board[i][k+1].getValue() == 1:
                        possible_moves += 1
    return possible_moves

def moveCell(i,k,counter,limit,mod,direction):      
    counti = counter[0]
    countk = counter[1]
    source = board[i][k]
    if direction in ["up","down"]:
        count = i + counti
    else:
        count = k + countk
    destination = None
    if count != limit:
        while True:
            if board[i+counti][k+countk].getValue() != 1:
                if board[i+counti][k+countk].getValue() == source.getValue():
                    board[i+counti][k+countk].increaseValue()
                    destination = board[i+counti][k+countk]
                    break
                else:
                    board[i+counti+mod[0]][k+countk+mod[1]].setValue(source.getValue())
                    if board[i+counti+mod[0]][k+countk+mod[1]]!=source:
                        destination = board[i+counti+mod[0]][k+countk+mod[1]]
                    break
            elif count == abs(limit)-1:
                board[i+counti][k+countk].setValue(source.getValue())
                destination = board[i+counti][k+countk]
                break
            counti += counter[0]
            countk += counter[1]
            count += counter[0]
            count += counter[1]
    return destination

def hasMoved(preboard,board):
    a = []
    b = []
    for i in range(BOARDY):
        for k in range(BOARDX):
            a.append(preboard[i][k].getValue())
            b.append(board[i][k].getValue())
    return a!=b

def Animate(source,dest):
    source_x = source.getX()
    source_y = source.getY()
    dest_x = dest.getX()
    dest_y = dest.getY()
    move = 15#4

    tempValue = dest.getValue()
    dest.setValue(1)
    if source_x - dest_x == 0:
        if source_y < dest_y:
            while source_y < dest_y:
                source.getAnimateImage(source_x,source_y)
                source_y += move
                pygame.display.update()
        else:
            while source_y > dest_y:
                source.getAnimateImage(source_x,source_y)
                source_y -= move
                pygame.display.update()

    elif source_y - dest_y == 0:
        if source_x < dest_x:
            while source_x < dest_x:
                source.getAnimateImage(source_x,source_y)
                source_x += move
                pygame.display.update()
        else:
            while source_x > dest_x:
                source.getAnimateImage(source_x,source_y)
                source_x -= move
                pygame.display.update()
    dest.setValue(tempValue)

def render():
    clock.tick(32)
    screen.fill(BACKGROUND)
    showBoard()
    pygame.display.update()

def events():
    direction = ""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = "left"
            elif event.key == pygame.K_RIGHT:
                direction = "right"
            elif event.key == pygame.K_UP:
                direction = "up"
            elif event.key == pygame.K_DOWN:
                direction = "down"
            elif event.key == pygame.K_SPACE: # FOR TESTING CREATE BLOCK WITH SPACE
                getRandomCell().increaseValue()

    if direction == "right":
        a1,b1,c1 = 0,BOARDY,1
        a2,b2,c2 = BOARDX-1,-1,-1
        count = [0,1] #count = i+0, k + 1
        limit = BOARDX
        modder = [0,-1]
    elif direction == "left":
        a1,b1,c1 = 0,BOARDY,1
        a2,b2,c2 = 0,BOARDX,1
        count = [0,-1] #count = i+0, k - 1
        limit = -1
        modder = [0,1]
    elif direction == "up":
        a1,b1,c1 = 0,BOARDY,1
        a2,b2,c2 = 0,BOARDX,1
        count = [-1,0] #count = i - 1, k+0
        limit = -1
        modder = [1,0]
    elif direction == "down":
        a1,b1,c1 = BOARDY-1,-1,-1
        a2,b2,c2 = 0,BOARDX,1
        count = [1,0] #count = i + 1, k+0
        limit = BOARDY
        modder = [-1,0]
    if direction in ["right","left","up","down"]:
        preboard = deepcopy(board)
        for i in range(a1,b1,c1):
            for k in range(a2,b2,c2):
                if board[i][k].getValue() != 1:
                    destination = moveCell(i,k,count,limit,modder,direction)
                    if destination != None:
                        Animate(board[i][k],destination)
                        board[i][k].setValue(1)
        moved = hasMoved(preboard,board)
        if moved:
            getRandomCell().increaseValue()

def gameOver():
    while True:
        screen.fill(BLACK)
        renderText("GAME OVER",50,WHITE,(SIZE[0]//2)/3,(SIZE[1]//2)/4)
        pygame.display.update()

def main():
    setBoard()
    getRandomCell().increaseValue()
    getRandomCell().increaseValue()
    while True:
        render()
        events()
        if getNumberOfValidMoves() == 0:
            gameOver()
            break


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.quit()
    pygame.display.set_caption('2048')
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    board = [[None for i in range(BOARDX)] for dimensions in range(BOARDY)]
    main()
