from django.db import models, transaction

# import app.toolbox as tb

class Colonne(models.Model):
    id_colonne = models.AutoField(primary_key=True)
    titre_colonne = models.CharField(max_length=250)
    position_colonne = models.IntegerField()

    class Meta:
        managed = True
        db_table = "colonne"

    def __str__(self):
            return f"{self.id_colonne}_{self.titre_colonne}"

    # @transaction.atomic
    # def move(self, *args, **kwargs):
    #     old_position = args[0]
    #     new_position = args[1]

    #     print("moving colonne...")
    #     tb.move_backward() if old_position > new_position else tb.move_forward()

class Tache(models.Model):
    id_tache = models.AutoField(primary_key=True)
    titre_tache = models.CharField(max_length=250)
    position_tache = models.IntegerField()
    colonne = models.ForeignKey("app.Colonne", on_delete=models.CASCADE, related_name="taches")

    class Meta:
        managed = True
        db_table = "tache"

    def __str__(self):
            return f"{self.id_tache}_{self.titre_tache}"

    # @transaction.atomic
    # def move(self):
    #     print("moving tache...")
