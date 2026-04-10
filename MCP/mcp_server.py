from fastmcp import FastMCP
from Tools.Advices import PreConseils_Immobiliers, Conseils_Immobiliers
from Tools.geocoding import geocode_localisations
from Tools.Possible_parameters_per_price import surface_habitable_selon_prix
from Tools.Tool_Price_per_parameters import moyenne_prix_bien_selon_surface_habitable

server = FastMCP("Agent-Immo-IA-MCP")

@server.tool()
def PreConseils_Immobiliers_() -> object:
    """
    Fournit au modèle l'ensemble des ressources documentaires immobilières FNAIM.

    Cette fonction doit être appelée AVANT Conseils_Immobiliers().

    Elle renvoie un dictionnaire où chaque clé correspond à un article immobilier,
    et chaque valeur contient :
        - "description" : résumé court du sujet de l'article
        - "url" : lien vers l'article FNAIM

    UTILISATION PAR LE MODÈLE :
    ---------------------------
    1. Le modèle reçoit une question utilisateur.
    2. Il parcourt les descriptions retournées par PreConseils_Immobiliers().
    3. Il identifie la clé de l'article le plus pertinent.
    4. Il appelle ensuite Conseils_Immobiliers(cle_article) pour obtenir le texte complet.
    5. Il utilise ce texte comme source fiable pour formuler sa réponse.

    OBJECTIF :
    ----------
    Fournir au modèle une liste structurée d'articles FNAIM fiables afin
    d'améliorer la précision et la qualité des réponses immobilières.

    RETURNS :
        dict : { cle_article : { "description": str, "url": str } }
    """
    return PreConseils_Immobiliers()

@server.tool()
def Conseils_Immobiliers_(code_url:str) -> str: 
    """
    Récupère le contenu textuel complet d'un article immobilier 
    à partir de sa clé (code_url).

    La fonction :
        - charge la page web associée à la clé
        - extrait les paragraphes pertinents (div.contentParagraphe)
        - renvoie un texte propre et exploitable par le modèle

    UTILISATION PAR LE MODÈLE :
    ---------------------------
    1. Le modèle sélectionne une clé pertinente via PreConseils_Immobiliers().
    2. Il appelle Conseils_Immobiliers(code_url).
    3. La fonction renvoie le texte complet de l'article.
    4. Le modèle utilise ce texte comme base documentaire pour répondre à l'utilisateur.

    EXEMPLE :
    ---------
    Question : "Quelles réparations sont à la charge du locataire ?"
    1. PreConseils_Immobiliers() → repère la clé "reparations_locatives"
    2. Conseils_Immobiliers("reparations_locatives")
    3. Retour : texte complet de l'article FNAIM
    4. Le modèle synthétise et répond.

    PARAMÈTRES :
        code_url (str) : clé retournée par PreConseils_Immobiliers()

    RETURNS :
        str : texte complet de l'article, prêt à être analysé par le modèle IA
    """
    return Conseils_Immobiliers(code_url)


@server.tool()
def geocode_localisations_(localisations: list[str]) -> list[str]:
    """
    Convertit une liste de localisations textuelles en une liste exhaustive de codes postaux.

    Cette fonction doit être utilisée AVANT les fonctions d'estimation immobilière
    (moyenne_prix_bien_selon_surface_habitable et surface_habitable_selon_prix),
    car l'utilisateur ne fournit pas toujours de code postal. Elle permet au modèle
    d'interpréter correctement des entrées telles que :
        - noms de villes ("Tours", "Orléans")
        - départements ("Indre-et-Loire", "Loiret")
        - régions ("Centre-Val de Loire")
        - codes postaux déjà valides ("37000")

    COMPORTEMENT :
    --------------
    - Si l'entrée est déjà un code postal valide → ajouté directement.
    - Si l'entrée est un nom de ville → retourne tous les codes postaux associés.
    - Si l'entrée est un département ou une région → retourne l'ensemble des codes postaux correspondants.
    - Les doublons sont supprimés et la liste finale est triée.

    UTILISATION PAR LE MODÈLE :
    ---------------------------
    1. L'utilisateur pose une question impliquant une localisation.
    2. Le modèle extrait les localisations textuelles.
    3. Le modèle appelle geocode_localisations() pour obtenir une liste fiable de codes postaux.
    4. Cette liste est ensuite utilisée dans les fonctions d'estimation immobilière.

    RETURNS:
        list[str] : liste triée de codes postaux uniques.
    """
    return geocode_localisations(localisations)


@server.tool()
def surface_habitable_selon_prix_(valeurs_foncieres:dict, type_souhaite:list, communes_souhaite:list[str]) -> list[dict]:  
    
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
    return surface_habitable_selon_prix(valeurs_foncieres, type_souhaite, communes_souhaite)


@server.tool()
def moyenne_prix_bien_selon_surface_habitable_(surface_habitable_souhaite:object, type_souhaite:list, communes_souhaite:list[str]) -> list[dict]:  
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
    return moyenne_prix_bien_selon_surface_habitable(surface_habitable_souhaite, type_souhaite, communes_souhaite)



if __name__ == "__main__":
    server.run(transport='http', host="0.0.0.0", port=8001)
