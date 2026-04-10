import pandas as pd
import os
from pathlib import Path
import sys
root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_path))
from langchain.tools import tool

@tool
def surface_habitable_selon_prix(valeurs_foncieres:dict, type_souhaite:list, communes_souhaite:list[str]) -> list[dict]:  
    
    """
    Estime les surfaces habitables (min, max, moyenne) accessibles en fonction d'un budget donné.

    Cette fonction est l'inverse de moyenne_prix_bien_selon_surface_habitable :
    - au lieu de filtrer par surface pour obtenir un prix,
      elle filtre par prix pour obtenir une surface.

    Elle doit être utilisée APRÈS geocode_localisations().

    PARAMÈTRES :
    ------------
    valeurs_foncieres : dict
        Dictionnaire contenant les bornes de prix :
            - {'min': x, 'max': y}
            - {'min': x, 'max': False}
            - {'min': False, 'max': y}
            - {'min': False, 'max': False}

    type_souhaite : list
        Liste optionnelle de types de biens (peut être vide).

    communes_souhaite : list[str]
        Liste de codes postaux valides.

    UTILISATION PAR LE MODÈLE :
    ---------------------------
    1. L'utilisateur exprime un budget (ex : "J'ai 200 000 €, que puis-je acheter ?").
    2. Le modèle géocode les localisations éventuelles.
    3. Le modèle appelle cette fonction pour obtenir :
        - surface minimale
        - surface maximale
        - surface moyenne
      pour chaque commune.

    RETOUR :
    --------
    list[dict] :
        [
            {
                'commune': '37100',
                'min': 35,
                'max': 120,
                'mean': 68
            },
            ...
        ]

    OBJECTIF :
    ----------
    Permettre au modèle IA de répondre aux questions du type :
        - "Quelle surface puis-je acheter avec mon budget ?"
        - "Quel type de logement est accessible dans cette zone ?"
        - "Comment varie la surface selon les communes ?"

    Si les paramètres fournis sont trop restrictifs et ne correspondent à aucune donnée,
    la fonction renvoie un message explicatif.
    """

    print(__file__)
    # ---- load data from data repository  ----
    df = pd.read_parquet('../Data/ValeursFoncieres-2025.parquet')

    # ---- gerer les cas où l'utilisateur ne fournit pas de surface habitable minimale ou maximale ----
    if not valeurs_foncieres['min']:
        valeurs_foncieres['min'] = 1 
    if not valeurs_foncieres['max']:
        valeurs_foncieres['max'] = 10000000000

    # ---- filtrer les données en fonction des critères de l'utilisateur et calculer les statistiques pour chaque commune ----
    results = []
    for commune in communes_souhaite:
        df_ = df[(df["Valeur fonciere"] > valeurs_foncieres['min']) & (df["Valeur fonciere"] < valeurs_foncieres['max'])]
        if len(type_souhaite) > 0:
            df_1 = df_[df_['Code type local'].isin(values=type_souhaite)]
        else:
            df_1=df_
        df_2 = df_1[df_1['Code postal']== commune]
        # df_2['Valeur fonciere'] = df_2['Valeur fonciere'].str.replace(',','.').astype(float)
        df_mean = df_2['Surface reelle bati'].mean()
        
        
        df_max = df_2['Surface reelle bati'].max()
        df_min = df_2['Surface reelle bati'].min()
        print(df_mean)
        print(df_min)
        print(df_max)
        try:
            result = {
                'commune': str(commune),
                'max' : int(df_max),
                'min' : int(df_min),
                'mean': int(df_mean),

            }
        except:
            return "les valeurs entrée en paramètre ne sont pas adaptée... beaucoup trop petites ou rigide bref nest pas réalistes au marché"

        results.append(result)
    return results