import os
import pickle

'''
Clermont County Foreclosure
'''
# Specify the filename to be used for the pickled data
filename = './Utility/global_list_clermont.pkl'

# Initialize an empty list
clermont_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(filename):
    with open(filename, 'rb') as f:
        clermont_county_visited_leads = pickle.load(f)

def save_global_list_clermont():
    with open(filename, 'wb') as f:
        pickle.dump(clermont_county_visited_leads, f)

'''
Lee County Foreclosure
'''
# Initialize an empty list
# Specify the filename to be used for the pickled data
filename = './Utility/global_list_lee.pkl'
lee_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(filename):
    with open(filename, 'rb') as f:
        lee_county_visited_leads = pickle.load(f)

def save_global_list_lee():
    with open(filename, 'wb') as f:
        pickle.dump(lee_county_visited_leads, f)
