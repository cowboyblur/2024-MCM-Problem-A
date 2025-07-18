import mesa
import math
from .random_walk import RandomWalker

def logistic(p):
    return 1 / (1 + math.exp(-p))

class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None
    sex = None


    def __init__(self, unique_id, pos, model, moore, energy=None,\
                  sex=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.sex = sex


    def step(self):
        """
        A model step. Move, then eat resource and reproduce.
        """
        self.random_move()
        living = True

        if self.model.resource:
            # Reduce energy
            if self.sex == 'Female':
                self.energy -= 1
            else: self.energy -= 0.8

            # If there is resource available, eat it
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            resource_patch = next(obj for obj in this_cell if isinstance(obj, GrassPatch))
            if resource_patch.fully_grown:
                self.energy += self.model.sheep_gain_from_food
                resource_patch.fully_grown = False

            # Death
            if self.energy < 0:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                living = False

        reproduce = (-4 * (self.model.rate - 0.5) * (self.model.rate - 0.5) + 1) * self.model.sheep_reproduce
        if living and self.random.random() < reproduce:
            # Create a new sheep:
            if self.model.resource:
                self.energy /= 2
            if self.random.random() < logistic(-0.02 * self.model.resource / self.model.sheep_num + 1.27) :
            #if self.random.random() < 0.5:
                lamb = Sheep(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy, 'Male'
                )
            else: 
                lamb = Sheep(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy, 'Female'
                )
            self.model.grid.place_agent(lamb, self.pos)
            self.model.schedule.add(lamb)


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        self.energy -= 1

        # If there are sheep present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]
        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            if sheep_to_eat.sex == 'Male' and self.random.random() < 0.8:
                self.energy += self.model.wolf_gain_from_food
                # Kill the sheep
                self.model.grid.remove_agent(sheep_to_eat)
                self.model.schedule.remove(sheep_to_eat)
            elif sheep_to_eat.sex == 'Female' :
                self.energy += self.model.wolf_gain_from_food
                # Kill the sheep
                self.model.grid.remove_agent(sheep_to_eat)
                self.model.schedule.remove(sheep_to_eat)

        # Death or reproduction
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.wolf_reproduce:
                # Create a new wolf cub
                self.energy /= 2
                cub = Wolf(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy
                )
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)


class GrassPatch(mesa.Agent):
    """
    A patch of resource that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of resource

        Args:
            grown: (boolean) Whether the patch of resource is fully grown or not
            countdown: Time for the patch of resource to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.resource_regrowth_time
            else:
                self.countdown -= 1
