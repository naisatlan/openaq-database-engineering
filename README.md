# Projet 3A — POK 2  
## **Comparaison SQL vs NoSQL à partir des données OpenAQ**

---

## **Objectif du projet**

L’objectif du projet est de comprendre quand et pourquoi utiliser une base SQL ou NoSQL, à partir d’un même domaine métier (les mesures environnementales OpenAQ)mais avec des cas d’usage différents.

L’idée clé est de montrer que forcer une technologie (SQL ou NoSQL) sur un mauvais cas d’usage peut être contreproductif.

Ce projet compare deux architectures :

- **PostgreSQL (SQL, relationnel)**
- **MongoDB (NoSQL, orienté document)**

---

## **La base de données**
Le projet s’appuie sur l’API **OpenAQ**, qui fournit des mesures de pollution atmosphérique horodatées.
[Documentation OpenAQ](https://docs.openaq.org/examples/examples)

Dans le pipeline d’ingestion, on ne conserve qu’un sous-ensemble des données afin d’avoir un jeu cohérent et comparable entre SQL et NoSQL :

- Uniquement les capteurs dont le champ `country = "FR"`,  
 *Attention : dans l’API OpenAQ, ce champ correspond au pays de l’opérateur du réseau, pas nécessairement au pays géographique du capteur. Certaines stations peuvent donc être hors de France tout en ayant `FR` comme code.*
- Uniquement le polluant `PM10`, afin de comparer des agrégations homogènes.

Les données récupérées incluent notamment :
- identifiant de la station,
- ville / pays,
- coordonnées géographiques,
- horodatage des mesures,
- valeur du PM10.


À partir des mêmes données brutes OpenAQ, on construit deux datasets différents :

#### Dataset orienté SQL (PostgreSQL) : structuré et normalisé
On transforme alors les données en un **modèle relationnel** avec plusieurs tables :

- `location` (stations)
- `sensor`
- `measurement`

Ce dataset est optimisé pour :
- des analyses historiques,
- des requêtes temporelles,
- des jointures complexes.


#### Dataset orienté NoSQL (MongoDB) — orienté document
On remodele les mêmes données sous forme **d’un document par station**, contenant :
- les métadonnées de la station,
- toutes ses mesures PM10 dans un tableau imbriqué.


Ce dataset est optimisé pour :
- une ingestion rapide,
- des lectures simples par station ou zone géographique.


## **Structure du projet**
Le projet est organisé en quatre modules indépendants, correspondant à deux technologies (Postgres / Mongo) et deux cas d’usage (SQL-optimisé / NoSQL-optimisé) :

openaq_database_engineering/
|
├──sql_optimized/
|  │
|  ├── postgres/
|  │ ├── ingestion/ # Pipeline Python d’ingestion vers PostgreSQL
|  │ ├── orm_hibernate/ # ORM Java (Hibernate / JPA)
|  │ └── visualization/ # Graphiques Python simples
|  │
|  └── mongodb/
|    ├── ingestion/ # Pipeline Python d’ingestion vers MongoDB
|    └── orm_mongo_engine/ # Requêtes analytiques avec MongoEngine
|
|
├──nosql_optimized/
|  │
|  ├── postgres/
|  │ ├── ingestion/ # Pipeline Python d’ingestion vers PostgreSQL
|  │ └── orm_hibernate/ # ORM Java (Hibernate / JPA)
|  │
|  └── mongodb/
|    ├── ingestion/ # Pipeline Python d’ingestion vers MongoDB
|    ├── orm_mongo_engine/ # Requêtes analytiques avec MongoEngine
|    └── visualization/ # Graphiques Python simples

---

## **Lancer le projet**

### 1. Cloner le repository 
```bash
git clone https://github.com/naisatlan/openaq-database-engineering.git
```

### 2. Créer les containers Docker
Il y a 4 bases de données différentes à créer (2 bases PostgresSQL et 2 bases MongoDB). Pour ce faire, on se place dans le dossir ingestion et on utilise le docker-compose.yml.

Par exemple :
```bash
cd openaq_database_engineering/sql_optimized/postgres/ingestion
docker compose up -d
```

### 3. Créer le schéma (pour Postgres)
Dans le cas d'une base de données PostgreSQL, il faut créer le schéma : 
```bash
docker exec -i openaq-postgres psql -U openaq -d openaq < database/schema.sql
```

### 4. Créer un environnement virtuel et installer les dépendances 
Pour les projets Python (tout sauf ORM Hibernate), il faut créer un venv et installer les dépendances : 
```bash
pip install -r requirements.txt
```

### 5. Lancer l'ingestion
Pour lancer l'ingestion, il faut exécuter le main du module ingestion de l'un des 4 cas. Par exemple : 
```bash
cd openaq_database_engineering/sql_optimized/
python -m postgres.ingestion.main
```

### 6. Lancer l'ORM 
Dans le cas d'un ORM Hibernate (sql_optimized/postgres et nosql_optimized/postgres) : 
```bash
cd openaq_database_engineering/sql_optimized/orm_hibernate
./gradlew clean build
./gradlew run
```

Dans le cas d'un ORM Mongo Engine (sql_optimized/mongodb et nosql_optimized/mongodb) : 
```bash
cd openaq_database_engineering/sql_optimized/
python -m mongodb.orm_mongo_engine.main
```

### 7. Lancer la visualisation 
```bash
cd openaq_database_engineering/sql_optimized/
python -m postgres.visualization.plots
```

## **Lancer les tests**

### 1. Lancer les tests Python
Par exemple : 
```bash
cd openaq_database_engineering/sql_optimized/
pytest
```

### 2. Lancer les tests sur l'ORM
```bash
cd openaq_database_engineering/sql_optimized/postgres/orm_hibernate
./gradlew test
```
