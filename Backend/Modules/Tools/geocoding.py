import pgeocode
from langchain.tools import tool



@tool
def geocode_localisations(localisations: list[str]) -> list[str]:
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
    
    nomi = pgeocode.Nominatim("fr")
    codes_postaux = set()

    for loc in localisations:
        loc = loc.strip()

        # ✅ 1. Déjà un code postal
        if loc.isdigit() and len(loc) == 5:
            codes_postaux.add(loc)
            continue

        # ✅ 2. Recherche simple avec pgeocode
        try:
            result = nomi.query_postal_code(loc)

            # pgeocode retourne souvent une Series
            if result is not None and hasattr(result, "postal_code"):
                cp = result.postal_code

                if isinstance(cp, str) and cp.isdigit():
                    codes_postaux.add(cp)

        except Exception as e:
            print("Erreur geocode :", e)

    return sorted(codes_postaux)