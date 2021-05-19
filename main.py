from random import randint, choice

'''
I've started with presenting Terrain as a class,but then I realized it'd be simpler to present it as a two-dimensional 
list,let it stay here

class Terrain:
    def __init__(self, x, y, terrains):
        self.x = x  # устанавливаем имя
        self.y = y
        self.terrains = list(terrains)

    def __str__(self):
        return f"{self.terrains}"
'''


class Animal:
    def __init__(self, animal_type, hunger, status='ALIVE'):
        self.animal_type = animal_type
        self.hunger = int(hunger)
        self.status = str(status)

    def __str__(self):
        return f"{self.animal_type} {self.hunger} {self.status}"

    def __repr__(self):
        return f"{self.animal_type} {self.hunger} {self.status}"


class TerrainCell:
    def __init__(self, terrain_type, animals):
        self.terrain_type = terrain_type  # устанавливаем имя
        self.animals = list(animals)

    def __str__(self):
        return f"{self.terrain_type} , {self.animals}"

    def __repr__(self):
        return f"{self.terrain_type}, {self.animals}"


ls_terrain_types = ['DESERT', 'MOUNTAIN', 'GRASS', 'WATER']
ls_status = ['DEAD', 'EATEN', 'ALIVE']
ls_animal_type = ['Carnivore', 'Herbivore', 'Scavenger']


def death(animal_obj):
    animal_obj.status = 'DEAD'
    animal_obj.hunger = 0


def eaten(animal_obj):
    animal_obj.status = 'EATEN'
    animal_obj.hunger = 0


def move(terrain, height, width, hg, wd, animal):
    ind = terrain[hg][wd].animals.index(animal)  # index of the animal in list of animals
    anim = terrain[hg][wd].animals[ind]  # moved animal
    if wd == 0 and hg != 0:
        terrain[hg - 1][wd].animals.append(anim)
        # print('up')
    elif hg + 1 == height and height != 0:
        terrain[hg][wd - 1].animals.append(anim)
        # print('left')
    elif wd + 1 == width:
        terrain[hg + 1][wd].animals.append(anim)
        # print('down')
    else:
        terrain[hg][wd + 1].animals.append(anim)
        # print('right')
    terrain[hg][wd].animals.remove(anim)


def visualisation(height, width, days):
    '''
        Test terrain
    terrain = [[TerrainCell(terrain_type='GRASS', animals=[Animal(animal_type='Scavenger', hunger=4),
                                                            Animal(animal_type='Herbivore', hunger=0,
                                                                    status='DEAD')]), ]]
    '''
    # Generating the terrain
    terrain = [[TerrainCell(terrain_type=choice(ls_terrain_types), animals=[Animal(animal_type=choice(ls_animal_type),
                                                                                   hunger=randint(1, 10))]) for i in
                range(width)] for i in range(height)]  # generating the terrain

    # Starting live in terrain
    for day in range(days):
        animals_for_moving = []  # list with data about animal,which are going to move
        # Killing animals who're in water
        for hg in range(height):
            for wd in range(width):
                if terrain[hg][wd].terrain_type == 'WATER':  # checking if terrain is water
                    for i in terrain[hg][wd].animals:  # iterating through all animals in water terrain
                        death(i)

        # Printing the day
        for hg in range(height):
            print('| ', end='')
            for wd in range(width):
                print(terrain[hg][wd], '|', end=' ')
            print()
            print('-' * 100)
        print()
        print()
        print('The end of ', day + 1, 'day ')
        print()
        print()

        # Changing in the terrain before starting the next day
        for hg in range(height):
            for wd in range(width):
                for animal in terrain[hg][wd].animals:  # iterating through the list of animals in every single terrain

                    if 5 > animal.hunger > 0:  # checking if animal is hunger and alive

                        # For hungry Herbivore
                        if animal.animal_type == 'Herbivore' and terrain[hg][wd].terrain_type == 'GRASS':
                            animal.hunger += 2

                        elif animal.animal_type == 'Herbivore':
                            animals_for_moving.append([hg, wd, animal])

                        # For hungry Carnivore
                        elif animal.animal_type == 'Carnivore':
                            counter_of_carnivores = 0
                            for assumed_not_carnivore in terrain[hg][wd].animals:
                                if assumed_not_carnivore.animal_type != 'Carnivore' and assumed_not_carnivore.hunger >= 1:
                                    eaten(assumed_not_carnivore)
                                    animal.hunger += 2
                                    break
                                else:
                                    counter_of_carnivores += 1
                                if counter_of_carnivores == len(
                                        terrain[hg][wd].animals):  # if there are not no Carnivores in terrain cell
                                    animals_for_moving.append([hg, wd, animal])

                        # For hungry Scavenger
                        elif animal.animal_type == 'Scavenger':
                            counter_of_not_dead = 0
                            for assumed_dead in terrain[hg][wd].animals:
                                if assumed_dead.status == 'DEAD':
                                    eaten(assumed_dead)
                                    animal.hunger += 2

                                    break
                                else:
                                    counter_of_not_dead += 1
                                if counter_of_not_dead == len(
                                        terrain[hg][wd].animals):  # if there are not no dead in terrain cell
                                    animals_for_moving.append([hg, wd, animal])

                    if animal.status != 'EATEN' and animal.status != 'DEAD':  # Hungering of the animal
                        animal.hunger -= 1

                    if animal.hunger <= 0 and animal.status != 'EATEN':  # Killing animals with 0 hunger
                        death(animal)
                    # animals_for_moving.append([hg,wd,animal])
        for i in animals_for_moving:
            move(terrain=terrain, height=height, width=width, hg=i[0], wd=i[1], animal=i[2])


height_ = int(input('Write the height of terrain(recommended value is 3 for betters visualising) : '))
width_ = int(input('Write the width of terrain(recommended value is 3 for betters visualising) :'))
days_ = int(input('How much days of terrain live you want to see (5):'))
print()
print()

visualisation(height=height_, width=width_, days=days_)
