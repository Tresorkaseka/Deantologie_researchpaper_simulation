from dotenv import load_dotenv
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule

from agents import TYPE_COLORS
from llm_backend import get_llm_api_key, get_llm_base_url, get_llm_model_name, get_llm_provider
from model import EthicalOrgModel


load_dotenv()


def agent_portrayal(agent):
    if agent is None:
        return None

    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 1,
        "r": 0.8,
    }

    portrayal["Color"] = TYPE_COLORS.get(agent.agent_type, "#999999")

    if agent.agent_type == "leader":
        portrayal["r"] = 1.0
        portrayal["Layer"] = 2
        portrayal["Color"] = TYPE_COLORS["leader"]

    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

chart = ChartModule(
    [
        {"Label": "Ethical", "Color": "#2ecc71"},
        {"Label": "NonEthical", "Color": "#e74c3c"},
        {"Label": "Neutral", "Color": "#f39c12"},
        {"Label": "Leader", "Color": "#3498db"},
    ],
    data_collector_name="datacollector",
)

model_params = {
    "n_agents": UserSettableParameter("slider", "Number of agents", 10, 10, 100, 1),
    "grid_size": 10,
    "institution_strength": UserSettableParameter("slider", "Institutional strength", 0.5, 0.1, 1.0, 0.1),
    "resource_pressure": UserSettableParameter("slider", "Resource pressure", 0.3, 0.1, 1.0, 0.1),
    "threshold": 0.4,
    "alpha": 0.4,
    "beta": 0.4,
    "gamma": 0.2,
    "model_name": get_llm_model_name(),
    "llm_api_key": get_llm_api_key(),
    "llm_provider": get_llm_provider(),
    "llm_base_url": get_llm_base_url(),
}

server = ModularServer(
    EthicalOrgModel,
    [grid, chart],
    "Ethics Simulation (GAMA-style)",
    model_params,
)

server.port = 8521


if __name__ == "__main__":
    print("\nLaunching the visualization server on http://localhost:8521")
    print("The LLM answers will appear here in real time while the agents move in the browser.\n")
    server.launch()
