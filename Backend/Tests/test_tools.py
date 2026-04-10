import pytest 
from pathlib import Path
import sys
root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_path))

from Modules.Tools.Tool_Price_per_parameters import moyenne_prix_bien_selon_surface_habitable
from Modules.Tools.Possible_parameters_per_price import surface_habitable_selon_prix



def test_moyenne_prix_bien_selon_surface_habitable_multiple():
    result = moyenne_prix_bien_selon_surface_habitable({'min':20, 'max':60}, [2,3], [37000, 37170])
    # Doit etre une liste
    assert isinstance(result, list)
    # Doit contenir 2 élements
    assert len(result)  == 2 
    # Pour chaques resultat doit remplir les conditions
    for res in result :
        assert isinstance(res['commune'] , str)
        assert isinstance(res['max'], int)
        assert isinstance(res['min'], int)
        assert isinstance(res['mean'], int)

def test_moyenne_prix_bien_selon_surface_habitable_unique():
    result = moyenne_prix_bien_selon_surface_habitable({'min':20, 'max':60}, [], [])
    # Doit etre une liste
    assert isinstance(result, list)
    # Doit contenir 2 élements
    assert len(result)  == 0




def test_surface_habitable_selon_prix_multiple():
    result = surface_habitable_selon_prix({'min':100_000, 'max':250_000}, [2,3], [37000, 37170])
    # Doit etre une liste
    assert isinstance(result, list)
    # Doit contenir 2 élements
    assert len(result)  == 2 
    # Pour chaques resultat doit remplir les conditions
    for res in result :
        assert isinstance(res['commune'] , str)
        assert isinstance(res['max'], int)
        assert isinstance(res['min'], int)
        assert isinstance(res['mean'], int)

def test_surface_habitable_selon_prix_unique():
    result = surface_habitable_selon_prix({'min':20, 'max':60}, [2,3], [37000, 37170])
    # Doit etre une liste
    assert isinstance(result, str)
    
    

