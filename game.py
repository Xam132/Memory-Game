import pygame,sys,random
from pygame.locals import *

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BOARD_WIDTH = 2     # in terms of num of icons
BOARD_HEIGHT = 2     # in terms of num of icons
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10

assert (BOARD_WIDTH * BOARD_HEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'

XMARGIN = (WINDOW_WIDTH - (BOARD_WIDTH * (BOXSIZE + GAPSIZE))) // 2
YMARGIN = (WINDOW_HEIGHT - (BOARD_HEIGHT * (BOXSIZE + GAPSIZE))) // 2

GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = ORANGE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOL = (RED, GREEN, BLUE, YELLOW, PURPLE, CYAN)
ALLSYM = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

assert (len(ALLCOL) * len(ALLSYM) * 2 >= BOARD_WIDTH * BOARD_HEIGHT), "Board is too big for the number of shapes/colors defined."

def random_board():
    icon = [(i,j) for i in ALLSYM for j in ALLCOL]
    random.shuffle(icon)
    num_icon = BOARD_WIDTH * BOARD_HEIGHT // 2
    icon = icon[:num_icon] * 2
    random.shuffle(icon)
    board = [[icon[i*BOARD_HEIGHT + j]for j in range(BOARD_HEIGHT)]for i in range(BOARD_WIDTH)]
    return board

def coords(boxx,boxy):
    corx = XMARGIN + boxx * (GAPSIZE + BOXSIZE)
    cory = YMARGIN + boxy * (GAPSIZE + BOXSIZE)
    return (corx,cory)

def draw_icon(sym,col,corx,cory):
    quar = BOXSIZE // 4
    half = BOXSIZE // 2
    left,top = coords(corx,cory)
    if sym == DONUT:
        pygame.draw.circle(DISPLAYSURF,col,(left+half,top+half),half-5)
        pygame.draw.circle(DISPLAYSURF,BGCOLOR,(left+half,top+half),quar-5)
    elif sym == SQUARE:
        pygame.draw.rect(DISPLAYSURF,col,(left+quar,top+quar,half,half))
    elif sym == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF,col,((left+half,top+quar),(left+half+quar,top+half),
                                             (left+half,top+half+quar),(left+quar,top+half)))
    elif sym == LINES:
        for i in range(4,BOXSIZE,4):
            pygame.draw.line(DISPLAYSURF,col,(left+4,top+i),(left+i,top+4),2)
            pygame.draw.line(DISPLAYSURF,col,(left+BOXSIZE-4,top+BOXSIZE-i),(left+BOXSIZE-i,top+BOXSIZE-4),2)
    elif sym == OVAL:
        pygame.draw.ellipse(DISPLAYSURF,col,(left+quar,top+quar,half,half))

def reveal_board(val):
    rev_board = [[val for j in range(BOARD_HEIGHT)] for i in range(BOARD_WIDTH)]
    return rev_board

def box_Cover(board,boxes,coverage):
    for box in boxes:
        left,top = coords(box[0],box[1])
        pygame.draw.rect(DISPLAYSURF,BGCOLOR,(left,top,BOXSIZE,BOXSIZE))
        shape,color = board[box[0]][box[1]][0],board[box[0]][box[1]][1]
        draw_icon(shape,color,box[0],box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,coverage,BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS//2)

def reveal_Cover_Animation(board,boxes):
    for coverage in range(BOXSIZE,-REVEALSPEED+1,-REVEALSPEED):
        box_Cover(board,boxes,coverage)

def close_Cover_Animation(board,boxes):
    for coverage in range(0,BOXSIZE+REVEALSPEED-1,REVEALSPEED):
        box_Cover(board,boxes,coverage)

def boxAtLoc(x,y):
    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left,top = coords(boxx,boxy)
            box = pygame.Rect(left,top,BOXSIZE,BOXSIZE)
            if box.collidepoint(x,y):
                return (boxx,boxy)
    return (None,None)

def startAnimation(board):
    boxes = [(i,j) for i in range(BOARD_WIDTH) for j in range(BOARD_HEIGHT)]
    random.shuffle(boxes)
    board1 = reveal_board(False)
    draw_board(board,board1)
    for i in range(0,len(boxes),8):
        reveal_Cover_Animation(board,boxes[i:i+8])
        close_Cover_Animation(board,boxes[i:i+8])

def win_animation(board):
    rev_board = reveal_board(True)
    col1, col2 = LIGHTBGCOLOR, BGCOLOR
    for i in range(11):
        col1, col2 = col2, col1
        DISPLAYSURF.fill(col1)
        draw_board(board,rev_board)
        pygame.display.update()
        pygame.time.wait(500)

def has_won(board):
    for i in board:
        if False in i:
            return False
    return True

def draw_board(board,rev_board):
    for boxx in range(0,BOARD_WIDTH):
        for boxy in range(0,BOARD_HEIGHT):
            left,top = coords(boxx,boxy)
            pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left-4,top-4,BOXSIZE+8,BOXSIZE+8),4)
            if rev_board[boxx][boxy]:
                sym, col = board[boxx][boxy][0], board[boxx][boxy][1]
                draw_icon(sym,col,boxx,boxy)
            else:
                pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,BOXSIZE,BOXSIZE))

def highlight_box(boxx,boxy):
    left,top = coords(boxx,boxy)
    pygame.draw.rect(DISPLAYSURF,HIGHLIGHTCOLOR,(left-4,top-4,BOXSIZE+8,BOXSIZE+8),4)

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Memory Game / Concentration")
    board = random_board()
    rev_board = reveal_board(False)
    DISPLAYSURF.fill(BGCOLOR)
    startAnimation(board)
    first_sel = None
    mousex,mousey = 0,0
    while True:
        mouseClick = False
        DISPLAYSURF.fill(BGCOLOR)
        draw_board(board,rev_board)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClick = True
        boxx,boxy = boxAtLoc(mousex,mousey)
        if boxx != None and boxy != None:
            if not rev_board[boxx][boxy]:
                highlight_box(boxx,boxy)
            if not rev_board[boxx][boxy] and mouseClick:
                reveal_Cover_Animation(board,[(boxx,boxy)])
                rev_board[boxx][boxy] = True
                if first_sel == None:
                    first_sel = (boxx,boxy)
                else:
                    item1 = board[boxx][boxy]
                    item2 = board[first_sel[0]][first_sel[1]]
                    if item1 != item2:
                        pygame.time.wait(1000)
                        close_Cover_Animation(board,[first_sel,(boxx,boxy)])
                        rev_board[boxx][boxy] = False
                        rev_board[first_sel[0]][first_sel[1]] = False
                    elif has_won(rev_board):
                        win_animation(board)
                        pygame.time.wait(2000)
                        board = random_board()
                        rev_board = reveal_board(False)
                        draw_board(board, rev_board)
                        startAnimation(board)
                    first_sel = None
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()


