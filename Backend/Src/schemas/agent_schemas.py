from pydantic import BaseModel
from pathlib import Path
import sys

# configuration du chemin vers le point d'entrée de l'application
root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root_path))



class AgentRequest(BaseModel):
    content: object


class AgentResponse(BaseModel):
     response: str