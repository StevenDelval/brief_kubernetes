🔹 1. À quoi sert un Ingress dans Kubernetes ?

Un Ingress est une ressource Kubernetes qui sert à gérer l’accès HTTP/HTTPS externe à tes services internes du cluster.

🧭 En résumé :
L’Ingress agit comme une table de routage HTTP (reverse proxy) pour orienter le trafic vers le bon Service.

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
  - host: monapp.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-api-service
            port:
              number: 8000

➡️ Cela veut dire :
Quand un utilisateur accède à http://monapp.example.com/api, le trafic est envoyé au service backend-api-service sur le port 8000.

🔹 2. Quelle différence y a-t-il entre un Ingress et un Ingress Controller ?
Élément	Rôle
Ingress	Objet de configuration Kubernetes (décrit les règles de routage HTTP/HTTPS)
Ingress Controller	Composant logiciel (Nginx, Traefik, Azure Application Gateway…) qui lit les objets Ingress et met en œuvre le routage réel
🧠 Analogie :
L’Ingress, c’est le plan de circulation.
L’Ingress Controller, c’est le policier qui lit ce plan et dirige les voitures.
Sans Ingress Controller, un objet Ingress ne fait rien du tout.

3. À quoi sert un health probe dans une architecture de déploiement ?

Un health probe (ou probe de santé) permet à Kubernetes de vérifier automatiquement l’état de santé des conteneurs.

Il en existe 3 types :

Type	But	Action en cas d’échec
livenessProbe	Vérifie si le conteneur est vivant (non bloqué)	Le pod est redémarré
readinessProbe	Vérifie si le conteneur est prêt à recevoir du trafic	Le pod est temporairement retiré du Service
startupProbe	Vérifie que le conteneur a bien fini de démarrer	Empêche les probes précoces

🧩 Dans ton cas (API web), la probe fait souvent une requête HTTP sur une route comme /health ou /ping.

4. Quelle est la relation entre le chemin défini dans l’annotation du probe et les routes réellement exposées par l’application ?

Le chemin du probe doit correspondre à une route réelle exposée par ton application.
Autrement dit, Kubernetes va appeler ce chemin depuis à l’intérieur du cluster (pas via l’Ingress).

Exemple :
livenessProbe:
  httpGet:
    path: /health
    port: 8000

Kubernetes enverra une requête à http://<pod_ip>:8000/health.
Il ne passe ni par l’Ingress ni par le LoadBalancer, mais directement dans le pod.

⚠️ Si ton application n’a pas de route /health, la probe échoue → Kubernetes redémarrera ton conteneur.

5. Comment mettre en place un chemin de préfixe (ex. /votre_namespace) dans l’Ingress, et quelle configuration doit être ajustée pour que ce chemin soit correctement pris en compte par l’application ?
Étape 1 : Définir le préfixe dans l’Ingress

Exemple :

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: backend-api-ingress
  namespace: stdelval
spec:
  rules:
  - host: monapp.example.com
    http:
      paths:
      - path: /stdelval
        pathType: Prefix
        backend:
          service:
            name: backend-api-service
            port:
              number: 8000

Tout ce qui commence par /stdelval est redirigé vers ton service backend-api-service.

Étape 2 : Adapter ton application au chemin de base

Le contrôleur d’ingress ne réécrit pas automatiquement les chemins.
Donc si ton application FastAPI ou Flask est configurée pour répondre à /, elle ne verra pas /stdelval sauf si tu le précises.

6. Comment le contrôleur d’Ingress décide-t-il si un service est “sain” ou non ?

Le contrôleur d’Ingress se base sur l’état des Endpoints du Service, lui-même lié aux readinessProbes des pods.

➡️ Le processus est :

Le Deployment déploie des pods.

Chaque pod a une readinessProbe.

Tant que la probe échoue → le pod est marqué comme non prêt.

Le Service ne dirige aucun trafic vers les pods non prêts.

Le Ingress Controller (NGINX, Traefik, etc.) ne route que vers les endpoints “ready”.

✅ Donc :
Si ton API n’est pas encore prête ou plantée → elle est exclue du load balancing automatiquement

Résumé synthétique
Élément	Rôle / Fonction
Ingress	Règles de routage HTTP/HTTPS vers les Services
Ingress Controller	Implémente le routage (Nginx, Traefik, Azure Gateway…)
Health Probes	Vérifient la santé et la disponibilité des pods
Chemin du probe	Route interne à l’application, appelée directement par Kubernetes
Préfixe Ingress (/namespace)	Routage HTTP via le contrôleur, nécessite config du root_path côté app
Service sain	Déterminé par la réussite de la readinessProbe du pod