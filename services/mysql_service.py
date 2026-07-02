import os
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        port=int(os.getenv("MYSQLPORT", 3306)),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE")
    )


def invoice_exists(invoice_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM invoices
        WHERE invoice_number = %s
    """, (invoice_number,))

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count > 0


def save_invoice(invoice_number, invoice_date, invoice_period, prize_type, prize_amount):
    conn = get_connection()
    cursor = conn.cursor()

    if prize_type in ["查無此期別或尚未開獎", "查詢失敗", "尚未開獎"]:
        final_prize_amount = None
    elif prize_type == "未中獎":
        final_prize_amount = 0
    else:
        final_prize_amount = int(prize_amount)

    cursor.execute("""
        INSERT INTO invoices
        (invoice_number, invoice_date, invoice_period, prize_type, prize_amount)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        invoice_number,
        invoice_date,
        invoice_period,
        prize_type,
        final_prize_amount
    ))

    conn.commit()
    cursor.close()
    conn.close()


def get_all_winning_numbers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            invoice_period,
            special_prize,
            grand_prize,
            first_prize1,
            first_prize2,
            first_prize3,
            sixth_prize1,
            sixth_prize2,
            sixth_prize3
        FROM winning_numbers
        ORDER BY invoice_period DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows