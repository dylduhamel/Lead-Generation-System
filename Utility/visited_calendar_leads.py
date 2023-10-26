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


"""
Broward County Foreclosure
"""
# Specify the filename to be used for the pickled data
broward_foreclosure_filename = "./Data/Visited_calendar_leads/global_list_broward_foreclosure.pkl"

# Initialize an empty list
broward_foreclosure_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(broward_foreclosure_filename):
    with open(broward_foreclosure_filename, "rb") as f:
        broward_foreclosure_county_visited_leads = pickle.load(f)


def save_global_list_broward_foreclosure():
    with open(broward_foreclosure_filename, "wb") as f:
        pickle.dump(broward_foreclosure_county_visited_leads, f)

        
"""
Orange County Foreclosure
"""
# Specify the filename to be used for the pickled data
orange_foreclosure_filename = "./Data/Visited_calendar_leads/global_list_orange_foreclosure.pkl"

# Initialize an empty list
orange_foreclosure_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(orange_foreclosure_filename):
    with open(orange_foreclosure_filename, "rb") as f:
        orange_foreclosure_county_visited_leads = pickle.load(f)


def save_global_list_orange_foreclosure():
    with open(orange_foreclosure_filename, "wb") as f:
        pickle.dump(orange_foreclosure_county_visited_leads, f)


"""
Miami Dade Foreclosure
"""
# Specify the filename to be used for the pickled data
miami_dade_foreclosure_filename = "./Data/Visited_calendar_leads/global_list_miami_dade_foreclosure.pkl"

# Initialize an empty list
miami_dade_foreclosure_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(miami_dade_foreclosure_filename):
    with open(miami_dade_foreclosure_filename, "rb") as f:
        miami_dade_foreclosure_visited_leads = pickle.load(f)


def save_global_list_miami_dade_foreclosure():
    with open(miami_dade_foreclosure_filename, "wb") as f:
        pickle.dump(miami_dade_foreclosure_visited_leads, f)


"""
Polk County taxdeed
"""
# Specify the filename to be used for the pickled data
polk_taxdeed_filename = "./Data/Visited_calendar_leads/global_list_polk_taxdeed.pkl"

# Initialize an empty list
polk_taxdeed_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(polk_taxdeed_filename):
    with open(polk_taxdeed_filename, "rb") as f:
        polk_taxdeed_county_visited_leads = pickle.load(f)


def save_global_list_polk_taxdeed():
    with open(polk_taxdeed_filename, "wb") as f:
        pickle.dump(polk_taxdeed_county_visited_leads, f)


"""
Lee County taxdeed
"""
# Specify the filename to be used for the pickled data
lee_taxdeed_filename = "./Data/Visited_calendar_leads/global_list_lee_taxdeed.pkl"

# Initialize an empty list
lee_taxdeed_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(lee_taxdeed_filename):
    with open(lee_taxdeed_filename, "rb") as f:
        lee_taxdeed_county_visited_leads = pickle.load(f)


def save_global_list_lee_taxdeed():
    with open(lee_taxdeed_filename, "wb") as f:
        pickle.dump(lee_taxdeed_county_visited_leads, f)


"""
Duval County taxdeed
"""
# Specify the filename to be used for the pickled data
duval_taxdeed_filename = "./Data/Visited_calendar_leads/global_list_duval_taxdeed.pkl"

# Initialize an empty list
duval_taxdeed_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(duval_taxdeed_filename):
    with open(duval_taxdeed_filename, "rb") as f:
        duval_taxdeed_county_visited_leads = pickle.load(f)


def save_global_list_duval_taxdeed():
    with open(duval_taxdeed_filename, "wb") as f:
        pickle.dump(duval_taxdeed_county_visited_leads, f)


"""
Cuyahoga County Foreclosure
"""
# Initialize an empty list
# Specify the filename to be used for the pickled data
cuyahoga_filename = "./Data/Visited_calendar_leads/global_list_cuyahoga.pkl"
cuyahoga_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(cuyahoga_filename):
    with open(cuyahoga_filename, "rb") as f:
        cuyahoga_county_visited_leads = pickle.load(f)


def save_global_list_cuyahoga():
    with open(cuyahoga_filename, "wb") as f:
        pickle.dump(cuyahoga_county_visited_leads, f)


"""
Volusia County taxdeed
"""
# Specify the filename to be used for the pickled data
volusia_taxdeed_filename = "./Data/Visited_calendar_leads/global_list_volusia_taxdeed.pkl"

# Initialize an empty list
volusia_taxdeed_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(volusia_taxdeed_filename):
    with open(volusia_taxdeed_filename, "rb") as f:
        volusia_taxdeed_county_visited_leads = pickle.load(f)


def save_global_list_volusia_taxdeed():
    with open(volusia_taxdeed_filename, "wb") as f:
        pickle.dump(volusia_taxdeed_county_visited_leads, f)


"""
Palm Beach County Foreclosure
"""
# Specify the filename to be used for the pickled data
palm_beach_filename = "./Data/Visited_calendar_leads/global_list_palm_beach.pkl"

# Initialize an empty list
palm_beach_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(palm_beach_filename):
    with open(palm_beach_filename, "rb") as f:
        palm_beach_visited_leads = pickle.load(f)


def save_global_list_palm_beach():
    with open(palm_beach_filename, "wb") as f:
        pickle.dump(palm_beach_visited_leads, f)


"""
Hillsborough County Foreclosure
"""
# Initialize an empty list
# Specify the filename to be used for the pickled data
hillsborugh_filename = "./Data/Visited_calendar_leads/global_list_hillsborugh.pkl"
hillsborugh_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(hillsborugh_filename):
    with open(hillsborugh_filename, "rb") as f:
        hillsborugh_county_visited_leads = pickle.load(f)


def save_global_list_hillsborugh():
    with open(hillsborugh_filename, "wb") as f:
        pickle.dump(hillsborugh_county_visited_leads, f)



"""
Polk County foreclosure
"""
# Specify the filename to be used for the pickled data
polk_foreclosure_filename = "./Data/Visited_calendar_leads/global_list_polk_foreclosure.pkl"

# Initialize an empty list
polk_foreclosure_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(polk_foreclosure_filename):
    with open(polk_foreclosure_filename, "rb") as f:
        polk_foreclosure_visited_leads = pickle.load(f)


def save_global_list_polk_foreclosure():
    with open(polk_foreclosure_filename, "wb") as f:
        pickle.dump(polk_foreclosure_visited_leads, f)


"""
Palm Beach Taxdeed
"""
# Specify the filename to be used for the pickled data
palm_beach_taxdeed_filename = "./Data/Visited_calendar_leads/global_list_palm_beach_taxdeed.pkl"

# Initialize an empty list
palm_beach_taxdeed_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(palm_beach_taxdeed_filename):
    with open(palm_beach_taxdeed_filename, "rb") as f:
        palm_beach_taxdeed_visited_leads = pickle.load(f)


def save_global_list_palm_beach_taxdeed():
    with open(palm_beach_taxdeed_filename, "wb") as f:
        pickle.dump(palm_beach_taxdeed_visited_leads, f)


"""
Summit County Foreclosure
"""
# Initialize an empty list
# Specify the filename to be used for the pickled data
summit_filename = "./Data/Visited_calendar_leads/global_list_summit.pkl"
summit_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(summit_filename):
    with open(summit_filename, "rb") as f:
        summit_county_visited_leads = pickle.load(f)


def save_global_list_summit():
    with open(summit_filename, "wb") as f:
        pickle.dump(summit_county_visited_leads, f)


"""
Montgomery County Foreclosure
"""
# Initialize an empty list
# Specify the filename to be used for the pickled data
montgomery_filename = "./Data/Visited_calendar_leads/global_list_montgomery.pkl"
montgomery_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(montgomery_filename):
    with open(montgomery_filename, "rb") as f:
        montgomery_county_visited_leads = pickle.load(f)


def save_global_list_montgomery():
    with open(montgomery_filename, "wb") as f:
        pickle.dump(montgomery_county_visited_leads, f)


"""
Mahoning County Foreclosure
"""
# Initialize an empty list
# Specify the filename to be used for the pickled data
mahoning_filename = "./Data/Visited_calendar_leads/global_list_mahoning.pkl"
mahoning_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(mahoning_filename):
    with open(mahoning_filename, "rb") as f:
        mahoning_county_visited_leads = pickle.load(f)


def save_global_list_mahoning():
    with open(mahoning_filename, "wb") as f:
        pickle.dump(mahoning_county_visited_leads, f)


"""
Lucas County Foreclosure
"""
# Initialize an empty list
# Specify the filename to be used for the pickled data
lucas_filename = "./Data/Visited_calendar_leads/global_list_lucas.pkl"
lucas_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(lucas_filename):
    with open(lucas_filename, "rb") as f:
        lucas_county_visited_leads = pickle.load(f)


def save_global_list_lucas():
    with open(lucas_filename, "wb") as f:
        pickle.dump(lucas_county_visited_leads, f)


"""
Lorain County Foreclosure
"""
# Initialize an empty list
# Specify the filename to be used for the pickled data
lorain_filename = "./Data/Visited_calendar_leads/global_list_lorain.pkl"
lorain_county_visited_leads = []

# If the file exists (i.e., if the program has been run before), load the data from it
if os.path.exists(lorain_filename):
    with open(lorain_filename, "rb") as f:
        lorain_county_visited_leads = pickle.load(f)


def save_global_list_lorain():
    with open(lorain_filename, "wb") as f:
        pickle.dump(lorain_county_visited_leads, f)