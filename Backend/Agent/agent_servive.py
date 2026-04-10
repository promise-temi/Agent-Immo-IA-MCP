# noqa
# Import des librairies
import os

from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import BaseTool
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


import sys
from pathlib import Path
root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_path))

from Llm.llm_service import llm_model, PROMPT_SYSTEM
from Modules.Tools.Advices import PreConseils_Immobiliers, Conseils_Immobiliers
from Modules.Tools.geocoding import geocode_localisations
from Modules.Tools.Possible_parameters_per_price import surface_habitable_selon_prix
from Modules.Tools.Tool_Price_per_parameters import moyenne_prix_bien_selon_surface_habitable


load_dotenv()


LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")


if "LANGSMITH_API_KEY" not in os.environ:
   raise ValueError("La variable d'environnement LANGSMITH_API_KEY est introuvable.")
os.environ["LANGSMITH_TRACING"] = "true"

tools = [PreConseils_Immobiliers, Conseils_Immobiliers, geocode_localisations, surface_habitable_selon_prix, moyenne_prix_bien_selon_surface_habitable]


memory = InMemorySaver()






agent = create_agent(
    model=llm_model,
    tools=tools,
    system_prompt=PROMPT_SYSTEM,
    checkpointer=memory
)


def agent_run(user_prompt: str, thread_id: str = "default"):
    return agent.invoke(
        {"messages": [{"role": "user", "content": user_prompt}]},
        config={"configurable": {"thread_id": thread_id}}
    )