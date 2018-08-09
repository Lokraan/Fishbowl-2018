
import sys
import math
import turtle
import random
from fractions import gcd # for py 3.3
from datetime import datetime
from time import sleep

import click


# class that draws spirographs
class Spiro:
  # constructor
  def __init__(self, xc, yc, col, R, r, l):

    # create the turtle object
    self.t = turtle.Turtle()
    # set the cursor shape
    self.t.shape("circle")
    # set the step in degrees
    self.step = 5
    # set the drawing complete flag
    self.drawingComplete = False

    # set the params
    self.setParams(xc, yc, col, R, r, l)

    # initialize the drawing
    self.restart()


  # set the parameters
  def setParams(self, xc, yc, col, R, r, l):
    self.xc = xc
    self.yc = yc
    self.col = col
    self.R = int(R)
    self.r = int(r)
    self.l = l
    # reduce r/R to it"s smallest form by dividing with the GCD
    gcdVal = gcd(self.r, self.R)
    
    # number of rotations
    self.nRot = self.r//gcdVal
    print(f"R: {self.R}")
    print(f"r: {self.r}")
    print(f"l: {self.l}")
    print(f"Number Rotations: {self.nRot}")
    
    # get ratio of radii
    self.k = r/float(R)
    
    # set the color
    self.t.color(*col)
    
    # set size
    self.t.turtlesize(0.5, 0.5)
    
    # store the current angle
    self.a = 0


  # restart the drawing
  def restart(self):
    # set the flag
    self.drawingComplete = True
    
    # show the turtle
    self.t.showturtle()

    # go to the first point
    self.t.up()
    R, k, l = self.R, self.k, self.l
    a = 0.0
    x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
    y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
    self.t.setpos(x, y)
    self.t.down()
    
    
  # draw the whole thing
  def draw(self):
    # draw the rest of the points
    R, k, l = self.R, self.k, self.l
    for i in range(0, 360 * self.nRot + 1, self.step):
      
      self.t.settiltangle(i - 10)
      a = math.radians(i)
      x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
      y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
      self.t.setpos(self.xc + x, self.yc + y)

    # drawing is now done
    self.drawingComplete = True
    # hide cursor
    self.t.hideturtle()
    sleep(4)


  # clear everything
  def clear(self):
    self.t.clear()


class SpiroAnimator:
  def __init__(self, N):
    # set the timer value in milliseconds
    self.deltaT = 10

    # get window dimensions
    self.width = turtle.window_width()
    self.height = turtle.window_height()

    # create spiro objects
    self.spiros = []
    for i in range(N):
      # gen random params
      rparams = self.genRandomParams()
      # set the spiro parameters
      spiro = Spiro(*rparams)
      self.spiros.append(spiro)

    # call timer
    turtle.ontimer(self.update, self.deltaT)


  # restart program
  def restart(self):
  
    for spiro in self.spiros:
    
      spiro.t.up()
      # clear
      spiro.clear()
      
      # gen random params
      rparams = self.genRandomParams()
      
      # set the spiro params
      spiro.setParams(*rparams)
      
      # restart drawing
      spiro.restart()

  def genRandomParams(self):
    width, height = self.width, self.height

    R = random.randint(50, min(width, height)//2)
    r = random.randint(10, 9*R//10)
    l = random.uniform(0.1, 0.9)

    xc = yc = 0
    col = (random.random(),
      random.random(), random.random())

    return (xc, yc, col, R, r, l)


  def update(self):
    # update all spiros
    nComplete = 0
    for spiro in self.spiros:
      spiro.restart()
      # update
      spiro.draw()
      # count completed spiros
      if spiro.drawingComplete:
        nComplete += 1

    # restart if all spiros are complete
    if nComplete == len(self.spiros):
      self.restart()
    # call timer
    turtle.ontimer(self.update, self.deltaT)

    
  # turtle toggle cursor on and off
  def toggleTurtles(self):
    for spiro in self.spiros:
      if spiro.t.isvisible():
        spiro.t.hideturtle()
      else:
        spiro.t.showturtle()


@click.command()
@click.option("--params", type=str, 
  help="The 3 arguments for a spirograph: R, r, and l. ie: 50 10 0.1")
def main(params):
  """This program draws spirographs using the Turtle module. 
    When run with no arguments, this program draws random spirographs.
    
    Terminology:
    R: radius of outer circle.
    r: radius of inner circle.
    l: ratio of hole distance to r.
  """

  # set up turtle
  turtle.setup(width=0.8)
  turtle.shape("classic")
  turtle.bgcolor("black")

  turtle.title("Spirographs")

  # start listening
  turtle.listen()

  # hide main turtle cursor
  turtle.hideturtle()

  # check for any params
  if params:
    if params.split(" ") < 3 or params.split(" ") < 0:
      sys.exit("Params requires 3 arguments: R, r, and l.")

    params = [float(x) for x in params]
    # draw he Spirograph with the given params
    col = (random.random(),
         random.random(),
         random.random())
    spiro = Spiro(0, 0, col, *params)
    spiro.draw()

  else:
    # create the animator object
    spiroAnim = SpiroAnimator(1)

    # add key handler to toggle turtle cursor
    turtle.onkey(spiroAnim.toggleTurtles, "t")

    # add key to restart animation
    turtle.onkey(spiroAnim.restart, "space")



  turtle.mainloop()

# call main

if __name__ == "__main__":
  main()
