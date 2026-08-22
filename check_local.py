import sqlite3
conn = sqlite3.connect('mlflow_store/mlflow.db')
experiments = conn.execute("SELECT experiment_id, name FROM experiments").fetchall()
print("Experiences locales:", experiments)