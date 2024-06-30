import sys

sys.path.append('..')

from utils import json_to_database, skiptrace_leads

if __name__ == "__main__":
    skiptrace_leads()
    json_to_database()