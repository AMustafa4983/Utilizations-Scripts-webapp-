import pandas as pd
import csv
import warnings
from .templates import ufic_beneficiary_map, ufic_asoap_map
warnings.filterwarnings("ignore")


def readFile(tpa, file, filetype):
    tpa = tpa[0] if isinstance(tpa, list) and tpa else None
    if tpa == "Nextcare":
        if filetype == 'csv':
            return pd.read_csv(file, quoting=csv.QUOTE_NONE, encoding='iso-8859-1', index_col=False, low_memory=False, on_bad_lines='skip')
        elif filetype == 'txt':
            return pd.read_csv(file, quoting=csv.QUOTE_NONE, delimiter="|", encoding='iso-8859-1', index_col=False, low_memory=False, on_bad_lines='skip')
        elif filetype == 'excel':
            return pd.read_excel(file, engine='openpyxl')
    elif tpa == "NAS":
        if filetype == 'csv':
            return pd.read_csv(file, quoting=csv.QUOTE_NONE, encoding='iso-8859-1', index_col=False, low_memory=False, on_bad_lines='skip')
        elif filetype == 'txt':
            return pd.read_csv(file, quoting=csv.QUOTE_NONE, delimiter="|", encoding='iso-8859-1', index_col=False, low_memory=False, on_bad_lines='skip')
        elif filetype == 'excel':
            return pd.read_excel(file, engine='openpyxl')
    else:
        raise ValueError("Invalid TPA system or file type specified")
    return None
        

# Beneficiary
def mapFile(dataframe, template):
    return dataframe[template]

Dependency_map_nc = {
    "Principal" : "Employee",
    "Child" : "Dependent",
    "Spouse" : "Spouse",
    "Others" : "Dependent"
}


def visa_issuance_place_cleanining_nc(value):
    if value == "HAAD":
        return "Abu Dhabi"
    elif value == "DHA":
        return "Dubai"
    else:
        return "Others"

def salary_mapping_nc(value):
    if value == 0:
        return "No Salary"
    elif value <= 4000:
        return "Low"
    elif value >= 4000:
        return "High"
    else:
        return "Unknown"

def status_mapping_nc(value):
    if value == "Voluntary Deletion":
        return "Cancelled"
    else: return "Active"
    
def dependency_mapping_nc(df, dependency_map):
    df['Dependency'] = df['Dependency'].replace(dependency_map)
    print("Dependency Column Mapped!")
    return df

def card_number_splitting_nc(value):
    return (value[:4] + "-" 
    + value[4:8] + "-" 
    + value[8:12] + "-" 
    + value[12:16])

beneficiary_types_map_nc = {'Master Contract':pd.StringDtype(), 'Contract':pd.StringDtype(), 'Policy Number':pd.StringDtype(), 'Effective Date':'datetime64[ns]',
       'Expiry Date':'datetime64[ns]', 'Start Date':'datetime64[ns]', 'Benficiary Status':pd.StringDtype(),
       'Benfeiciary Family Name':pd.StringDtype(), 'Benfeiciary Middle Name':pd.StringDtype(),
       'Benfeiciary First Name':pd.StringDtype(), 'Card Number':pd.StringDtype(), 'DOB':'datetime64[ns]', 'Gender':pd.StringDtype(), 'Nationality':pd.StringDtype(),
       'Dependency':pd.StringDtype(), 'Marital Status':pd.StringDtype(), 'Category':pd.StringDtype(), 'Product':pd.StringDtype(), 'Salary':pd.StringDtype(),
       'VisaIssuedPlace':pd.StringDtype(), 'Net Premium':'float', 'Gross Premium':'float', 'Passport Number':pd.StringDtype(),
       'National ID':pd.StringDtype(), 'UID Number':pd.StringDtype(), 'Endoresement date':'datetime64[ns]',
       'Policy type':pd.StringDtype()}


def NC_Bene_Mapping(df):
    df["Gross Premium"] = df["Gross Premium Without Taxes"] - df["Fees"]
    df['Licensing Authority'] = df['Licensing Authority'].apply(visa_issuance_place_cleanining_nc)
    df = mapFile(df, ufic_beneficiary_map['NC'])
    df.columns = ufic_beneficiary_map["UFIC Format"]
    df['Salary'] = df['Salary'].apply(salary_mapping_nc)
    df['Benficiary Status'] = df['Benficiary Status'].apply(status_mapping_nc)
    df['Card Number'] = df['Card Number'].apply(card_number_splitting_nc)
    df = dependency_mapping_nc(df, Dependency_map_nc)
    df = df.astype(beneficiary_types_map_nc)

    return df


def visa_issuance_place_cleanining_nas(value):
    if value == "Health Authority Abu Dhabi":
        return "Abu Dhabi"
    elif value == "Dubai Health Authority":
        return "Dubai"
    else:
        return "Others"

Salary_map_nas = {
    "Salary less than 4,000 AED per month" : "Low",
    "Salary between 4,001 and 12,000 AED per month": "High",
    "Salary greater than 12,000 AED per month": "High",
    "No salary": "No Salary",
    "nan" : "Unknown",
    float('nan') : "Unknown"
}

Dependency_map_nas = {
    "Principal" : "Employee",
    "Child" : "Dependent",
    "Spouse" : "Spouse",
    "Others" : "Dependent"
}


def salary_mapping_nas(df, salary_map):
    df['Salary'] = df['Salary'].replace(salary_map)
    print("Salary Column Mapped!")
    
    return df

def dependency_mapping_nas(df, dependency_map):
    df['Dependency'] = df['Dependency'].replace(dependency_map)
    print("Dependency Column Mapped!")

    return df

def MemberExpiryDate_nas(df):
    date = []
    for i in df.values:
        if pd.isna(i[85]):
            date.append(i[11])
        else:
            date.append(i[85])
    return date


def endodate_mapping_nas(df):
    endodate = []
    for row in df.values:
        if pd.isna(row[85]):
            endodate.append(row[82])
        else:
            endodate.append(row[85])

    return endodate


def NAS_Bene_Mapping(df):
    df['Reporting Authority'] = df['Reporting Authority'].apply(visa_issuance_place_cleanining_nas)
    df["Endoresement date"] = endodate_mapping_nas(df)
    df["MemberExp.Date"] = MemberExpiryDate_nas(df)
    df = mapFile(df, ufic_beneficiary_map['NAS'])
    df.columns = ufic_beneficiary_map["UFIC Format"]
    df = salary_mapping_nas(df, Salary_map_nas)
    df = dependency_mapping_nas(df, Dependency_map_nas)
    df = df.astype(beneficiary_types_map_nc)
    return df

# ASOAP
nc_claims_status_map = {
    "Settled": "Paid",
    "Processed": "Paid",
    "Initial": "OS",
    "Authorized": "OS",
}

nc_in_out_network_map = {
    "No": "In",
    "Yes": "Out",
}

nc_fob_map = {
    "Out-Patient": "OP",
    "In-Patient": "IP",
    "Alternative Treatment": "OP",
    "Psychiatry": "OP",
    "Maternity": "OP",
    "Dental": "Dental",
    "Optical": "Optical",
}


def nc_claims_status_mapping(df, map):
    df["Claims Status"] = df["Claims Status"].replace(map)
    print("Claims Mapped!")
    return df

def nc_category_mapping(df):
    df['Category'] = df['Product'].str.extract("(CAT [a-zA-Z])", expand = True)
    return df
    
def nc_in_out_network_mapping(df, map):
    df["In-Out Network"] = df["In-Out Network"].replace(map)
    print("In-Out-Network Mapped!")
    return df

def nc_fob_mapping(df, map):
    df["FOB"] = df["FOB"].replace(map)
    print("FOB Mapped!")
    return df

def nc_provider_type_mapping(value):
    if value == "Polyclinic - Group of Doctors with lab, X-ray, treatment facilities":
        return "Clinic"
    elif value == "Hospital":
        return "Hospital"
    elif value == "Pharmacy":
        return "Pharmacy"
    else:
        return "Others"
    

def nc_dependency_mapping(df):
    df['Dependency'] = df['Dependency'].replace(Dependency_map_nc)
    print("Dependency Column Mapped!")
    return df

nc_claims_types_map = {'Master Contract':pd.StringDtype(), 'Sub Contract':pd.StringDtype(), 'Policy Number':pd.StringDtype(),
        'Policy Effective date':'datetime64[ns]', 'Policy Expiry date':'datetime64[ns]', 'FOB':pd.StringDtype(), 'Claim Date':'datetime64[ns]',
        'Claim Amount':'float', 'Approved Amount':'float', 'Curency':pd.StringDtype(), 'Provider Type':pd.StringDtype(),
        'Provider Name':pd.StringDtype(), 'Dependency':pd.StringDtype(), 'Marital Status':pd.StringDtype(), 'Gender':pd.StringDtype(), 
        'DOB':'datetime64[ns]', 'Nationality':pd.StringDtype(), 'Product':pd.StringDtype(), 
        'Claims Status':pd.StringDtype(), 'In-Out Network':pd.StringDtype(), 
        'Category':pd.StringDtype(),'Assessment':pd.StringDtype(), 
        'Card Number':pd.StringDtype(), 'PO date':'datetime64[ns]', 'Discharge Date':'datetime64[ns]', 'Invoice No.':pd.StringDtype()}

def NC_Claims_Mapping(df):
    df['Inc Amt.'] = df['BC.Share'] + df['Pure Claim Value in Loc Curr']
    df = mapFile(df, ufic_asoap_map['NC'])
    df.columns = ufic_asoap_map["UFIC Format"]
    df = nc_claims_status_mapping(df, nc_claims_status_map)
    df = nc_in_out_network_mapping(df, nc_in_out_network_map)
    df = nc_fob_mapping(df, nc_fob_map)
    df = nc_category_mapping(df)
    df['Provider Type'] = df['Provider Type'].apply(nc_provider_type_mapping)
    df = nc_dependency_mapping(df)
    df = df.astype(nc_claims_types_map)

    return df

nas_claims_status_map = {
    "Initial": "OS",
    "PO Issued": "Paid",
    "Settled": "Paid",
    "Processed": "Paid",
    "Completed": "OS",
    "Authorized": "OS",
    "Reversed": "Paid",
    "UnderProcess": "Paid",
}

nas_in_out_network_map = {
    "Network": "In",
    "Reimbursement": "Out",
}

nas_fob_map = {
    "Out-Patient": "OP",
    "In-Patient": "IP",
    "Alternative Treatment": "OP",
    "Psychiatry": "OP",
    "Maternity": "OP",
    "Dental": "Dental",
    "Optical": "Optical",
}


def nas_claims_status_mapping(df, map):
    df["Claims Status"] = df["Claims Status"].replace(map)
    print("Claims Mapped!")
    return df

def nas_in_out_network_mapping(df, map):
    df["In-Out Network"] = df["In-Out Network"].replace(map)
    print("In-Out-Network Mapped!")
    return df

def nas_fob_mapping(df, map):
    df["FOB"] = df["FOB"].replace(map)
    print("FOB Mapped!")
    return df

def nas_provider_type_mapping(value):
    if value == "Clinic":
        return "Clinic"
    elif value == "Hospital":
        return "Hospital"
    elif value == "Pharmacy":
        return "Pharmacy"
    else:
        return "Others"

def NAS_Claims_Mapping(df):
    df = mapFile(df, ufic_asoap_map['NAS'])
    df.columns = ufic_asoap_map["UFIC Format"]
    df = nas_claims_status_mapping(df, nas_claims_status_map)
    df = nas_in_out_network_mapping(df, nas_in_out_network_map)
    df = nas_fob_mapping(df, nas_fob_map)
    df['Provider Type'] = df['Provider Type'].apply(nas_provider_type_mapping)

    df = dependency_mapping_nas(df, Dependency_map_nas)

    return df

