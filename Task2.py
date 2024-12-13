import mariadb

app = Flask(__name__)

db_config = {
    "user": "root",
    "password": "256481@dinal",
    "host": "localhost",
    "port": 3306,
    "database": "flight_game"
}

def get_airport_data(icao):

    try:
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT ident AS ICAO, name AS Name, municipality AS Location FROM airport_backup WHERE ident = %s"
        cursor.execute(query, (icao,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

@app.route('/airport/<string:icao>', methods=['GET'])
def get_airport_info(icao):

    airport = get_airport_data(icao.upper())
    if airport:
        return jsonify(airport)
    else:
        return jsonify({"error": "Airport not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
