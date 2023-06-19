from app.models import Colonne, Tache

def space_move(entity, current_entity, old_position, new_position):
    entity = entity.lower()
    range_ = None
    pas = None
    entites_a_modifier = None
    colonne = None

    if old_position > new_position: # moving backward
        range_ = range(new_position, old_position)
        pas = 1
    else: # moving forward
        range_ = range(old_position + 1, new_position + 1)
        pas = -1

    if entity == "tache":
        colonne = current_entity.colonne

    entites_a_modifier = Colonne.objects.filter(position_colonne__in=range_) if entity == "colonne" else colonne.taches.filter(position_tache__in=range_)

    for entite in entites_a_modifier:
        if entity == "colonne":
            entite.position_colonne = entite.position_colonne + pas
        else:
            entite.position_tache = entite.position_tache + pas

        entite.save()

    if entity == "colonne":
        current_entity.position_colonne = new_position
    else:
        current_entity.position_tache = new_position

    current_entity.save()

def space_time_move(tache, old_column, new_colonne, old_tache_position, new_tache_position):
    taches_a_modifier_in_new_column = new_colonne.taches.filter(position_tache__gte = new_tache_position)
    taches_a_modifier_in_old_column = old_column.taches.filter(position_tache__gt = old_tache_position)

    for tache_a_modifier_in_new_column in taches_a_modifier_in_new_column:
        tache_a_modifier_in_new_column.position_tache = tache_a_modifier_in_new_column.position_tache + 1
        tache_a_modifier_in_new_column.save()

    tache.colonne = new_colonne
    tache.position_tache = new_tache_position
    tache.save()

    for tache_a_modifier_in_old_column in taches_a_modifier_in_old_column:
        tache_a_modifier_in_old_column.position_tache = tache_a_modifier_in_old_column.position_tache - 1
        tache_a_modifier_in_old_column.save()
