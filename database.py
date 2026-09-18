import sqlite3


DATABASE = "parties.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def get_all_parties():
    connection = get_connection()

    query = """ SELECT p.id, s.code AS serveur, s.nom AS serveur_nom, j.nom AS jeu, f.nom AS file, p.debut, p.attente_secondes, p.duree_minutes
                FROM parties p
                JOIN serveurs s ON p.serveur_id = s.id
                JOIN files f ON p.file_id = f.id
                JOIN jeux j ON f.jeu_id = j.id
                ORDER BY p.debut DESC """

    rows = connection.execute(query).fetchall()
    connection.close()

    return [dict(row) for row in rows]


def get_referentiel():
    connection = get_connection()

    serveurs = connection.execute("""
        SELECT id, code, nom, region
        FROM serveurs
        ORDER BY nom
    """).fetchall()

    jeux = connection.execute("""
        SELECT id, nom
        FROM jeux
        ORDER BY nom
    """).fetchall()

    files = connection.execute("""
        SELECT f.id, f.nom, f.jeu_id, j.nom AS jeu
        FROM files f
        JOIN jeux j ON f.jeu_id = j.id
        ORDER BY j.nom, f.nom
    """).fetchall()

    annees = connection.execute("""
        SELECT DISTINCT strftime('%Y', debut) AS annee
        FROM parties
        WHERE debut IS NOT NULL
        ORDER BY annee
    """).fetchall()

    connection.close()

    return {
        "serveurs": [dict(row) for row in serveurs],
        "jeux": [dict(row) for row in jeux],
        "files": [dict(row) for row in files],
        "annees": [row["annee"] for row in annees]
    }