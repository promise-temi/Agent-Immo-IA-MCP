
import pandas as pd
import os
from pathlib import Path
import sys
root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_path))
from langchain.tools import tool

@tool
def moyenne_prix_bien_selon_surface_habitable(surface_habitable_souhaite:object, type_souhaite:list, communes_souhaite:list[str]) -> list[dict]:  
    """
    Estime les prix immobiliers (min, max, moyen) en fonction de la surface habitable,
    du type de bien et des communes ciblées.

    Cette fonction doit être utilisée APRÈS geocode_localisations(), afin de garantir
    que la liste des communes est constituée de codes postaux valides.

    PARAMÈTRES :
    ------------
    surface_habitable_souhaite : dict
        Dictionnaire contenant les bornes de surface :
            - {'min': x, 'max': y}
            - {'min': x, 'max': False}
            - {'min': False, 'max': y}
            - {'min': False, 'max': False}
            - surface idéale : {'min': x-1, 'max': x+1}

    type_souhaite : list
        Liste optionnelle de types de biens :
            ['Maison'], ['Appartement'], ['Dépendance'], ['Local industriel'], etc.
        Peut être vide.

    communes_souhaite : list[str]
        Liste de codes postaux (déjà géocodés via geocode_localisations).

    UTILISATION PAR LE MODÈLE :
    ---------------------------
    1. L'utilisateur exprime une recherche basée sur la surface (ex : "Je veux un logement de 50 m²").
    2. Le modèle convertit les localisations en codes postaux via geocode_localisations().
    3. Le modèle appelle cette fonction pour obtenir :
        - prix minimum
        - prix maximum
        - prix moyen
      pour chaque commune.

    RETOUR :
    --------
    list[dict] :
        [
            {
                'commune': '37000',
                'min': 120000,
                'max': 350000,
                'mean': 220000
            },
            ...
        ]

    OBJECTIF :
    ----------
    Permettre au modèle IA de fournir une estimation immobilière réaliste et contextualisée
    en fonction des critères fournis par l'utilisateur.
    """

    print(__file__)
    # ---- load data from data repository  ----
    df = pd.read_parquet('../Data/ValeursFoncieres-2025.parquet')

    # ---- gerer les cas où l'utilisateur ne fournit pas de surface habitable minimale ou maximale ----
    if not surface_habitable_souhaite['min']:
        surface_habitable_souhaite['min'] = 1 
    if not surface_habitable_souhaite['max']:
        surface_habitable_souhaite['max'] = 100000

    # ---- filtrer les données en fonction des critères de l'utilisateur et calculer les statistiques pour chaque commune ----
    results = []
    for commune in communes_souhaite:
        df_ = df[(df["Surface reelle bati"] > surface_habitable_souhaite['min']) & (df["Surface reelle bati"] < surface_habitable_souhaite['max'])]
        if len(type_souhaite) > 0:
            df_1 = df_[df_['Code type local'].isin(values=type_souhaite)]
        else:
            df_1=df_
        df_2 = df_1[df_1['Code postal']== commune]
        # df_2['Valeur fonciere'] = df_2['Valeur fonciere'].str.replace(',','.').astype(float)
        df_mean = df_2['Valeur fonciere'].mean()
        
        
        df_max = df_2['Valeur fonciere'].max()
        df_min = df_2['Valeur fonciere'].min()
    
        result = {
            'commune': str(commune),
            'max' : int(df_max),
            'min' : int(df_min),
            'mean': int(df_mean),

        }
        results.append(result)
    return results



