from graphics import *
from classes import *
import time

width = 1200
height = 600

gameFPS = 30
framePeriod = 1.0/gameFPS

ground = 545
friction = 1
kickSpeed = 10


# Main Window
win = GraphWin('Head Soccer', width, height, False)

# Instance background but don't draw
background = Image(Point(width/2, height/2), 'Images/bg.gif')

# Init Key Buffer
win.ligar_Buffer()

# Instance Player and draw collisions ## Collisions must be drawed before background
leftPlayer = Player(win, 300, 485, "Left")

# Instance Ball and collisions
ball = Ball(win, width/2, 200)
ball.drawCollisions(width/2, 200)

# Draw background
background.draw(win)

# Draw Player Mechs
leftPlayer.drawMech(300, 503, "Images/LeftChar.gif")
leftPlayer.drawCollisions(300, 485)

# Draw Ball Mechs
ball.drawMech(width/2, 200, "Images/Ball.gif")



# Main loop
while True:

    # Get all Pressed Keys
    lista = win.checkKey_Buffer()
    update()



     # Keyboard Verification
    if len(lista) > 0:

        if ("Left" in lista) and (leftPlayer.getPos()[0] - headRadius > 0):
            leftPlayer.move(-leftPlayer.charVel, 0)

        elif("Right" in lista) and (leftPlayer.getPos()[0] + headRadius < width):	
            leftPlayer.move(leftPlayer.charVel, 0)
            
        if("Up" in lista):	
            if not(leftPlayer.isJumping):
                leftPlayer.isJumping = True

        if("space" in lista):
            if not(leftPlayer.isKicking):
                leftPlayer.isKicking = True
                leftPlayer.saveMech = leftPlayer.mech

        if("quoteright" in lista):	
            leftPlayer.restartPos()
            ball.restartPos()




    # Foot and Ball collisions
    if ( checkCollisions(leftPlayer, ball) ):
        
        # if True: Char is left from ball
        if ( leftPlayer.getFootPos()[0] < ball.getPos()[0] ):
            ball.speedX = 20

        # if True: Char is right from ball
        if ( leftPlayer.getFootPos()[0] > ball.getPos()[0] ):
            ball.speedX = -20


    # leftPlayer Jump Verification
    if (leftPlayer.isJumping):

        if leftPlayer.contJump <= 24:

            # Up
            if leftPlayer.contJump//12 == 0:
                leftPlayer.jump(-leftPlayer.jumpDy)
                leftPlayer.jumpDy += 4

            # Down
            if leftPlayer.contJump//12 == 1:
                leftPlayer.jumpDy -= 4
                leftPlayer.jump(leftPlayer.jumpDy)

            # Defines jump speed
            leftPlayer.contJump += 1.5

        # Jump ends		
        else:
            leftPlayer.isJumping = False
            leftPlayer.contJump = 0


    # Checks if the player is kicking
    if (leftPlayer.isKicking):

        # First Mech
        if (leftPlayer.contKick < kickSpeed/2):

            CurrentX = leftPlayer.getPos()[0]
            CurrentY = leftPlayer.getPos()[1] + 18

            leftPlayer.undrawMech()
            leftPlayer.drawMech(CurrentX, CurrentY, "Images/LeftChar_kick1.gif")

            leftPlayer.contKick += 1

        # Second Mech
        elif (leftPlayer.contKick < kickSpeed):

            CurrentX = leftPlayer.getPos()[0]
            CurrentY = leftPlayer.getPos()[1] + 18

            leftPlayer.undrawMech()
            leftPlayer.drawMech(CurrentX, CurrentY, "Images/LeftChar_kick2.gif")

            leftPlayer.contKick += 1
        
        # Change to initial mech
        else:
            CurrentX = leftPlayer.getPos()[0]
            CurrentY = leftPlayer.getPos()[1] + 18
            
            leftPlayer.undrawMech()
            leftPlayer.drawMech(CurrentX, CurrentY, "Images/LeftChar.gif")
            leftPlayer.isKicking = False
            leftPlayer.contKick = 0



    # Checks for vel and move
    if (ball.speedX != 0 or ball.speedY != 0):

        ball.move(ball.speedX, ball.speedY)



    # Verify if ball is on the ground and apply friction
    if ( ball.getPosBellow()[1]  == ground ):

        ball.acceleration = 0
        print(ball.getPosBellow()[1])

        # Verify if ball is moving to right
        if ball.speedX > 0:
        
            if (ball.speedX - friction < 0):
                ball.speedX = 0
            else:
                ball.speedX -= friction
        
        # Or moving to left
        else:

            if (ball.speedX + friction > 0):
                ball.speedX = 0
            else:
                ball.speedX += friction

    elif ( ball.getPosBellow()[1] < ground ):

        if (ball.getPosBellow()[1] + ball.speedY > ground):

            ball.speedY = (ball.speedY * -0.8)//1

            if ( ball.speedY < 2 and ball.speedY > -2 ):
                ball.speedY = 0

        else: 
            ball.speedY += ball.acceleration

    else:
        ball.move( 0, ground - ball.getPosBellow()[1] )


    time.sleep(framePeriod)

win.close()