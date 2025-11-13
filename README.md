# 🐳 Kubernetes - Déploiement Backend

Ce README décrit les étapes nécessaires pour installer **Minikube**, se connecter à un cluster **Azure Kubernetes Service (AKS)** et déployer un **backend** dans un namespace dédié.

---

## 🧩 I. Installation de Minikube (en local)

### 1. Télécharger et installer Minikube (Linux x86-64)

Exécutez les commandes suivantes pour installer la dernière version stable de **Minikube** :

```bash
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```

### 2. Démarrer Minikube

Depuis un terminal avec des droits administrateur (sans être connecté en tant que root) :


```bash
minikube start
```

### 3. Vérifier le cluster

kubectl est installé, vous pouvez vérifier le bon fonctionnement du cluster :

```bash
kubectl get po -A
```

## ☁️ II. Connexion à Azure et au cluster Kubernetes

### 1. Connexion à Azure

Connectez votre terminal à votre compte Azure : :

```bash
az login --tenant <votre_tenant_id>
```

### 2. Connexion du kubectl local au cluster AKS

Récupérez les informations d’accès au cluster Kubernetes :


```bash
az aks get-credentials --resource-group RG_PROMO --name <votre_cluster_kubernetes>
```

### 3. Vérifier et gérer les contextes disponibles

Afficher les contextes configurés :

```bash
kubectl config get-contexts
```

Sélectionner le cluster <votre_cluster_kubernetes> :

```bash
kubectl config use-context <votre_cluster_kubernetes>
```


### 4. Vérifications de base

Afficher toutes les ressources du cluster :

```bash
kubectl get all
```

Afficher les informations du cluster :

```bash
kubectl cluster-info
```

## 🧱 III. Création et configuration d’un Namespace

Créer un nouveau namespace :

```bash
kubectl create namespace <your_namespace>
```

Définir le namespace par défaut pour la session actuelle :

```bash
kubectl config set-context --current --namespace=<your_namespace>
```

## 🚀 IV. Déploiement et gestion du backend

### 1. Nettoyage complet du namespace (si nécessaire)

Avant un nouveau déploiement, il est recommandé de supprimer toutes les ressources existantes dans le namespace :

```bash
kubectl delete all --all -n <your_namespace>          # Supprime tous les pods, services et déploiements
kubectl delete secrets --all -n <your_namespace>      # Supprime tous les secrets
kubectl delete configmaps --all -n <your_namespace>   # Supprime tous les ConfigMaps
kubectl delete ingress --all -n <your_namespace>      # Supprime tous les Ingress
```

### 2. Application des fichiers de configuration

Déployez ensuite les différentes ressources nécessaires au backend :

```bash
kubectl apply -f config_map_secrets.yaml
kubectl apply -f pvc_database.yaml
kubectl apply -f database.yaml
kubectl apply -f api.yaml
kubectl apply -f streamlit.yaml
kubectl apply -f ingress.yaml
```

### 3. Accès au backend en local

Vous pouvez rediriger le port local vers le service du backend pour accéder à l’API :

```bash
kubectl port-forward service/backend-api-service 8000:8000
```

### 4. Suppression complète des ressources (tous namespaces confondus)

En cas de nettoyage global du cluster (toutes namespaces inclus) :

```bash
kubectl delete all --all
kubectl delete secrets --all
kubectl delete configmaps --all
kubectl delete ingress --all
```

### 5. Vérification de l’Ingress Controller

Pour vérifier le service de l’Ingress NGINX déployé :
```bash
kubectl get svc -n ingress-nginx
```

kubectl get pods 
kubectl logs pod_name
kubectl port-forward svc/frontend-streamlit-service 8501:8501 -n stdelval