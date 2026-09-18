import sqlite3


DATABASE = "parties.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


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