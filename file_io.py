import pandas as pd
import numpy as np

def load_applications(file_path: str) -> pd.DataFrame:
    """TODO
    CSV must have columns "EMPLID", "Gender", "CUNY", "Year", "CS Courses", "Govt ID", "F1/J1"
    """
    df = pd.read_csv(file_path,
                     usecols=["EMPLID", "Gender", "CUNY", "Year", "CS Courses", "Govt ID", "F1/J1", "Major", "Major - Other","S Format"],
                     skipinitialspace=True
                     #, skiprows=[1,2]
                     )
    df['Gender'] = df['Gender'].str.split(',')
    return df

def load_enrollment(file_path: str) -> pd.DataFrame:
    """TODO
    CSV must have columns "EMPLID", "Programming Languages", "Interests"
    """
    df = pd.read_csv(file_path,
                     usecols=["EMPLID", "Programming Languages", "Interests"],
                     skipinitialspace=True,
                     skiprows=[1,2])
    df['Programming Languages'] = df['Programming Languages'].str.split(',')
    df['Interests'] = df['Interests'].str.split(',')
    print("enrollment= ",len(df['EMPLID']))
    return df

def load_student_pref(file_path: str) -> pd.DataFrame:
    """TODO
    CSV must have columns "First", "Last", "EMPLID", "Preferences"
    """
    df = pd.read_csv(file_path,
                     usecols=["First", "Last", "EMPLID", "Preferences"],
                     skipinitialspace=True,
                     skiprows=[1])
    df['Preferences'] = df['Preferences'].str.split(',')
    print("pref= ",len(df["EMPLID"]))
    return df

def determine_cs_experience(num_courses: str, programming_languages: list) -> str:
    """TODO"""
    if 'None' in programming_languages or num_courses == '0':
        return 'beginner'

    if len(programming_languages) >= 5 or num_courses in ['3', '4', '5+']:
        return 'advanced'

    return 'intermediate'

def load_students(app_file, enrollment_file, pref_file) -> dict:
    app_df = load_applications(app_file)
    enrollment_df = load_enrollment(enrollment_file)
    pref_df = load_student_pref(pref_file)
    print("app= ",len(app_df['EMPLID']))
    #added code to avoid error for column types below
    pref_df['EMPLID']=pref_df['EMPLID'].astype(int)
    #app_df['EMPLID']=app_df['EMPLID'].astype(str)
    #pref_df['EMPLID']=pref_df['EMPLID'].astype(str)
    #print('!!!!!!!!!!!!!!type enroll', type(enrollment_df.loc[5,'EMPLID']))
    #print('!!!!!!!!!!!!!!type enroll', type(app_df.loc[5,'EMPLID']))
    #print('!!!!!!!!!!!!!!type enroll', type(pref_df.loc[5,'EMPLID']))

    #testing to find out why match pool is smaller than students enrolled
    #old code
    #combined_df = pref_df.merge(enrollment_df,on='EMPLID').merge(app_df,on='EMPLID')
    #new newcode
    combined_df = pref_df.merge(enrollment_df,on='EMPLID')
    print(len(combined_df),"enroll + pref")

    combined_df = combined_df.merge(app_df,on='EMPLID')
    combined_df.to_csv('combineds.csv')
    print(len(combined_df),"enroll + pref + app")
    #solution: if emplids are not the same across datasets, match pool will shrink
    # if len(pref_df) != len(combined_df):
    #     raise Exception

    combined_df.insert(0, 'LastFirst', combined_df.Last.str.title() + combined_df.First.str.title())
    #new line to deal with set_index must be unique Error
    combined_df = combined_df.drop_duplicates(subset=['LastFirst'])
    #combined_df = combined_df.reset_index(drop='true')
    combined_df = combined_df.set_index('LastFirst')

    print('!!!!!!!!!!!!!!!!!! combined df',len(combined_df))
    #print('!!!!!!!!!!!!!!!!!!after alts',len(combined_df))
    # combined_df'cs_experience'] = determine_cs_experience(combined_df['CS Courses'], combined_df['Programming Languages'])
    combined_df['matched_company'] = None
    combined_df.drop(columns=['CS Courses', 'Programming Languages'], inplace=True)
    combined_df.rename(columns={'First': 'first',
                                'Last': 'last',
                                'Gender': 'gender',
                                'Year': 'year',
                                'CUNY': 'cuny',
                                "Govt ID":'govtid',
                                "F1/J1":'f1j1',
                                'Interests': 'interests',
                                'Preferences': 'ranked_companies',
                                'Major':'major',
                                'Major - Other' : 'major other',
                                'S Format':'sformat'}, inplace=True)

    return combined_df.to_dict(orient='index')

def load_company_info(file_path: str) -> pd.DataFrame:
    """
    CSV must have columns "Organization", "Number of Students", "Sponsored", "F1/J1"
    """
    df = pd.read_csv(file_path,
                     usecols=["Organization", "Number of Students", "Sponsored", "F1/J1", "Format"],
                     skipinitialspace=True)
    df.rename(columns={'Number of Students': 'num_students',
                       'Sponsored': 'sponsored',
                       'F1/J1': 'f1_j1',
                       'Format':'format'}, inplace=True)
    return df

def load_company_pref(file_path: str) -> pd.DataFrame:
    """
    CSV must have columns "Organization", "Prefer", "Exclude"
    """
    df = pd.read_csv(file_path,
                     usecols=["Organization", "Prefer", "Exclude"],
                     skipinitialspace=True,
                     skiprows=[1,2])
    df.Prefer = df.Prefer.str.title()
    df.Prefer = df.Prefer.str.replace(', ', '')
    df.Prefer = df.Prefer.str.split(' / ')

    df.Exclude = df.Exclude.str.title()
    df.Exclude = df.Exclude.str.replace(', ', '')
    df.Exclude = df.Exclude.str.split(' / ')

    df.rename(columns={'Prefer': 'prefer',
                       'Exclude': 'exclude'}, inplace=True)
    return df

def load_companies(info_file, pref_file) -> dict:
    info_df = load_company_info(info_file)
    pref_df = load_company_pref(pref_file)
    combined_df = pref_df.merge(info_df, on='Organization')
    combined_df['team'] = np.empty((len(combined_df), 0)).tolist()
    combined_df = combined_df.set_index('Organization')
    #print(combined_df.index.to_list)
    return combined_df.to_dict(orient='index')
