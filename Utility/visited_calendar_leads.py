import os
import pickle

'''
Clermont County Foreclosure
'''
# Specify the filename to be used for the pickled data
clermont_filename = './Data/Visited_calendar_leads/global_list_clermont.pkl'

# Initialize an empty list
clermont_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(clermont_filename):
    with open(clermont_filename, 'rb') as f:
        clermont_county_visited_leads = pickle.load(f)

def save_global_list_clermont():
    with open(clermont_filename, 'wb') as f:
        pickle.dump(clermont_county_visited_leads, f)


'''
Lee County Foreclosure
'''
# Initialize an empty list
# Specify the filename to be used for the pickled data
lee_filename = './Data/Visited_calendar_leads/global_list_lee.pkl'
lee_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(lee_filename):
    with open(lee_filename, 'rb') as f:
        lee_county_visited_leads = pickle.load(f)

def save_global_list_lee():
    with open(lee_filename, 'wb') as f:
        pickle.dump(lee_county_visited_leads, f)


'''
Franklin County Foreclosure
'''
# Initialize an empty list
# Specify the filename to be used for the pickled data
franklin_filename = './Data/Visited_calendar_leads/global_list_franklin.pkl'
franklin_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(franklin_filename):
    with open(franklin_filename, 'rb') as f:
        franklin_county_visited_leads = pickle.load(f)

def save_global_list_franklin():
    with open(franklin_filename, 'wb') as f:
        pickle.dump(franklin_county_visited_leads, f)


'''
Hamilton County Foreclosure
'''
# Initialize an empty list
# Specify the filename to be used for the pickled data
hamilton_filename = './Data/Visited_calendar_leads/global_list_hamilton.pkl'
hamilton_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(hamilton_filename):
    with open(hamilton_filename, 'rb') as f:
        hamilton_county_visited_leads = pickle.load(f)

def save_global_list_hamilton():
    with open(hamilton_filename, 'wb') as f:
        pickle.dump(hamilton_county_visited_leads, f)


'''
Pinellas County Foreclosure
'''
# Specify the filename to be used for the pickled data
pinellas_filename = './Data/Visited_calendar_leads/global_list_pinellas.pkl'

# Initialize an empty list
pinellas_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(pinellas_filename):
    with open(pinellas_filename, 'rb') as f:
        pinellas_county_visited_leads = pickle.load(f)

def save_global_list_pinellas():
    with open(pinellas_filename, 'wb') as f:
        pickle.dump(pinellas_county_visited_leads, f)


'''
Duval County Foreclosure
'''
# Specify the filename to be used for the pickled data
duval_filename = './Data/Visited_calendar_leads/global_list_duval.pkl'

# Initialize an empty list
duval_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(duval_filename):
    with open(duval_filename, 'rb') as f:
        duval_county_visited_leads = pickle.load(f)

def save_global_list_duval():
    with open(duval_filename, 'wb') as f:
        pickle.dump(duval_county_visited_leads, f)


'''
Butler County Foreclosure
'''
# Specify the filename to be used for the pickled data
butler_filename = './Data/Visited_calendar_leads/global_list_butler.pkl'

# Initialize an empty list
butler_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(butler_filename):
    with open(butler_filename, 'rb') as f:
        butler_county_visited_leads = pickle.load(f)

def save_global_list_butler():
    with open(butler_filename, 'wb') as f:
        pickle.dump(butler_county_visited_leads, f)