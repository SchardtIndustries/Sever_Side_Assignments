import mysql.connector

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "student",
    "password": "StudentPass123!",
    "database": "SUPPLY_CHAIN",
}

def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Simple query: show suppliers and how many purchase orders each has
    cur.execute("""
        SELECT s.SUPNR, s.SUPNAME, COUNT(po.PONR) AS order_count
        FROM SUPPLIER s
        LEFT JOIN PURCHASE_ORDER po ON po.SUPNR = s.SUPNR
        GROUP BY s.SUPNR, s.SUPNAME
        ORDER BY order_count DESC, s.SUPNR;
    """)

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
