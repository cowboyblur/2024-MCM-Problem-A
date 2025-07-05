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
    stuck = None
    para = None

    def __init__(self, unique_id, pos, model, moore, energy=None,\
                  sex=None, stuck=None, para=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.sex = sex
        self.stuck = stuck
        self.para = para


    def step(self):
        """
        A model step. Move, then eat resource and reproduce.
        """
        living = True
        if self.model.resource1 or self.model.resource2:
            # Reduce energy
            if self.sex == 'Female':
                self.energy -= 1
            else: self.energy -= 0.8

            if self.stuck and living:
                this_cell = self.model.grid.get_cell_list_contents([self.pos])
                try:
                    resource_patch = next(obj for obj in this_cell if isinstance(obj, GrassPatch))
                except StopIteration:
                    judge1 = False
                else:
                    judge1 = resource_patch.fully_grown
                try:
                    resource_patch2 = next(obj for obj in this_cell if isinstance(obj, GrassPatch2))
                except StopIteration:
                    judge2 = False
                else:
                    judge2 = resource_patch2.fully_grown
                if judge1 or judge2:
                    self.energy += self.model.sheep_gain_from_food / 3
                else:
                    self.stuck = False
            else:
                self.random_move()
            # If there is resource available, parasite it
                this_cell = self.model.grid.get_cell_list_contents([self.pos])
                try:
                    resource_patch = next(obj for obj in this_cell if isinstance(obj, GrassPatch))
                except StopIteration:
                    judge1 = False
                else:
                    judge1 = resource_patch.fully_grown
                try:
                    resource_patch2 = next(obj for obj in this_cell if isinstance(obj, GrassPatch2))
                except StopIteration:
                    judge2 = False
                else:
                    judge2 = resource_patch2.fully_grown
                try:
                    competer = next(obj for obj in this_cell if isinstance(obj, Sheep))
                except StopIteration:
                    judge3 = False
                else:
                    judge3 = competer.stuck
                if judge1:
                    if judge3:
                        resource_patch.fully_grown = False
                        competer.stuck = False
                    else:
                        self.stuck = True
                        self.energy += self.model.sheep_gain_from_food /3
                        if self.para and self.random.random() < 1:
                            resource_patch.para = True
                        elif resource_patch.para and self.random.random() < 1:
                            self.para = True
                            
                elif judge2:
                    if judge3:
                        resource_patch2.fully_grown = False
                        competer.stuck = False
                    else:
                        self.stuck = True
                        self.energy += self.model.sheep_gain_from_food /3
                        if self.para and self.random.random() < 1:
                            resource_patch2.para = True
                        elif resource_patch2.para and self.random.random() < 1:
                            self.para = True


            # Death
            if self.energy < 0:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                living = False
            
            # Caught by human
            if living and self.random.random() < 0.01:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                living = False
            
            # Recover
            if living and self.random.random() < 0.05:
                self.para = False
            
            reproduce = (-4 * (self.model.rate - 0.5) * (self.model.rate - 0.5) + 1) * self.model.sheep_reproduce
            if living and self.random.random() < reproduce:
                # Create a new sheep:
                if self.model.resource1 or self.model.resource2:
                    self.energy /= 2
                next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
                next_move = self.random.choice(next_moves)
                #if self.random.random() < logistic(-0.02 * (self.model.resource1 + self.model.resource2) / self.model.sheep_num + 1.27) :
                if self.random.random() < 0.5:
                    lamb = Sheep(
                        self.model.next_id(), next_move, self.model, self.moore, self.energy, 'Male'
                    , False, False)
                else: 
                    lamb = Sheep(
                        self.model.next_id(), next_move, self.model, self.moore, self.energy, 'Female'
                    , False, False)
                self.model.grid.place_agent(lamb, self.pos)
                self.model.schedule.add(lamb)

class Sheep2(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    energy = None
    para = None
    def __init__(self, unique_id, pos, model, moore, energy=None, para=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.para = para


    def step(self):
        """
        A model step. Move, then eat resource and reproduce.
        """
        self.random_move()
        living = True

        if self.model.resource1 or self.model.resource2:
            self.energy -= 1
            # If there is resource available, eat it
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            try:
                resource_patch = next(obj for obj in this_cell if isinstance(obj, GrassPatch2))
            except StopIteration:
                judge1 = False
            else:
                judge1 = resource_patch.fully_grown
            if judge1:
                self.energy += self.model.sheep_gain_from_food * 1.5
                self.para = resource_patch.para
                resource_patch.fully_grown = False

            # Death
            if self.energy < 0:
                self.model.grid.remove_agent(self)
                self.model.schedule.remove(self)
                living = False
                
        reproduce = self.model.sheep_reproduce 
        if living and self.random.random() < reproduce * 1.2:
            # Create a new sheep:
            if self.model.resource1 or self.model.resource2:
                self.energy /= 2
            #if self.random.random() < logistic(-0.02 * self.model.resource / self.model.sheep_num + 1.27) :
            if self.random.random() < 0.5:
                lamb = Sheep2(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy
                )
            else: 
                lamb = Sheep2(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy, False
                )
            self.model.grid.place_agent(lamb, self.pos)
            self.model.schedule.add(lamb)


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None
    para = None
    def __init__(self, unique_id, pos, model, moore, energy=None, para=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.para = para

    def step(self):
        self.random_move()
        self.energy -= 1

        # If there are sheep present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]
        sheep2 = [obj for obj in this_cell if isinstance(obj, Sheep2)]
        if len(sheep) > 0 and len(sheep2) == 0:
            sheep_to_eat = self.random.choice(sheep)
            if sheep_to_eat.sex == 'Male' and self.random.random() < 0.8:
                self.energy += self.model.wolf_gain_from_food
                # Kill the sheep
                if sheep_to_eat.para:
                    self.para = True
                self.model.grid.remove_agent(sheep_to_eat)
                self.model.schedule.remove(sheep_to_eat)
            elif sheep_to_eat.sex == 'Female' :
                self.energy += self.model.wolf_gain_from_food
                # Kill the sheep
                if sheep_to_eat.para:
                    self.para = True
                self.model.grid.remove_agent(sheep_to_eat)
                self.model.schedule.remove(sheep_to_eat)
        elif len(sheep2) > 0 and len(sheep) == 0:
            sheep_to_eat = self.random.choice(sheep2)
            self.energy += self.model.wolf_gain_from_food
            # Kill the sheep
            if sheep_to_eat.para:
                self.para = True
            self.model.grid.remove_agent(sheep_to_eat)
            self.model.schedule.remove(sheep_to_eat)
        elif len(sheep2) > 0 and len(sheep) > 0:
            if self.random.random() < (len(sheep) / (len(sheep) + len(sheep2))):
                sheep_to_eat = self.random.choice(sheep)
                if sheep_to_eat.sex == 'Male' and self.random.random() < 0.8:
                    self.energy += self.model.wolf_gain_from_food
                    # Kill the sheep
                    if sheep_to_eat.para:
                        self.para = True
                    self.model.grid.remove_agent(sheep_to_eat)
                    self.model.schedule.remove(sheep_to_eat)
                elif sheep_to_eat.sex == 'Female' :
                    self.energy += self.model.wolf_gain_from_food
                    # Kill the sheep
                    if sheep_to_eat.para:
                        self.para = True
                    self.model.grid.remove_agent(sheep_to_eat)
                    self.model.schedule.remove(sheep_to_eat)
            else:
                sheep_to_eat = self.random.choice(sheep2)
                self.energy += self.model.wolf_gain_from_food
                # Kill the sheep
                if sheep_to_eat.para:
                    self.para = True
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
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy, False
                )
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)

class Wolf2(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None
    para = None
    def __init__(self, unique_id, pos, model, moore, energy=None, para=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.para = para

    def step(self):
        self.random_move()
        self.energy -= 1

        # If there are sheep present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        try:
            resource_patch = next(obj for obj in this_cell if isinstance(obj, GrassPatch))
        except StopIteration:
            judge1 = False
        else:
            judge1 = resource_patch.fully_grown
        try:
            resource_patch2 = next(obj for obj in this_cell if isinstance(obj, GrassPatch2))
        except StopIteration:
            judge2 = False
        else:
            judge2 = resource_patch2.fully_grown
        if len(sheep) > 0:
            sheep_to_eat = self.random.choice(sheep)
            if sheep_to_eat.sex == 'Male' and self.random.random() < 0.8:
                self.energy += self.model.wolf_gain_from_food * 0.8
                # Kill the sheep
                if sheep_to_eat.para:
                    self.para = True
                self.model.grid.remove_agent(sheep_to_eat)
                self.model.schedule.remove(sheep_to_eat)
            elif sheep_to_eat.sex == 'Female' :
                self.energy += self.model.wolf_gain_from_food * 0.8
                # Kill the sheep
                if sheep_to_eat.para:
                    self.para = True
                self.model.grid.remove_agent(sheep_to_eat)
                self.model.schedule.remove(sheep_to_eat)
        if judge1:
            resource_patch.fully_grown = False
            if resource_patch.para:
                    self.para = True
            self.energy += self.model.sheep_gain_from_food * 0.3
        elif judge2:
            resource_patch2.fully_grown = False
            if resource_patch2.para:
                    self.para = True
            self.energy += self.model.sheep_gain_from_food * 0.2
        # Death or reproduction
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.wolf_reproduce:
                # Create a new wolf cub
                self.energy /= 2
                cub = Wolf2(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy, False
                )
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)

class GrassPatch(mesa.Agent):
    """
    A patch of resource that grows at a fixed rate and it is eaten by sheep
    """
    para = None
    def __init__(self, unique_id, pos, model, fully_grown, countdown, para=None):
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
        self.para = para

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.resource_regrowth_time 
            else:
                self.countdown -= 1


class GrassPatch2(mesa.Agent):
    """
    A patch of resource that grows at a fixed rate and it is eaten by sheep
    """

    para = None
    def __init__(self, unique_id, pos, model, fully_grown, countdown, para=None):
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
        self.para = para

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.resource_regrowth_time * 0.8
            else:
                self.countdown -= 1
        # Recover
        if self.random.random() < 0.005:
            self.para = False

