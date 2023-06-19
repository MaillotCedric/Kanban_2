from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Colonne, Tache

ADMIN_ID = "admin"
ADMIN_PASSWORD = "admin"
COLONNES = ["To Do", "W.I.P.", "Done"]
TACHES = [
    {
        "titre": "Tâche 1",
        "colonne": "Done",
        "position": 2
    },
    {
        "titre": "Tâche 2",
        "colonne": "Done",
        "position": 1
    },
    {
        "titre": "Tâche 3",
        "colonne": "W.I.P.",
        "position": 1
    },
    {
        "titre": "Tâche 4",
        "colonne": "W.I.P.",
        "position": 2
    },
    {
        "titre": "Tâche 5",
        "colonne": "W.I.P.",
        "position": 3
    },
    {
        "titre": "Tâche 6",
        "colonne": "To Do",
        "position": 1
    },
    {
        "titre": "Tâche 7",
        "colonne": "To Do",
        "position": 2
    },
    {
        "titre": "Tâche 8",
        "colonne": "To Do",
        "position": 3
    },
    {
        "titre": "Tâche 9",
        "colonne": "To Do",
        "position": 4
    }
]

class Command(BaseCommand):
    init_start_message = "Initialisation du projet pour un environnement local"
    database_delete_message = "Suppression du jeu de données existant..."
    superuser_create_message = "Création d'un super utilisateur..."
    colonnes_create_message = "Création des colonnes..."
    taches_create_message = "Création des tâches..."
    init_end_message = "Initialisation terminée !"

    def handle(self, *args, **options):

        self.stdout.write(self.style.MIGRATE_HEADING(self.init_start_message))

        self.stdout.write(self.style.WARNING(self.database_delete_message))
        User.objects.all().delete()
        Colonne.objects.all().delete()

        self.stdout.write(self.style.MIGRATE_HEADING(self.superuser_create_message))
        User.objects.create_superuser(ADMIN_ID, "admin@example.com", ADMIN_PASSWORD)

        self.creer_colonnes()

        self.creer_taches()

        self.stdout.write(self.style.SUCCESS(self.init_end_message))

    def creer_colonnes(self):
        self.stdout.write(self.style.MIGRATE_HEADING(self.colonnes_create_message))

        for (index, colonne) in enumerate(COLONNES):
            titre_colonne = colonne
            position_colonne = index + 1

            Colonne.objects.create(titre_colonne=titre_colonne, position_colonne=position_colonne)

    def creer_taches(self):
        self.stdout.write(self.style.MIGRATE_HEADING(self.taches_create_message))

        for tache in TACHES:
            titre_tache = tache["titre"]
            colonne = Colonne.objects.get(titre_colonne=tache["colonne"])
            position_tache = tache["position"]

            Tache.objects.create(titre_tache=titre_tache, colonne=colonne, position_tache=position_tache)
