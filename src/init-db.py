from db.models import create_tables
from time import sleep

if __name__ == '__main__':
    create_tables()
    sleep(60)  # time for creating topics
