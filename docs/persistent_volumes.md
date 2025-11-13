🔹 1. Quel est le rôle d’un volume dans un déploiement Kubernetes ?

Un volume dans Kubernetes sert à fournir un espace de stockage accessible par un ou plusieurs conteneurs d’un pod.

➡️ Sans volume :
Les données écrites dans un conteneur sont éphémères — elles disparaissent dès que le pod est redémarré ou recréé.

➡️ Avec un volume :
Les données sont conservées sur un espace externe (disque, réseau, cloud storage) et peuvent être réutilisées même si le pod change.

🧠 En résumé :
Le volume permet de séparer la durée de vie des données de celle du pod.

🔹 2. Que signifie la mention storageClassName dans un PVC, et que peut-elle impliquer côté cloud ?

Le champ storageClassName dans un PersistentVolumeClaim (PVC) indique quel type de stockage Kubernetes doit utiliser pour satisfaire la demande.

Exemple :
storageClassName: managed-premium


Sur Azure, cela peut correspondre à :

un Azure Managed Disk (Premium SSD, Standard SSD, HDD),

avec des paramètres automatiques de performance, chiffrement, disponibilité, etc.

💡 Concrètement :

Kubernetes demande à Azure de créer un disque selon cette classe.

Azure crée automatiquement un Azure Disk avec les bonnes caractéristiques.

Ainsi, storageClassName agit comme un profil de stockage cloud.

🔹 3. Que se passe-t-il si le pod MySQL disparaît ?

Si ton pod MySQL est supprimé, redémarré ou migré vers un autre nœud :

Le conteneur MySQL est recréé.

Le PVC reste inchangé.

Le volume (Azure Disk) est réattaché automatiquement au nouveau pod.

MySQL retrouve exactement les mêmes fichiers de données.

✅ Résultat : les données de la base restent intactes.
⚠️ Seule la perte du PVC (ou du disque associé) effacerait les données.

🔹 4. Qu’est-ce qui relie un PersistentVolumeClaim à un volume physique ?

Le lien se fait via le contrôle de correspondance entre le PVC et un PV (PersistentVolume) :

Le PVC décrit ce qu’il veut (taille, mode d’accès, classe de stockage).

Kubernetes cherche ou crée un PV (volume réel) qui satisfait cette demande.

Une fois trouvé ou créé, le PV est "bindé" (lié) au PVC.

Sur le cloud (Azure, AWS, GCP) :

Ce PV correspond souvent à un disque physique (Azure Disk, EBS, Persistent Disk…).

Ce lien est géré automatiquement grâce au provisioner de la StorageClass.

🧩 En résumé :
PVC = demande de stockage
PV = volume réel (le disque Azure)
StorageClass = mode de création et type du disque

🔹 5. Comment le cluster gère-t-il la création ou la suppression du stockage sous-jacent ?

Cela dépend du provisioning défini dans la StorageClass :

🧱 Cas courant : Dynamic Provisioning (automatique)

Quand tu crées un PVC, Kubernetes demande automatiquement au cloud provider (Azure, ici) de créer un disque.

Quand tu supprimes le PVC, Kubernetes peut aussi supprimer le disque, selon la politique de reclaim.

⚙️ Politique de Reclaim Policy :

Définie dans le StorageClass (par défaut Delete sur AKS).

Reclaim Policy	Effet
Delete	Le disque Azure est supprimé quand le PVC est supprimé
Retain	Le disque reste sur Azure (utile si tu veux garder les données)
Recycle	Obsolète – réinitialise le volume (peu utilisé aujourd’hui)