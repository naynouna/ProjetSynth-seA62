import sqlite3
conn = sqlite3.connect('/app/mlflow_store/mlflow.db')
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Tables:", tables)
runs = conn.execute("SELECT COUNT(*) FROM runs").fetchall()
print("Nombre de runs:", runs)
experiments = conn.execute("SELECT experiment_id, name FROM experiments").fetchall()
print("Experiences:", experiments)