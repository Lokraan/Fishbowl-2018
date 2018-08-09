
from random import randint

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import click


ON = 1
OFF = 0
vals = [ON, OFF]


def gen_glider(i, j, grid):
  """ Add glider with top left cell at (i, j) """
  glider = np.array([[0, 0, 1],
                    [1, 0, 1],
                    [0, 1, 1]])
                      
  grid[i:i+3, j:j+3] = glider
    

def gen_rand_grid(side_length, density):
  """ return random set of values """
  grid = np.random.choice(vals, side_length**2, p=[density, 1 - density])
  grid = grid.reshape(side_length, side_length)
  return grid


"""
def blankGrid(N):
  return(np.array([[[0]*N]*N]]))
    
def putMiddle(grid, N, D, S):
  for i in range(N-1):
    for j in range(N-1):
      
"""
def update(frameNum, img, grid, N):
  # copy grid since we require 8 neighbors for calculation
  # and we go line by line 
  newGrid = grid.copy()
  for i in range(N - 1):
    for j in range(N - 1):
      # compute 8-neghbor sum
      total = int((grid[i, (j-1)] + grid[i, (j+1)] + 
             grid[(i-1), j] + grid[(i+1), j] + 
             grid[(i-1), (j-1)] + grid[(i-1), (j+1)] + 
             grid[(i+1), (j-1)] + grid[(i+1), (j+1)]))
             
            # apply Conway's rules
      if grid[i, j]  == ON:
        if (total < 2) or (total > 3):
          newGrid[i, j] = OFF
      else:
        if total == 3:
          newGrid[i, j] = ON
          
    # update data
  img.set_data(newGrid)
  grid[:] = newGrid[:]
  return img,


# main function
@click.command()
@click.option("--gridsize", type=int, default=100, help="Size of grid, must be greater than 8")
@click.option("--movfile", type=str, help="File to save animation to")
@click.option("--interval", type=int, default=30, help="Interval for each frame in miliseconds, ie: 1000 = 1 second")
@click.option("--glider/--no-glider", default=False, help="Have a glider on the screen or not.")
@click.option("--density", type=int, default=30, help="Density of screen, ie: 70 = 70% full")
def run(gridsize, movfile, interval, glider, density):
  # set size
  if gridsize <= 8:
    gridsize = 100
    
  # declare grid
  grid = np.array([])
  
  density = density / 100
  if 0 >= density or density > 1:
    density = 0.3
  
  if interval <= 0:
    interval = 17 # ~60 frames per second

  # check glider
  if glider:
    grid = np.zeros(gridsize**2).reshape(gridsize, gridsize)
    gen_glider(1, 1, grid)
  else:
    grid = gen_rand_grid(gridsize, density)

  # set up animation
  fig, ax = plt.subplots()
  img = ax.imshow(grid, interpolation="nearest")
  ani = animation.FuncAnimation(fig, update, fargs=(img, grid, gridsize,),
      frames=30, interval=interval, save_count=50)
                  
                  
  # num frames?
  # set the output of the file
  if movfile:
    ani.save(movfile, fps=30, extra_args=["-vcodec", "libx264"])
  
  plt.show()
  
  
# call main
if __name__ == "__main__":
  run()
