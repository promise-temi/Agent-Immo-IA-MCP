from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Facultatif si tu veux garder webdriver-manager
from webdriver_manager.firefox import GeckoDriverManager




urls = {
  "raisons_confier_pro": {
    "description": "5 raisons de confier son projet immobilier à un professionnel",
    "url": "https://www.fnaim.fr/4214-5-raisons-de-confier-votre-projet-immobilier-a-un-professionnel-fnaim.htm"
  },
  "vendre_bien_choix": {
    "description": "Conseils pour bien vendre un bien immobilier",
    "url": "https://www.fnaim.fr/3716-vendre-un-bien-immobilier-faites-les-bons-choix.htm"
  },
  "vendre_constituer_dossier": {
    "description": "Constituer son dossier avant de vendre un bien",
    "url": "https://www.fnaim.fr/3717-vendre-son-bien-constituer-d-abord-son-dossier.htm"
  },
  "estimer_bien_pourquoi": {
    "description": "Pourquoi faire estimer son bien par un professionnel",
    "url": "https://www.fnaim.fr/3706-pourquoi-faire-estimer-son-bien-immobilier-par-un-professionnel-.htm"
  },
  "mandat_vente": {
    "description": "Mandat de vente : ce qu'il faut savoir",
    "url": "https://www.fnaim.fr/3362-mandat-de-vente-que-faut-il-savoir.htm"
  },
  "faire_estimer_bien": {
    "description": "Faire estimer son bien immobilier",
    "url": "https://www.fnaim.fr/3636-faire-estimer-son-bien-immobilier.htm"
  },
  "preparer_dossier_location": {
    "description": "Comment préparer son dossier de location",
    "url": "https://www.fnaim.fr/3712-comment-preparer-son-dossier-de-location.htm"
  },
  "charges_locatives": {
    "description": "Charges locatives : qui paie quoi et régularisation",
    "url": "https://www.fnaim.fr/3708-charges-locatives-qui-paie-quoi-et-regularisation.htm"
  },
  "renouvellement_contrat_location": {
    "description": "Renouvellement de contrat de location : modalités",
    "url": "https://www.fnaim.fr/3317-renouvellement-contrat-location-quelles-modalites.htm"
  },
  "etat_des_lieux": {
    "description": "État des lieux d'entrée et de sortie",
    "url": "https://www.fnaim.fr/3476-etat-des-lieux-entree-et-sortie-soyez-precis-et-attentif.htm"
  },
  "reparations_locatives": {
    "description": "Réparations locatives : locataire vs propriétaire",
    "url": "https://www.fnaim.fr/3718-reparations-locatives-travaux-charge-locataire-proprietaire.htm"
  },
  "bail_colocation": {
    "description": "Bail de colocation : précautions à prendre",
    "url": "https://www.fnaim.fr/3394-bail-de-colocation-quelles-sont-les-precautions.htm"
  },
  "coproprietaires_droits": {
    "description": "Droits et obligations des copropriétaires",
    "url": "https://www.fnaim.fr/3720-coproprietaires-quels-sont-vos-droits-et-obligations.htm"
  },
  "syndic_role": {
    "description": "Syndic de copropriété : rôle et missions",
    "url": "https://www.fnaim.fr/3701-syndic-de-copropriete-quel-role-quelles-missions.htm"
  },
  "choisir_syndic": {
    "description": "Comment choisir son syndic de copropriété",
    "url": "https://www.fnaim.fr/3748-comment-choisir-son-syndic-de-copropriete.htm"
  },
  "loi_alur_copropriete": {
    "description": "Loi ALUR : changements pour la copropriété",
    "url": "https://www.fnaim.fr/3749-loi-alur-copropriete-quels-changements.htm"
  },
  "assemblee_generale": {
    "description": "Tout savoir sur l'assemblée générale de copropriété",
    "url": "https://www.fnaim.fr/3475-tout-savoir-sur-assemblee-generale-copropriete.htm"
  },
  "investissement_patrimoine": {
    "description": "Investissement immobilier : se créer un patrimoine",
    "url": "https://www.fnaim.fr/3699-investissement-immobilier-comment-se-creer-un-patrimoine.htm"
  },
  "assurance_loyers_impayes": {
    "description": "Assurance loyers impayés : solutions",
    "url": "https://www.fnaim.fr/3707-assurance-loyers-impayes-quelles-sont-les-solutions.htm"
  },
  "location_meublee": {
    "description": "Location meublée : avantages",
    "url": "https://www.fnaim.fr/3363-location-meublee-quels-avantages.htm"
  },
  "taxes_proprietaire": {
    "description": "Taxes et impôts du propriétaire",
    "url": "https://www.fnaim.fr/3711-taxes-proprietaire-et-impots.htm"
  },
  "creer_sci": {
    "description": "Créer une SCI : comment et avantages",
    "url": "https://www.fnaim.fr/3332-creer-une-sci-comment-quels-avantages.htm"
  },
  "investir_scpi_retraite": {
    "description": "Investir en SCPI pour la retraite",
    "url": "https://www.fnaim.fr/3860-investir-scpi-retraite.htm"
  },
  "agrandissement_maison": {
    "description": "Agrandissement de maison : étapes et autorisations",
    "url": "https://www.fnaim.fr/3265-agrandissement-maison-etapes-autorisations.htm"
  },
  "aides_renovation_energetique": {
    "description": "Aides pour la rénovation énergétique",
    "url": "https://www.fnaim.fr/3842-aides-renovation-energetique.htm"
  },
  "diagnostics_obligatoires": {
    "description": "Diagnostics immobiliers obligatoires",
    "url": "https://www.fnaim.fr/3536-diagnostics-immobiliers-obligatoires.htm"
  },
  "conseils_demenager": {
    "description": "Conseils pour déménager",
    "url": "https://www.fnaim.fr/3531-nos-conseils-pour-demenager.htm"
  }
}


def PreConseils_Immobiliers() -> object:
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
    return urls







def _create_driver():
    options = Options()
    # utile sur serveur / uvicorn / environnement sans affichage
    options.add_argument("-headless")

    # Option A : garder webdriver-manager
    service = Service(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)

    # Option B : recommandé avec Selenium récent
    # return webdriver.Firefox(options=options)



def Conseils_Immobiliers(code_url):
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


    if code_url not in urls:
        raise ValueError(f"Code URL inconnu : {code_url}")

    url = urls[code_url]["url"]
    driver = _create_driver()

    try:
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.contentParagraphe"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        paragraphs = soup.select("div.contentParagraphe")

        full_text = " ".join(p.get_text(" ", strip=True) for p in paragraphs)
        return full_text

    finally:
        driver.quit()