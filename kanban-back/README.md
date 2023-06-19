# Kanban (back-end)

Pour des besoins internes, votre responsable vous demande de développer une petite application de gestion de tâches.

Application qui prendra la forme d'un kanban.

## Contexte du projet

Pour ses besoins en gestion de projet, votre responsable vous demande de développer un Kanban afin de gérer les tâches internes de votre équipe de développement.

Pour exprimer son besoin en terme d'UI/UX, votre responsable vous a transmis un [wireframe](https://www.figma.com/file/sOnV2kpnBoVatB89DCnoo8/WF-kanban-interface?type=design&node-id=0-1).

Vous êtes libre d'y apporter des améliorations.

Les fonctionnalités à mettre en place sont les suivantes :

- Colonnes
  - Ajouter une colonne
  - Modifier le titre d'une colonne
  - Modifier la position d'une colonne
- Tâches
  - Ajouter une tâche
  - Modifier le titre d'une tâche
  - Modifier la position d'une tâche

Outre les besoins fonctionnels, votre responsable aimerait que votre travail puisse facilement être repris en main par un autre développeur.

En terme de technologie, rien n'est imposé.

La librairie [jKanban](https://github.com/riktar/jkanban) a cependant été conseillée.

## Installation

- Install a virtual environment
  
  ```powershell
  <Python command> -m venv .env
  ```

- Activate the virtual environment
  
  - Windows
    
    ```powershell
    .env\Scripts\activate
    ```
  
  - Linux
    
    ```powershell
    source .env/bin/activate
    ```

- Install packages
  
  ```powershell
  pip install -r requirements.txt
  ```

- Hide the key to the castle
  
  - Create the safe
    
    Inside `project` folder, create a file called `.env`.
  
  - Generate the key
    
    We gonna generate the key through the Django shell interface.
    
    To launch the shell interface, run the following command in the terminal of your Django project :
    
    ```powershell
    <Python command> manage.py shell
    ```
    
    - Import the key generator function
      
      Run the following command and hit `Enter` :
      
      ```python
      from django.core.management.utils import get_random_secret_key
      ```
    
    - Generate a random key
      
      On the next line we can now use the function to generate the secret key.
      
      ```python
      print(get_random_secret_key())
      ```
    
    - Hide the key
      
      Copy the generated key and exit the shell interface using the following command :
      
      ```python
      exit()
      ```
      
      In the `.env` file, declare a `SECRET_KEY` variable as follows :
      
      ```python
      SECRET_KEY=<generated key>
      ```
      
      *The castle is well-protected now. :)*

- Setting up the database
  
  - Install the PostgreSQL database connection package
    
    - Windows
      
      ```powershell
      pip install psycopg2
      ```
    
    - Linux
      
      ```powershell
      pip install psycopg2-binary
      ```
  
  - Create the database through pgAdmin
  
  - Update `project/settings.py`
    
    ```python
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ.get("DB_NAME"),
            "USER": os.environ.get("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASSWORD"),
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }
    ```
  
  - Update `project/.env`
    
    ```python
    DB_NAME=<database name>
    DB_USER=<database user>
    DB_PASSWORD=<database password>
    ```

- Make the first migrations
  
  ```powershell
  <Python command> manage.py makemigrations
  <Python command> manage.py migrate
  ```

- Populate database
  
  ```powershell
  <Python command> manage.py init_local_dev
  ```
  
  When populating the database, a superuser is created.
  
  Superuser credentials :
  
  - Username : admin
  
  - Password : admin

## API REST

| URI                           | Authorization | Method | Data                                                         | Description                                     |
| ----------------------------- | ------------- | ------ | ------------------------------------------------------------ | ----------------------------------------------- |
| /api/colonnes/                | No Auth       | GET    | None                                                         | Liste des colonnes et de leurs tâches associées |
| /api/colonnes/                | No Auth       | POST   | titre_colonne: `string`, position_colonne: `number`          | Ajouter une colonne                             |
| /api/taches/                  | No Auth       | POST   | titre_tache: `string`, position_tache: `number`, colonne: `number` | Ajouter une tâche                               |
| /api/colonnes/{{id_colonne}}/ | No Auth       | PATCH  | titre_colonne: `string`                                      | Modifier le titre d'une colonne                 |
| /api/taches/{{id_tache}}/     | No Auth       | PATCH  | titre_tache: `string`                                        | Modifier le titre d'une tâche                   |
| /api/colonne/move/            | No Auth       | PATCH  | id_colonne: `number`, position_colonne: `number`             | Modifier la position d'une colonne              |
| /api/tache/move/              | No Auth       | PATCH  | id_tache: `number`, colonne: `number`, position_tache: `number` | Modifier la position d'une tâche                |

## Run server

``` powershell
<Python command> manage.py runserver
```

