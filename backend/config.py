import os

def get_database_uri():
    return os.getenv('DATABASE_URL', 'postgresql://localhost/rentownosc_db')
