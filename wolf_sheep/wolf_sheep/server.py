import mesa
from wolf_sheep.agents2 import GrassPatch, Sheep, Wolf, GrassPatch2, Sheep2, Wolf2
from wolf_sheep.model2 import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Sheep:
        if agent.stuck:
            portrayal["Color"] = ["#A730C8"]
        else:
            portrayal["Color"] = ["#768B90"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Wolf:
        portrayal["Shape"] = "wolf_sheep/resources/wolf.png"
        # https://icons8.com/web-app/36821/German-Shepherd
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
    
    elif type(agent) is GrassPatch2:
        if agent.fully_grown:
            portrayal["Color"] = ["#201E9B"]
        else:
            portrayal["Color"] = ["#8E8CF9"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Species_E", "Color": "#AA0000"},
        {"Label": "Lamprey(male)", "Color": "#E2D246"},
        {"Label": "Lamprey(female)", "Color": "#A626B5"},
        {"Label": "Species_B", "Color": "#00AA00"},
        {"Label": "Species_A", "Color": "#201E9B"},
        {"Label": "Species_C", "Color": "#1CDCD3"},
        {"Label": "Species_D", "Color": "#EB8E17"},
        {"Label": "Parasite", "Color": "#171614"},
    ]
)

model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("Parameters:"),
    "resource1": mesa.visualization.Checkbox("Grass Enabled", True),
    "resource_regrowth_time": mesa.visualization.Slider("Grass Regrowth Time", 25, 1, 50),
    "initial_sheep": mesa.visualization.Slider(
        "Initial Sheep Population", 30, 0, 300
    ),
    "sheep_reproduce": mesa.visualization.Slider(
        "Sheep Reproduction Rate", 0.06, 0.01, 1.0, 0.01
    ),
    "initial_wolves": mesa.visualization.Slider("Initial Wolf Population", 5, 0, 100),
    "wolf_reproduce": mesa.visualization.Slider(
        "Wolf Reproduction Rate",
        0.05,
        0.01,
        1.0,
        0.01,
        description="The rate at which wolf agents reproduce.",
    ),
    "wolf_gain_from_food": mesa.visualization.Slider(
        "Wolf Gain From Food Rate", 15, 1, 50
    ),
    "sheep_gain_from_food": mesa.visualization.Slider("Sheep Gain From Food", 5, 0, 10),
}

server = mesa.visualization.ModularServer(
    WolfSheep, [canvas_element, chart_element], "Wolf Sheep Predation", model_params
)
server.port = 8521
