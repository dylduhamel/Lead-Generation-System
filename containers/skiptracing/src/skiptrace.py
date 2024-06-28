import sys
sys.path.append('..')

from utils import skiptrace_leads, json_to_database

if __name__ == "__main__":
    skiptrace_leads()
    json_to_database()