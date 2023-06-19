export function print_(... params) {
    console.log(... params);
};

export function sorted_columns(columns) {
    return columns.sort((a, b) => {
        return a.id_colonne - b.id_colonne
    });
}

export function sorted_columns_on_position(columns) {
    return columns.sort((a, b) => {
        return a.position_colonne - b.position_colonne
    });
}

export function sorted_taches(taches) {
    return taches.sort((a, b) => {
        return a.id_tache - b.id_tache
    });
}

export function sorted_taches_on_position(taches) {
    return taches.sort((a, b) => {
        return a.position_tache - b.position_tache
    });
}
