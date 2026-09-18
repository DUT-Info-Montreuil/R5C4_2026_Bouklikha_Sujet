from flask import Flask, request, jsonify
import sqlite3

from database import get_connection, get_referentiel


app = Flask(__name__)


# ---------------------------------------------------------
# ROUTE DE TEST
# ---------------------------------------------------------

@app.route("/")
def accueil():
    return {
        "message": "API Pilotage des files de jeu",
        "version": "v1"
    }


# ---------------------------------------------------------
# REFERENTIEL
# ---------------------------------------------------------

@app.route("/api/v1/parties/referentiel", methods=["GET"])
def referentiel():
    try:
        data = get_referentiel()

        return jsonify(data), 200

    except Exception as e:
        return jsonify({
            "error": "Erreur lors de la récupération du référentiel",
            "details": str(e)
        }), 500


# ---------------------------------------------------------
# PARTIES
# ---------------------------------------------------------

@app.route("/api/v1/parties", methods=["GET"])
def get_parties():

    # -----------------------------------------------------
    # 1. RÉCUPÉRATION DES PARAMÈTRES
    # -----------------------------------------------------

    annee = request.args.get("annee")
    serveur = request.args.get("serveur")
    jeu = request.args.get("jeu")
    file = request.args.get("file")

    tri = request.args.get("tri", "date")
    ordre = request.args.get("ordre", "desc")

    # Valeurs par défaut demandées dans le sujet
    limit = request.args.get("limit", "20")
    offset = request.args.get("offset", "0")


    # -----------------------------------------------------
    # 2. VALIDATION DE LIMIT
    # -----------------------------------------------------

    try:
        limit = int(limit)
    except ValueError:
        return jsonify({
            "error": "Le paramètre limit doit être un entier."
        }), 400

    if limit <= 0:
        return jsonify({
            "error": "Le paramètre limit doit être supérieur à 0."
        }), 400


    # -----------------------------------------------------
    # 3. VALIDATION DE OFFSET
    # -----------------------------------------------------

    try:
        offset = int(offset)
    except ValueError:
        return jsonify({
            "error": "Le paramètre offset doit être un entier."
        }), 400

    if offset < 0:
        return jsonify({
            "error": "Le paramètre offset doit être supérieur ou égal à 0."
        }), 400


    # -----------------------------------------------------
    # 4. VALIDATION DU TRI
    # -----------------------------------------------------

    tris_acceptes = {
        "date": "p.debut",
        "attente": "p.attente_secondes"
    }

    if tri not in tris_acceptes:
        return jsonify({
            "error": "Paramètre tri invalide.",
            "valeurs_acceptees": list(tris_acceptes.keys())
        }), 400


    # -----------------------------------------------------
    # 5. VALIDATION DE L'ORDRE
    # -----------------------------------------------------

    ordres_acceptes = {
        "asc": "ASC",
        "desc": "DESC"
    }

    if ordre not in ordres_acceptes:
        return jsonify({
            "error": "Paramètre ordre invalide.",
            "valeurs_acceptees": list(ordres_acceptes.keys())
        }), 400


    # -----------------------------------------------------
    # 6. CONSTRUCTION DE LA REQUÊTE
    # -----------------------------------------------------

    query_from = """
        FROM parties p
        JOIN serveurs s ON p.serveur_id = s.id
        JOIN files f ON p.file_id = f.id
        JOIN jeux j ON f.jeu_id = j.id
    """

    conditions = []
    parameters = []


    # -----------------------------------------------------
    # 7. FILTRE ANNÉE
    # -----------------------------------------------------

    if annee:
        conditions.append("strftime('%Y', p.debut) = ?")
        parameters.append(annee)


    # -----------------------------------------------------
    # 8. FILTRE SERVEUR
    # -----------------------------------------------------

    if serveur:
        conditions.append("""
            (
                s.code = ?
                OR s.nom = ?
            )
        """)

        parameters.append(serveur)
        parameters.append(serveur)


    # -----------------------------------------------------
    # 9. FILTRE JEU
    # -----------------------------------------------------

    if jeu:
        conditions.append("j.nom = ?")
        parameters.append(jeu)


    # -----------------------------------------------------
    # 10. FILTRE FILE
    # -----------------------------------------------------

    if file:
        conditions.append("f.nom = ?")
        parameters.append(file)


    # -----------------------------------------------------
    # 11. WHERE
    # -----------------------------------------------------

    where = ""

    if conditions:
        where = " WHERE " + " AND ".join(conditions)


    # -----------------------------------------------------
    # 12. CALCUL DU TOTAL
    # -----------------------------------------------------

    count_query = """
        SELECT COUNT(*) AS total
    """ + query_from + where

    connection = get_connection()

    total_result = connection.execute(
        count_query,
        parameters
    ).fetchone()

    total = total_result["total"]


    # -----------------------------------------------------
    # 13. RÉCUPÉRATION DES PARTIES
    # -----------------------------------------------------

    order_by = tris_acceptes[tri]
    order_direction = ordres_acceptes[ordre]

    data_query = """
        SELECT
            p.id,
            s.code AS serveur,
            s.nom AS serveur_nom,
            j.nom AS jeu,
            f.nom AS file,
            p.debut,
            p.attente_secondes,
            p.duree_minutes
    """ + query_from + where + f"""
        ORDER BY {order_by} {order_direction}
        LIMIT ? OFFSET ?
    """

    data_parameters = parameters + [limit, offset]

    rows = connection.execute(
        data_query,
        data_parameters
    ).fetchall()

    connection.close()


    # -----------------------------------------------------
    # 14. CONVERSION EN JSON
    # -----------------------------------------------------

    data = [dict(row) for row in rows]


    # -----------------------------------------------------
    # 15. RÉPONSE
    # -----------------------------------------------------

    return jsonify({
        "data": data,
        "total": total,
        "limit": limit,
        "offset": offset
    }), 200


# ---------------------------------------------------------
# LANCEMENT DE L'API
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )