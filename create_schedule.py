import random
from random import choice
import copy    # array-copying convenience
import sys     # max float
import matplotlib.pyplot as plt
# ------------------------------------

def show_vector(vector):
  arr = []
  arr1 = []
  arr2 = []
  arr3 = []
  for i in range(100):
      if(array_bus[round(vector[0][i])][0] in arr or array_sopir[round(vector[1][i])][0] in arr1 or array_kondektur[round(vector[2][i])][0] in arr2 or array_kota[round(vector[3][i])][0] in arr3):
        continue
      else:
        print(array_bus[round(vector[0][i])], array_sopir[round(vector[1][i])], array_kondektur[round(vector[2][i])], array_kota[round(vector[3][i])])
        arr.append(array_bus[round(vector[0][i])][0])
        arr1.append(array_sopir[round(vector[1][i])][0])
        arr2.append(array_kondektur[round(vector[2][i])][0])
        arr3.append(array_kota[round(vector[3][i])][0])


def fitness(position):
  fit = 0
  arr = []
  arr1 = []
  arr2 = []
  arr3 = []
  for i in range(100):
    if(array_bus[round(position[0][i])][0] in arr or array_sopir[round(position[1][i])][0] in arr1 or array_kondektur[round(position[2][i])][0] in arr2 or array_kota[round(position[3][i])][0] in arr3):
      continue
    else:
      fit += (array_bus[round(position[0][i])][2] * 10 - array_kota[round(position[3][i])][1]/100 + array_bus[round(position[0][i])][3] * 2 + array_sopir[round(position[1][i])][2] * 5 + array_kondektur[round(position[2][i])][2] * 5 - (array_sopir[round(position[1][i])][5] + 
        array_kondektur[round(position[2][i])][5]) * 0.5 + jadwal(array_sopir[round(position[1][i])], array_kondektur[round(position[2][i])]) * 10)
      arr.append(array_bus[round(position[0][i])][0])
      arr1.append(array_sopir[round(position[1][i])][0])
      arr2.append(array_kondektur[round(position[2][i])][0])
      arr3.append(array_kota[round(position[3][i])][0])
  return fit

def jadwal(array1, array2):
  count = 0
  if(array1[3] == array2[3]):
    count = count + 1
  if(array1[3] == array2[4]):
    count = count + 1
  if(array1[4] == array2[3]):
    count = count + 1
  if(array1[4] == array2[4]):
    count = count + 1
  return count

# ------------------------------------

class Particle:
  def __init__(self, dim, minx, maxx, seed):
    self.rnd = random.Random(seed)
    self.position = [[] for i in range(dim)]
    self.velocity = [[] for i in range(dim)]
    self.best_part_pos = [0.0 for i in range(dim)]

    for i in range(dim):
      for j in range(100):
        self.position[i].append(((maxx - minx) * self.rnd.random()) + minx)
        self.velocity[i].append(((maxx - minx) * self.rnd.random()) + minx)

    self.fit = fitness(self.position) # curr fitness
    self.best_part_pos = copy.copy(self.position) 
    self.best_part_fit = self.fit # best fitness

def Solve(max_epochs, n, dim, minx, maxx, minv, maxv):
  rnd = random.Random(0)

  # create n random particles
  swarm = [Particle(dim, minx, maxx, i) for i in range(n)] 

  best_swarm_pos = [[] for i in range(dim)] # not necess.
  best_swarm_fit = sys.float_info.min # swarm best
  for i in range(n): # check each particle
    if swarm[i].fit > best_swarm_fit:
      best_swarm_fit = swarm[i].fit
      best_swarm_pos = copy.copy(swarm[i].position) 

  epoch = 0
  w = 0.25  # inertia
  c1 = 1 # cognitive (particle)
  c2 = 2 # social (swarm)

  iter = []
  best_fit = []

  while epoch < max_epochs:
    best_fitness_iter = 0  # Menyimpan best fitness untuk iterasi saat ini

    for i in range(n): # process each particle
      
      # compute new velocity of curr particle
      for k in range(dim): 
        r1 = rnd.random()    # randomizations
        r2 = rnd.random()
        for l in range(100):
    
          swarm[i].velocity[k][l] = ((w * swarm[i].velocity[k][l]) +
            (c1 * r1 * (swarm[i].best_part_pos[k][l] -
            swarm[i].position[k][l])) +  
            (c2 * r2 * (best_swarm_pos[k][l] -
            swarm[i].position[k][l])) )  

          if swarm[i].velocity[k][l] < minv:
            swarm[i].velocity[k][l] = minv
          elif swarm[i].velocity[k][l] > maxv:
            swarm[i].velocity[k][l] = maxv

      # compute new position using new velocity
          swarm[i].position[k][l] += swarm[i].velocity[k][l]
          if(swarm[i].position[k][l] >= maxx):
            swarm[i].position[k][l] = maxx
          elif(swarm[i].position[k][l] <= minx):
            swarm[i].position[k][l] = minx
  
      # compute fitness of new position
          swarm[i].fit = fitness(swarm[i].position)

      # is new position a new best for the particle?
          if swarm[i].fit > swarm[i].best_part_fit:
            swarm[i].best_part_fit = swarm[i].fit
            swarm[i].best_part_pos = copy.copy(swarm[i].position)

      # is new position a new best overall?
          if swarm[i].fit > best_swarm_fit:
            best_swarm_fit = swarm[i].fit
            best_swarm_pos = copy.copy(swarm[i].position)

      # Menyimpan best fitness untuk iterasi saat ini
          if swarm[i].fit > best_fitness_iter:
            best_swarm_pos_iter = copy.copy(swarm[i].position)
            best_fitness_iter = swarm[i].fit

    # for-each particle
    
    show_vector(best_swarm_pos_iter)
    iter.append(epoch+1)
    best_fit.append(best_fitness_iter)
    print("Best fitness of iteration", epoch+1, "= %.4f" % best_fitness_iter)
    print("\n")
    epoch += 1

  plt.plot(iter, best_fit, label='Graph')

  # Adding labels and title
  plt.xlabel('Iteration')
  plt.ylabel('Global Best')
  plt.title('Global Best Each Iteration')
  plt.legend()

  # Showing plot
  plt.show()
  # while
  return best_swarm_pos
# end Solve


print("\nBegin particle swarm optimization using Python demo\n")
dim = 4
print("Goal is to solve Rastrigin's function in " +
 str(dim) + " variables")
print("Function has known min = 0.0 at (", end="")
for i in range(dim-1):
  print("0, ", end="")
print("0)")

array_bus = [ [0, "A1", 1, 1], [1, "A2", 1, 1], [2, "A3", 0, 1], [3, "A4", 1, 3], 
            [4, "A5", 0, 3], [5, "A6", 1, 6], [6, "A7", 1, 6], [7, "A8", 1, 3], 
            [8, "A9", 1, 3], [9, "A10", 0, 3], [10, "A11", 1, 1], [11, "A12", 1, 6], 
            [12, "A13", 0, 3], [13, "A14", 0, 3], [14, "A15", 1, 1], [15, "A16", 1, 2], 
            [16, "A17", 0, 3], [17, "A18", 1, 1], [18, "A19", 1, 3], [19, "A20", 1, 3]] 

array_sopir = [[0, "Ari", 1, 1, 3, 2], [1, "Bobi", 1, 1, 2, 3], [2, "Cena", 1, 1, 3, 1], [3, "Doni", 1, 3, 4, 5], [4, "Endar", 1, 1, 3, 2], 
               [5, "Farhan", 1, 1, 4, 2], [6, "Golu", 1, 3, 4, 3], [7, "Hardi", 1, 1, 2, 2], [8, "Ian", 1, 1, 2, 4], [9, "Jali", 0, 2, 3, 2], 
               [10, "Kasmi", 1, 1, 3, 2], [11,"Lali", 1, 3, 4, 1], [12, "Marko", 1, 1, 2, 1], [13, "Ngatno", 1, 1, 2, 4], [14, "Oleng", 1, 3, 4, 2], 
               [15, "Qodam", 0, 2, 4, 2], [16, "Rossi", 1, 1, 2, 0], [17, "Santo", 1, 2, 4, 2], [18, "Tukul", 1, 1, 2, 2], [19, "Umar", 1, 1, 4, 2]]

array_kondektur = [[0, "Anton", 1, 2, 3, 2], [1, "Botol", 1, 3, 4, 3], [2, "Conel", 0, 1, 4, 1], [3, "Danzo", 1, 3, 4, 5], [4, "Eri", 1, 3, 4, 2], 
                   [5, "Faryadi", 1, 1, 2, 2], [6, "Gopal", 1, 3, 4, 3], [7, "Harul", 1, 1, 2, 2], [8, "Ishan", 1, 1, 2, 4], [9, "Jordi", 1, 3, 4, 2], 
                   [10, "Karyo", 1, 2, 3, 3], [11, "Lamidi", 1, 1, 2, 0], [12, "Mardi", 0, 1, 2, 2], [13, "Nassar", 1, 1, 3, 4], [14, "Omen", 1, 3, 4, 2], 
                   [15, "Qory", 0, 2, 4, 3], [16, "Romi", 1, 3, 4, 0], [17, "Sugik", 1, 1, 4, 1], [18, "Temon", 1, 2, 4, 2], [19, "Uno", 0, 3, 4, 1]]

array_kota = [[0, 353, "Jakarta"], [1, 0, "Surabaya"], [2, 79, "Malang"], [3, 477, "Bandung"], [4, 517, "Tasikmalaya"], 
              [5, 409, "Depok"], [6, 535, "Tangerang"], [7, 455, "Bekasi"], [8, 606, "Yogyakarta"], [9, 659, "Surakarta"], 
              [10, 421, "Bogor"], [11, 518, "Semarang"], [12, 939, "Cirebon"], [13, 488, "Madiun"], [14, 781, "Pekalongan"],
              [15, 353, "Jakarta"], [16, 0, "Surabaya"], [17, 79, "Malang"], [18, 477, "Bandung"], [19, 517, "Tasikmalaya"]]

num_particles = 50
max_epochs = 10
print("Setting num_particles = " + str(num_particles))
print("Setting max_epochs    = " + str(max_epochs))
print("\nStarting PSO algorithm\n")

best_position = Solve(max_epochs, num_particles, dim, 0, 19, -2, 1.5)

print("\nPSO completed\n")
print("\n")

print("\nEnd particle swarm demo\n")