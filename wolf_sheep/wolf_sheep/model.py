"""
Wolf-Sheep Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

import mesa

from .agents import GrassPatch, Sheep, Wolf
from .scheduler import RandomActivationByTypeFiltered


class WolfSheep(mesa.Model):
    """
    Wolf-Sheep Predation Model
    """

    height = 20
    width = 20

    initial_sheep = 100
    initial_wolves = 50

    sheep_reproduce = 0.04
    wolf_reproduce = 0.05

    wolf_gain_from_food = 20

    resource = False
    resource_regrowth_time = 30
    sheep_gain_from_food = 4
    initial_rate = 0.5,

    verbose = False  # Print-monitoring

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
        self,
        width=20,
        height=20,
        initial_sheep=20,
        initial_wolves=50,
        sheep_reproduce=0.04,
        wolf_reproduce=0.05,
        wolf_gain_from_food=20,
        resource=False,
        resource_regrowth_time=30,
        sheep_gain_from_food=0.4,
        initial_rate = 0.5,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            resource: Whether to have the sheep eat resource for energy
            resource_regrowth_time: How long it takes for a resource patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from resource, if enabled.
        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.sheep_num = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.resource = resource
        self.resource_regrowth_time = resource_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        self.rate = initial_rate
        self.initial_male = self.sheep_num * self.rate

        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        self.datacollector = mesa.DataCollector(
            {
                "Predator": lambda m: m.schedule.get_type_count(Wolf),
                "Lamprey(male)": lambda m: m.schedule.get_type_count(Sheep, lambda x: x.sex == 'Male'),
                "Lamprey(female)": lambda m: m.schedule.get_type_count(Sheep, lambda x: x.sex == 'Female'),
                "Resource": lambda m: m.schedule.get_type_count(
                    GrassPatch, lambda x: x.fully_grown
                ),
            }
        )

        # Create sheep:
        for i in range(self.sheep_num):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.sheep_gain_from_food)
            sex = 'Male' if i < self.initial_male else 'Female'
            sheep = Sheep(self.next_id(), (x, y), self, True, energy, sex)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

        # Create wolves
        for i in range(self.initial_wolves):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(2 * self.wolf_gain_from_food)
            wolf = Wolf(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

        # Create resource patches
        if self.resource:
            for agent, (x, y) in self.grid.coord_iter():
                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.resource_regrowth_time
                else:
                    countdown = self.random.randrange(self.resource_regrowth_time)

                patch = GrassPatch(self.next_id(), (x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_type_count(Wolf),
                    self.schedule.get_type_count(Sheep),
                    self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown),
                ]
            )
        self.sheep_num = self.schedule.get_type_count(Sheep)
        self.resource = self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown)
        self.male_num = self.schedule.get_type_count(Sheep, lambda x: x.sex == 'Male')
        self.rate = self.male_num / self.sheep_num
        #self.rate = 0.5

    def run_model(self, step_count=200):
        if self.verbose:
            print("Initial number wolves: ", self.schedule.get_type_count(Wolf))
            print("Initial number sheep: ", self.schedule.get_type_count(Sheep))
            print(
                "Initial number resource: ",
                self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown),
            )

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Final number wolves: ", self.schedule.get_type_count(Wolf))
            print("Final number sheep: ", self.schedule.get_type_count(Sheep))
            print(
                "Final number resource: ",
                self.schedule.get_type_count(GrassPatch, lambda x: x.fully_grown),
            )