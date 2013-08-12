import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint


class Snake(object):
    def __init__(self):
        self.loc=[[2,5],[2,4],[2,3],[2,2]]
        self.orient='R'
        self.score=0
        self.death=0
    def draw(self):
        for i in self.loc:
            win.addch(i[0], i[1], '*') 
    def headmove(self,orient,food):
        if orient=='L':
            self.loc[0][1]-=1
        elif orient=='R':
            self.loc[0][1]=self.loc[0][1]+1
        elif orient=='U':
            self.loc[0][0]-=1
        else:
            self.loc[0][0]+=1
            
        if self.loc[0]==food.position:
            food.new(self)
            self.loc.append(self.tail)
            self.score=self.score+1
        if self.loc[0][0]==0 or self.loc[0][0]==14 or self.loc[0][1]==0 or self.loc[0][1]==29:
            self.death=1
        elif self.loc[0] in self.loc[1:]:
            self.death=1   
            
    def bodyfollow(self):
        self.tail=self.loc[3]
        for i in range(len(self.loc)-1,0,-1):
            self.loc[i]=self.loc[i-1][:]
    def advance(self,key,food):

        if key==-1:
            self.bodyfollow()
            self.headmove(self.orient,food)
        elif key==KEY_RIGHT and self.orient!='L':
            self.bodyfollow()
            self.headmove('R',food)
            self.orient='R'
        elif key==KEY_LEFT and self.orient!='R':
            self.bodyfollow()
            self.headmove('L',food)
            self.orient='L'
        elif key==KEY_UP and self.orient!='D':
            self.bodyfollow()
            self.headmove('U',food)
            self.orient='U'
        elif key==KEY_DOWN and self.orient!='U':
            self.bodyfollow()
            self.headmove('D',food)
            self.orient='D'
        else:
            pass

class Food(object):
    def __init__(self):
        self.position=[randint(1,13),randint(1,28)]
    def new(self,snake):
        self.position=[randint(1,13),randint(1,28)]
        while self.position in snake.loc:
            self.position=[randint(1,13),randint(1,28)]
    def draw(self):
        win.addch(self.position[0], self.position[1], '*',curses.color_pair(1))
            
        
    
snake=Snake()
food=Food()

curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
win = curses.newwin(15, 30, 4, 25)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

while True:
    if snake.death==1:
        break
        
    if snake.score<5:
        t=500
    elif snake.score<15:
        t=400
    elif snake.score<30:
        t=300
    elif snake.score<50:
        t=200
    else:
        t=100
    win.erase()
    win.border(0)
    win.addstr(0,4," Score:"+str(snake.score)+' ',curses.color_pair(3))
    win.addstr(14,6," Xiang Li Sha Bi! ",curses.color_pair(2))
    snake.draw()
    food.draw()
    win.timeout(t)         
    key = win.getch()
    snake.advance(key,food)

curses.endwin()
print "Game over!"
print "Your score is %d" %snake.score
