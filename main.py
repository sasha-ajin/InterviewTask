from random import randint, choice


class Animal:
    def __init__(self):
        self._hunger = randint(1, 10)
        self._status = 'ALIVE'

    @property
    def hunger(self):
        return self._hunger

    @hunger.setter
    def hunger(self, hunger):
        if hunger in range(0, 11):
            self._hunger = hunger
        else:
            print("Not valid hunger value")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status == 'DEAD' or status == 'EATEN' or status == 'ALIVE':
            self._status = status
        else:
            print("Not valid animal status")

    def death(self):
        self.status = 'DEAD'
        self.hunger = 0

    def eaten(self):
        self.status = 'EATEN'
        self.hunger = 0


class Carnivore(Animal):
    def __init__(self):
        Animal.__init__(self)
        self._animal_type = 'Carnivore'

    def __str__(self):
        return f"{self._animal_type} {self._hunger} {self._status}"

    def __repr__(self):
        return f" {self._animal_type}{self._hunger} {self._status}"


class Herbivore(Animal):
    def __init__(self):
        Animal.__init__(self)
        self._animal_type = 'Herbivore'

    def __str__(self):
        return f"{self._animal_type} {self._hunger} {self._status}"

    def __repr__(self):
        return f" {self._animal_type}{self._hunger} {self._status}"


class Scavenger(Animal):
    def __init__(self):
        Animal.__init__(self)
        self._animal_type = 'Scavenger'

    def __str__(self):
        return f"{self._animal_type} {self._hunger} {self._status}"

    def __repr__(self):
        return f" {self._animal_type}{self._hunger} {self._status}"


class TerrainCell:
    def create_animal(self):
        i = randint(1, 3)
        if i == 1:
            return Scavenger()
        elif i == 2:
            return Carnivore()
        else:
            return Herbivore()

    def __init__(self):
        self.animals = [self.create_animal()]


class WATER(TerrainCell):

    def __init__(self):
        TerrainCell.__init__(self)
        self.terrain_type = 'WATER'

    def __str__(self):
        return f"{self.terrain_type} , {self.animals}"

    def __repr__(self):
        return f"{self.terrain_type}, {self.animals}"


class DESERT(TerrainCell):
    def __init__(self):
        TerrainCell.__init__(self)
        self.terrain_type = 'DESERT'

    def __str__(self):
        return f"{self.terrain_type} , {self.animals}"

    def __repr__(self):
        return f"{self.terrain_type}, {self.animals}"


class MOUNTAIN(TerrainCell):
    def __init__(self):
        TerrainCell.__init__(self)
        self.terrain_type = 'MOUNTAIN'

    def __str__(self):
        return f"{self.terrain_type} , {self.animals}"

    def __repr__(self):
        return f"{self.terrain_type}, {self.animals}"


class GRASS(TerrainCell):
    def __init__(self):
        TerrainCell.__init__(self)
        self.terrain_type = 'GRASS'

    def __str__(self):
        return f"{self.terrain_type},{self.animals}"

    def __repr__(self):
        return f"{self.terrain_type},{self.animals}"


class Terrain:
    def create_terrain(self):
        i = randint(1, 3)
        if i == 1:
            return GRASS()
        elif i == 2:
            return MOUNTAIN()
        elif i == 3:
            return DESERT()
        else:
            return WATER()

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.terrain_list = [[self.create_terrain() for i in range(width)] for o in range(height)]
        # self.terrain_list=[] #For testing


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


def visualising(days, width, height):
    ter = Terrain(width=width, height=height)
    terrain = ter.terrain_list

    for day in range(days):
        animals_for_moving = []  # list with data about animal,which are going to move
        # Killing animals in water
        for i in terrain:
            for o in i:
                if isinstance(o, WATER):
                    for animal in o.animals:
                        animal.death()
        # Printing the day
        for i in terrain:
            print('|', end=' ')
            for o in i:
                print(o, end=' | ')
            print()
            print('-' * 100)
        print('end of ' + str(day + 1) + ' day')

        # Changing terrain before the next day
        for hg in range(height):
            for wd in range(width):
                for animal in terrain[hg][wd].animals:

                    # detecting hunger animals
                    if 5 > animal.hunger >= 1:
                        # For hungry Herbivore
                        if isinstance(animal, Herbivore):
                            if isinstance(terrain[hg][wd], GRASS):
                                animal.hunger += 2
                            else:
                                animals_for_moving.append([hg, wd, animal])
                        # For hungry Carnivore
                        elif isinstance(animal, Carnivore):
                            counter_not_carn = 0
                            for assumed_not_carn in terrain[hg][wd].animals:#iterating through the animals in terraincell
                                if not isinstance(assumed_not_carn, Carnivore) and assumed_not_carn.status == 'ALIVE':
                                    assumed_not_carn.eaten()
                                    animal.hunger += 2
                                    break
                                else:
                                    counter_not_carn += 1
                                if counter_not_carn == len(
                                        terrain[hg][wd].animals):  # if there are not no Carnivores in terrain cell
                                    animals_for_moving.append([hg, wd, animal])
                        # For hungry Scavenger
                        elif isinstance(animal, Scavenger):
                            counter_not_dead = 0
                            for assumed_dead in terrain[hg][wd].animals:#iterating through the animals in terraincell
                                if assumed_dead.status == 'DEAD':
                                    assumed_dead.eaten()
                                    animal.hunger += 2
                                    break
                                else:
                                    counter_not_dead += 1
                                if counter_not_dead == len(
                                        terrain[hg][wd].animals):  # if there are not no dead in terrain cell
                                    animals_for_moving.append([hg, wd, animal])

                    if animal.status == 'ALIVE':
                        animal.hunger -= 1
                    if animal.hunger == 0 and animal.status != 'EATEN':
                        animal.death()
        for i in animals_for_moving:
            move(terrain=terrain, height=height, width=width, hg=i[0], wd=i[1], animal=i[2])


height_ = int(input('Write the height of terrain(recommended value is 3 for better visualising) : '))
width_ = int(input('Write the width of terrain(recommended value is 3 for better visualising) :'))
days_ = int(input('How much days of terrain live you want to see (5):'))
print()
print()

visualising(height=height_, width=width_, days=days_)
