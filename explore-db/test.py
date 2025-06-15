import pyodbc

try:
    print(pyodbc.drivers())

    # Test direct pyodbc connection
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=127.0.0.1,1433;"
        "DATABASE=master;"
        "UID=sa;"
        "PWD=YourStrong!Passw0rd;"
        "Connection Timeout=30;"
    )

    print("Attempting pyodbc connection...")
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    result = cursor.fetchone()
    print(f"Success: {result[0]}")
    conn.close()

except Exception as e:
    print(f"pyodbc failed: {e}")
