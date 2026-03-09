from enum import StrEnum


class Challenges(StrEnum):
    CHALLENGE_1 = "Population of naked mole rats"
    CHALLENGE_2 = "Coffin break"
    CHALLENGE_2 = "Data Miners in Mensa"


class Languages(StrEnum):
    PYTHON = "Python"
    R = "R"


db_connection_string = "postgresql://evaluser:evalpass@localhost:5432/evaldb"


def insert_row(conn, data: dict, table='submissions'):
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))

    query = f"""
        INSERT INTO {table} ({columns})
        VALUES ({placeholders})
        RETURNING id
    """

    with conn.cursor() as cur:
        cur.execute(query, tuple(data.values()))
        return cur.fetchone()[0]


def update_row(conn, row_id, data: dict, table='submissions'):
    assignments = ", ".join([f"{k} = %s" for k in data.keys()])

    query = f"""
        UPDATE {table}
        SET {assignments}
        WHERE id = %s
    """

    with conn.cursor() as cur:
        cur.execute(query, tuple(data.values()) + (row_id,))
