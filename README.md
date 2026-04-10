
## Choix du modèle et contraintes techniques
Dans ce projet, le choix du modèle s’est porté sur Mistral Small Latest. Ce choix est directement lié aux contraintes de développement. En effet, l’environnement utilisé reposait sur un abonnement freemium ainsi que sur une machine avec des ressources limitées.
L’objectif était donc de trouver un modèle suffisamment performant pour répondre à des cas d’usage concrets, tout en restant léger et rapide à exécuter. Mistral Small représente un bon compromis entre qualité de réponse, latence et coût. Ce choix s’inscrit aussi dans une logique réaliste, proche de ce que l’on peut rencontrer en entreprise lorsqu’il faut optimiser les ressources disponibles.

## Construction de l’agent et ajout de la mémoire
Le modèle a ensuite été transformé en agent grâce à l’utilisation de LangChain. Un prompt système a été défini afin de lui donner un rôle précis d’assistant immobilier, avec des règles de comportement et un périmètre métier clair.
L’agent a également été enrichi avec une mémoire conversationnelle. Cette mémoire permet de conserver le contexte des échanges avec l’utilisateur, ce qui améliore la cohérence des réponses. Cela permet d’éviter que le modèle réponde de manière isolée à chaque question, et se rapproche davantage d’une interaction naturelle.
LangChain joue ici un rôle central, puisqu’il permet à la fois de gérer cette mémoire et de connecter le modèle à des outils externes.

## Externalisation des outils avec MCP
Un choix important dans ce projet a été de ne pas intégrer directement les tools dans le backend. À la place, ils ont été externalisés dans un serveur MCP, accessible via une API sur un port dédié.
Ce serveur a été développé avec FastMCP, qui permet d’exposer des fonctions Python sous forme d’outils utilisables par un modèle de langage. Concrètement, cela signifie que les fonctionnalités comme l’estimation ou l’analyse de marché sont accessibles indépendamment du modèle.
Ce choix permet de rendre l’architecture plus modulaire. Les outils ne dépendent plus directement de l’agent, ce qui ouvre la possibilité de les réutiliser avec d’autres modèles ou d’autres applications. C’est une approche qui se rapproche de ce que l’on peut retrouver dans des architectures orientées services.

## Conteneurisation et orchestration avec Docker
L’ensemble de l’application a été conteneurisé avec Docker. Chaque composant possède son propre environnement : le backend, le serveur MCP et le serveur Nginx.
L’orchestration a été réalisée avec Docker Compose, ce qui permet de gérer facilement les différents services, leurs dépendances et leur communication. Cette approche simplifie le lancement de l’application et garantit une certaine reproductibilité de l’environnement.
Ce choix a également été motivé par une volonté de se rapprocher des pratiques utilisées en entreprise, où la conteneurisation est devenue un standard.

## Mise en place d’un reverse proxy avec Nginx
Dans la continuité de cette logique, un serveur Nginx a été mis en place en tant que reverse proxy. Son rôle est de servir de point d’entrée unique pour l’application et de rediriger les requêtes vers les bons services internes.
Concrètement, cela permet de :centraliser les accès,masquer l’architecture interne,simplifier la gestion des routes entre le backend et le serveur MCP.

Ce choix n’est pas seulement technique. Il est aussi lié à un contexte réel : en entreprise, je suis régulièrement confrontée à des configurations avec Nginx. J’ai donc volontairement intégré cet outil dans le projet afin de mieux comprendre son fonctionnement et de me familiariser avec sa configuration.

## Sécurisation des échanges avec HTTPS
Un autre point important du projet concerne la sécurité des communications. Un certificat SSL autosigné a été généré afin de permettre un fonctionnement en HTTPS.
Même si ce type de certificat n’est pas destiné à la production, il permet de reproduire des conditions réelles :
les navigateurs exigent une connexion sécurisée, certaines fonctionnalités ne fonctionnent correctement qu’en HTTPS, les échanges sont chiffrés.
Cela m’a permis de travailler concrètement sur des aspects souvent rencontrés en entreprise, comme la gestion des certificats, leur intégration dans Nginx, et la configuration des ports sécurisés.

## Justification globale des choix techniques
Globalement, les choix techniques réalisés dans ce projet ne sont pas uniquement liés au besoin fonctionnel. Ils s’inscrivent aussi dans une démarche d’apprentissage orientée vers des problématiques concrètes rencontrées en entreprise.
L’utilisation de Nginx, du HTTPS, de Docker et d’une architecture distribuée avec un serveur MCP répond à une volonté de ne pas se limiter à un simple prototype d’agent IA. L’objectif était plutôt de comprendre comment intégrer ce type de système dans un environnement plus réaliste, avec des contraintes d’infrastructure, de sécurité et de déploiement.
Ce projet a donc été construit de manière progressive, avec une logique itérative. Certaines parties, comme DataLab, n’ont pas pu être approfondies, mais cela n’a pas empêché de développer une vision globale du fonctionnement d’une application complète, allant du modèle jusqu’à son exposition sécurisée.
