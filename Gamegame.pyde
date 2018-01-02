# The developers of this project are Flavia Cereceda, Araz Aslanian and
# Tamara Gjorgjieva. The purpose of the game is to capture the college experience
# at NYUAD by trying to capture falling objects that are 'good' and avoid falling
# objects that are 'bad'. The idea behind the falling objects is the hecticness of
# having your NYUAD responsibilities hitting you in the head. The main objective of
# the player is to SURVIVE, rather than gain points, which is described in the 
# opening screen.

# The game has 4 levels (freshman, sophomore, junior and senior year); as levels
# increment, the total number of object increases, and so does the velocity of 
# their fall.

# The game can also be played with one of 3 animated characters, which is are
# developers themselves. 

# The game difficulty was determined to make the player frustrated and thus eager to 
# play again in order to 'graduate'.

# The game is built with:
#     * screens controlled by a counter
#         - counter controlled by clicker and game conditions
#         - leveling up happens when the player survives the set of objects
#           created for the level 
#     * players that resemble the developers
#         - animated movement
#         - collisions with objects
#     * objects that are either good or bad
#         - collision with a bad object => lose live
#         - collision with a good object => gain points 
    
# Other software used to build the game:
#     * PhotoScape
#     * PhotoShop
#     * Audacity


import random, time, os 
add_library("sound")
path = os.getcwd()

# class Screen is a superclass of all screens used in the game
class Screen:
    def __init__(self):
        self.w = 500
        self.h = 700
        self.bg = loadImage(path + '/' + "backOpening.png")
        self.counter = 0
        self.musicCount = 0
        self.musicCountLose = 0
        self.musicCountWin = 0
        
# the following methods are used to assure that win and lose sounds
# are played only at ONE instance and thus do not overlap 

    def musicPlayer(self):       
        if self.musicCount == 0:
            musicPlay.play()
            self.musicCount += 1
            
    def musicLose(self):
        if self.musicCountLose ==0:
            musicLose.play()
            self.musicCountLose +=1 
            
    def musicWin(self):
         if self.musicCountWin == 0:
            musicWin.play()
            self.musicCountWin += 1 

# method called every time the counter changes, and thus the screen.     
    def flipping(self):
        if self.counter == 4 or self.counter == 5:
            self.counter = 1
        else:
            self.counter += 1 
    
    def display(self):
        background(255)
        textSize(20)
        fill(0)

        # text captures the main objective of the player.
        text ("Welcome to the college game", 115, 295)
        text ("No need to excel", 170, 330)
        text ("You just need to survive", 130, 365)
        
        fill (0)
        rect (150, 630, 200, 40)
        
        textSize(30);
        fill (255)
        text("START GAME", 160, 660)

# subclass of screen, counter = 1
class Instructions(Screen):
    def __init__(self):
        self.bg = loadImage (path + "/" + 'instructions.PNG')
    
    def display(self):
        image (self.bg, 0, 0)    
        
        fill (0)
        rect (150, 630, 200, 40)
        
        textSize(30);
        fill (255)
        text("NEXT", 210, 660)
    
# subclass of screen, counter = 2
class PlayerScreen (Screen):
    def __init__(self):
        
        self.bg = loadImage (path + '/' + 'backOpening.png')
        self.characters = ['Flavia', 'Araz', 'Tami']            
        self.Flavia = loadImage(path + '/' + "Flavia.png")
        self.Araz =  loadImage(path + '/' + "Araz.png")
        self.Tami = loadImage(path + '/' + "Tami.png")
                
    def display(self):            
        image (self.bg, 0, 0)
        image(self.Flavia, 70, 260)
        image(self.Araz, 210, 260)
        image(self.Tami, 350, 260)
        
        textSize(20);
        fill(0)
        
        # us trying to be funny
        if game.tryno == 1:
            text ("Select your player", 150, 200)
            text ("Click on their head", 148, 240)
        
        if game.tryno == 2:
            text ("Maybe try another player?", 120, 200)
            
        if game.tryno > 2:
            text ("Are you ever gonna graduate?", 110, 200)
        
        # printing our names
        self.count = 1    
        for i in self.characters:
            textSize(20);
            fill(0)
            text( str(i).upper() , (75*(self.count*2-1)), 470)
            self.count += 1
        
        textSize(20);
        fill(0)
        text ("They move left. They move right. They jump.", 40, 600)

# subclass of screen, counter = 4            
class LoserScreen (Screen):
    def __init__(self):
        self.bg = loadImage (path + "/" + 'backClosing.png')
        
    def display(self):
        image (self.bg, 0, 0)
        
        fill (255)
        rect (150, 630, 200, 40)
        
        textSize(30);
        fill (0)
        text("TRY AGAIN", 168, 660)

# subclass of screen, counter = 5
class Congratulations (Screen):
    def __init__(self):
        self.bg = loadImage (path + "/" + 'congratulations.png')    
        
    def display(self):
        image (self.bg, 0, 0)
        
        fill (255)
        rect (150, 630, 200, 40)
        
        textSize(30);
        fill (0)
        text("Your final score:" + str (game.score), 110, 600)
        text("PLAY AGAIN", 168, 660)
        print(screen.counter)
        
   
###############################################################################

# main class Game, counter = 3
class Game:
    def __init__(self):
        self.w = 500
        self.h = 700
        self.x = 0
        self.game = False               
        self.level = 1                  
        self.score = 0
        
        self.back = loadImage (path + '/' + "back.png")
        self.grass = loadImage (path + "/" + "grass.png")
        
        # this helps us be funny above
        self.tryno = 1
        
    def startGame(self, character, level):
        self.character = character
        self.level = level
        self.turn = 1
        self.player = Player(100,400,39,self.character,100,360,6)
        self.back = loadImage (path + "/" + "back" + str(self.level) + ".png")
                
        self.objects = []
        self.numObjects = self.level * 15
        
        # the turn alternates between 0 and 1 as the code in Objects
        # is adapted accordingly to have even numbers of good and bad objects
        for x in range (self.numObjects):
            self.turn = (self.turn) % 2
            self.objects.append(Objects(45, self.turn))
            self.turn += 1
            
    def display(self):
        image(self.back, 0, 0, self.w, self.h)
        image(self.grass, 0, self.h*5/7, self.w, self.h*2/7) 
    
        self.player.display()
        
        for x in range (len(self.objects)):
            self.objects[x].display()
        
        # display the scores and lives
        textSize(20);
        fill(255)
        text("Points:" + str (game.score), self.w - 90, self.h - 100)
        
        textSize(20);
        fill(255)
        text("Lives:  " + str(self.player.lives), \
             self.w - 90, self.h - 50)    

###############################################################################
                                         
class Player:
    def __init__ (self, x, y, r, v, w, h, F):
        self.x = x
        self.y = y
        self.r = r
        self.v = v
        self.vx = 0
        self.vy = 0
        self.img = loadImage(path+"\\"+"Walking"+str(self.v)+"PN.png")
        self.w = w
        self.h = h
        self.F = F
        self.f = 0
        self.dir = 1
        self.keyHandler= {LEFT:False,RIGHT:False,UP:False}        
        self.gameOver = False 
        self.lives = 3        
    def update(self):
        self.collision()
        self.x += self.vx
        self.y += self.vy
        
        # movement of the player 
        if self.keyHandler[LEFT]:
            self.vx = -3
            self.dir = -1
        elif self.keyHandler[RIGHT]:
            self.vx = 3
            self.dir = 1
        else:
            self.vx = 0
            
        # player jump    
        if self.keyHandler[UP] and self.vy == 0:
            self.vy = -4
            
        # prevents player from moving off screen
        if self.x - self.r < 0:
            self.x = self.r
        if self.x + self.r > game.w:
            self.x = game.w - self.r
            
        # prevents player from jumping infinetly
        if self.y < self.h*0.8:             
            self.vy = 4
            
        # stops the player from going all the way
        if self.y > 400:
            self.y = 400
            self.vy = 0
            
        self.x += self.vx
        self.y += self.vy
        
        # when the object hits the grass, it gets removed from the list 
        for x in game.objects:
            if x.y > x.h * 3/4 + 10:
                game.objects.remove(x)
        
        # level increments when the list of objects is empty
        if len(game.objects) == 0:
            
            # to assure that the code still works if 2 bad objects are
            # picked up at the same time AND in a scenario that the last
            # object that falls is also the 3rd bad object picked up
            # therefore, level should increment (emtpy list of objects), but also
            # player already lost (3 bad objects collected)
            
            if game.player.lives <= 0:
                screen.counter = 4
                
            game.level +=1
            
            if game.level == 5:
                game.game = False
                screen.counter = 5
            else:
                game.startGame (game.character, game.level)
            
    # distance of player from objects
    def distance (self, target):
        return ((self.x - target.x) ** 2 + (self.y - target.y)**2) ** 0.5
    
    # determines if collision occurs
    def collision(self):
        for x in game.objects:
            if self.distance (x) <= self.r + x.r and x.v == 0:
                game.objects.remove(x)
                del x
                game.score += 1         
            elif self.distance (x) <= self.r + x.r and x.v == 1:
                game.objects.remove(x)
                del x
                self.lives -= 1
        
        # condition for game over
        if self.lives <= 0:
            self.gameOver = True 
            game.game = False
            musicPlay.stop() 
  
    # displaying the player and animating it                  
    def display(self):
        self.update()
        if self.vx != 0:
            self.f = (self.f+0.1) % self.F
        else:
            self.f = 3
        
        if self.dir >= 0:
            image(self.img,self.x-self.r-game.x,self.y-self.r, self.w,\
                  self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        else:
            image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,\
                  self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)
            
###############################################################################

class Objects:
    
    def __init__ (self, dim, turn):
        self.dim = dim
        self.turn = turn
        self.r = dim/2               
        
        # randomly selectes a x and y variable; overlaps are allowed to increase
        # difficulty of game
        
        self.x = random.randint (0, game.w - self.dim)
        self.y = random.randint (-1600 +(game.level*150), 0)
        
        self.w = game.w
        self.h = game.h
        
        self.numObjects = 13
        self.vy = game.level * 1.5
        
        # make a list of either odd or even numbers depending on turn
        # to assure that objects List = 50% good and 50% bad
        
        self.list = range(self.turn, self.numObjects, 2)
        
        self.num = (random.choice(self.list)) # randomly assign odd value
        
            
        if self.num % 2 == 0:
            self.v = 0
        elif self.num % 2 == 1:
            self.v = 1
        
        self.img = loadImage (path + '/' + 'object' + str(self.num) + '.png')
        self.grass = loadImage (path + "/" + "grass.png")
                                                            
    def fall(self):
        self.y = self.y + self.vy             # dates ball position in y
                 
    def display(self):
        image (self.img, self.x, self.y, self.dim, self.dim)
        self.fall()
    
# load all the screens
screen = Screen()
instructions = Instructions()
playerScreen = PlayerScreen() 
game = Game()
loserScreen = LoserScreen()
congratulations = Congratulations()

# music is loaded externally in order to assure that no overlaps occur
# and also allow access from anywhere in the code (as they are needed to be
# played in more than one class

musicPlay = SoundFile (this, path + "/" + "circus.wav")
musicWin = SoundFile (this, path + "/" + 'graduation.mp3') 
musicLose = SoundFile (this, path + "/" + 'lose.wav')

def setup(): 
    size(500,700)  
    
def draw(): 
    background(255)

    # draw function behaves differently depending on counter     
    # music functions are adjusted accordingly
    
    if screen.counter == 0:
        screen.display()
    
    elif screen.counter == 1:
        instructions.display()
        musicWin.stop()
        screen.musicPlayer()
        screen.musicCountLose = 0
        screen.musicCountWin = 0
    
    elif screen.counter == 2:
        playerScreen.display()
    
    elif screen.counter == 3:
        game.display()
        if game.player.gameOver:
            screen.counter +=1 
            game.tryno += 1
    
    elif screen.counter == 4:
        loserScreen.display()
        musicPlay.stop()
        screen.musicLose()
        screen.musicCount = 0
        
    elif screen.counter == 5:
        congratulations.display()
        musicPlay.stop()
        screen.musicWin()
        screen.musicCount = 0
    
def keyPressed():
    
    # for movement left, right, up
    if keyCode == LEFT and game.game:
        game.player.keyHandler[LEFT]=True
    elif keyCode == RIGHT and game.game:
        game.player.keyHandler[RIGHT]=True
    elif keyCode == UP and game.game:
        game.player.keyHandler[UP]=True


def keyReleased():
    
    # stops infinite movement left, right, up
    if keyCode == LEFT and game.game:
        game.player.keyHandler[LEFT]=False
    elif keyCode == RIGHT and game.game:
        game.player.keyHandler[RIGHT]=False
    elif keyCode == UP and game.game:
        game.player.keyHandler[UP]=False

def mouseClicked():
    
    # mouseClicked is used for jumping between screens due to
    # user input
    
    if not game.game:
        if 260 < mouseY < 335 and 70 < mouseX < 141:
            screen.counter +=1
            game.startGame("Flavia", 1)
            game.score = 0
            game.game = True

        if 260 < mouseY < 335 and 210 < mouseX < 281:
            screen.counter +=1
            game.startGame("Araz", 1)
            game.score = 0
            game.game = True
            
        if 260 < mouseY < 335 and 350 < mouseX < 429:
            screen.counter +=1
            game.startGame("Tami", 1)
            game.score = 0
            game.game = True
            
        if 630 < mouseY < 670 and 150 < mouseX < 350:
            screen.flipping()                        