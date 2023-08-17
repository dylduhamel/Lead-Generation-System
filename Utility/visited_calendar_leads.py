import os
import pickle

"""
Clermont County Foreclosure
"""
# Specify the filename to be used for the pickled data
clermont_filename = "./Data/Visited_calendar_leads/global_list_clermont.pkl"

# Initialize an empty list
clermont_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(clermont_filename):
    with open(clermont_filename, "rb") as f:
        clermont_county_visited_leads = pickle.load(f)


def save_global_list_clermont():
    with open(clermont_filename, "wb") as f:
        pickle.dump(clermont_county_visited_leads, f)


"""
Lee County Foreclosure
"""
# Initialize an empty list
# Specify the filename to be used for the pickled data
lee_filename = "./Data/Visited_calendar_leads/global_list_lee.pkl"
lee_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(lee_filename):
    with open(lee_filename, "rb") as f:
        lee_county_visited_leads = pickle.load(f)


def save_global_list_lee():
    with open(lee_filename, "wb") as f:
        pickle.dump(lee_county_visited_leads, f)


"""
Franklin County Foreclosure
"""
# Initialize an empty list
# Specify the filename to be used for the pickled data
franklin_filename = "./Data/Visited_calendar_leads/global_list_franklin.pkl"
franklin_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(franklin_filename):
    with open(franklin_filename, "rb") as f:
        franklin_county_visited_leads = pickle.load(f)


def save_global_list_franklin():
    with open(franklin_filename, "wb") as f:
        pickle.dump(franklin_county_visited_leads, f)


"""
Hamilton County Foreclosure
"""
# Initialize an empty list
# Specify the filename to be used for the pickled data
hamilton_filename = "./Data/Visited_calendar_leads/global_list_hamilton.pkl"
hamilton_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(hamilton_filename):
    with open(hamilton_filename, "rb") as f:
        hamilton_county_visited_leads = pickle.load(f)


def save_global_list_hamilton():
    with open(hamilton_filename, "wb") as f:
        pickle.dump(hamilton_county_visited_leads, f)


"""
Pinellas County Foreclosure
"""
# Specify the filename to be used for the pickled data
pinellas_filename = "./Data/Visited_calendar_leads/global_list_pinellas.pkl"

# Initialize an empty list
pinellas_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(pinellas_filename):
    with open(pinellas_filename, "rb") as f:
        pinellas_county_visited_leads = pickle.load(f)


def save_global_list_pinellas():
    with open(pinellas_filename, "wb") as f:
        pickle.dump(pinellas_county_visited_leads, f)


"""
Duval County Foreclosure
"""
# Specify the filename to be used for the pickled data
duval_filename = "./Data/Visited_calendar_leads/global_list_duval.pkl"

# Initialize an empty list
duval_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(duval_filename):
    with open(duval_filename, "rb") as f:
        duval_county_visited_leads = pickle.load(f)


def save_global_list_duval():
    with open(duval_filename, "wb") as f:
        pickle.dump(duval_county_visited_leads, f)


"""
Butler County Foreclosure
"""
# Specify the filename to be used for the pickled data
butler_filename = "./Data/Visited_calendar_leads/global_list_butler.pkl"

# Initialize an empty list
butler_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(butler_filename):
    with open(butler_filename, "rb") as f:
        butler_county_visited_leads = pickle.load(f)


def save_global_list_butler():
    with open(butler_filename, "wb") as f:
        pickle.dump(butler_county_visited_leads, f)


"""
Fairfield County Foreclosure
"""
# Specify the filename to be used for the pickled data
fairfield_filename = "./Data/Visited_calendar_leads/global_list_fairfield.pkl"

# Initialize an empty list
fairfield_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(fairfield_filename):
    with open(fairfield_filename, "rb") as f:
        fairfield_county_visited_leads = pickle.load(f)


def save_global_list_fairfield():
    with open(fairfield_filename, "wb") as f:
        pickle.dump(fairfield_county_visited_leads, f)


"""
Charlotte County Foreclosure
"""
# Specify the filename to be used for the pickled data
charlotte_filename = "./Data/Visited_calendar_leads/global_list_charlotte.pkl"

# Initialize an empty list
charlotte_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(charlotte_filename):
    with open(charlotte_filename, "rb") as f:
        charlotte_county_visited_leads = pickle.load(f)


def save_global_list_charlotte():
    with open(charlotte_filename, "wb") as f:
        pickle.dump(charlotte_county_visited_leads, f)


"""
Marion County Foreclosure
"""
# Specify the filename to be used for the pickled data
marion_filename = "./Data/Visited_calendar_leads/global_list_marion.pkl"

# Initialize an empty list
marion_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(marion_filename):
    with open(marion_filename, "rb") as f:
        marion_county_visited_leads = pickle.load(f)


def save_global_list_marion():
    with open(marion_filename, "wb") as f:
        pickle.dump(marion_county_visited_leads, f)


"""
Marion County taxdeed
"""
# Specify the filename to be used for the pickled data
marion_taxdeed_filename = "./Data/Visited_calendar_leads/global_list_marion_taxdeed.pkl"

# Initialize an empty list
marion_taxdeed_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(marion_taxdeed_filename):
    with open(marion_taxdeed_filename, "rb") as f:
        marion_taxdeed_county_visited_leads = pickle.load(f)


def save_global_list_marion_taxdeed():
    with open(marion_taxdeed_filename, "wb") as f:
        pickle.dump(marion_taxdeed_county_visited_leads, f)


"""
Alachua County Foreclosure
"""
# Specify the filename to be used for the pickled data
alachua_filename = "./Data/Visited_calendar_leads/global_list_alachua.pkl"

# Initialize an empty list
alachua_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(alachua_filename):
    with open(alachua_filename, "rb") as f:
        alachua_county_visited_leads = pickle.load(f)


def save_global_list_alachua():
    with open(alachua_filename, "wb") as f:
        pickle.dump(alachua_county_visited_leads, f)


"""
St Lucie County Foreclosure
"""
# Specify the filename to be used for the pickled data
st_lucie_filename = "./Data/Visited_calendar_leads/global_list_st_lucie.pkl"

# Initialize an empty list
st_lucie_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(st_lucie_filename):
    with open(st_lucie_filename, "rb") as f:
        st_lucie_county_visited_leads = pickle.load(f)


def save_global_list_st_lucie():
    with open(st_lucie_filename, "wb") as f:
        pickle.dump(st_lucie_county_visited_leads, f)


"""
Sarasota County Foreclosure
"""
# Specify the filename to be used for the pickled data
sarasota_filename = "./Data/Visited_calendar_leads/global_list_sarasota.pkl"

# Initialize an empty list
sarasota_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(sarasota_filename):
    with open(sarasota_filename, "rb") as f:
        sarasota_county_visited_leads = pickle.load(f)


def save_global_list_sarasota():
    with open(sarasota_filename, "wb") as f:
        pickle.dump(sarasota_county_visited_leads, f)


"""
Nassau County Foreclosure
"""
# Specify the filename to be used for the pickled data
nassau_foreclosure_filename = "./Data/Visited_calendar_leads/global_list_nassau_foreclosure.pkl"

# Initialize an empty list
nassau_foreclosure_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(nassau_foreclosure_filename):
    with open(nassau_foreclosure_filename, "rb") as f:
        nassau_foreclosure_county_visited_leads = pickle.load(f)


def save_global_list_nassau_foreclosure():
    with open(nassau_foreclosure_filename, "wb") as f:
        pickle.dump(nassau_foreclosure_county_visited_leads, f)


"""
Nassau County Taxdeed
"""
# Specify the filename to be used for the pickled data
nassau_taxdeed_filename = "./Data/Visited_calendar_leads/global_list_nassau_taxdeed.pkl"

# Initialize an empty list
nassau_taxdeed_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(nassau_taxdeed_filename):
    with open(nassau_taxdeed_filename, "rb") as f:
        nassau_taxdeed_county_visited_leads = pickle.load(f)


def save_global_list_nassau_taxdeed():
    with open(nassau_taxdeed_filename, "wb") as f:
        pickle.dump(nassau_taxdeed_county_visited_leads, f)

