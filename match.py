from typing import Tuple
from random import shuffle
import pandas as pd
import numpy as np

def is_eligible(new_student: dict, company: str, companies: dict) -> bool:
    if ('No' in new_student['govtid'] and companies[company]['sponsored'] != True):
        return False
    if 'No' in new_student['f1j1'] and companies[company]['f1_j1'] != 'Yes':
        return False
    if new_student['sformat']=='Virtual' and companies[company]['format'] != 'Virtual':
        return False
    return True

def is_good_fit(new_student: dict, team: list , students: dict , total: int) -> bool:
    """TO DO"""
    #if np.isnan(new_student['gender']):
    #    print(new_student)

    #OCT 2021 - Attempting to change best fit rules to be ratios for teams that accept more than 5 Students
    if 'Male' in new_student['gender']:
        count = 0
        for name in team:
            if 'Male' in students[name]['gender']:
                count +=1
        if count > 0:
            #print(count, total, count/total)
            if count/total > 0.4:
                return False

    if [students[name]['cuny'] for name in team].count(new_student['cuny']) !=0:
        if [students[name]['cuny'] for name in team].count(new_student['cuny'])/total > 0.6:
            #print([students[name]['cuny'] for name in team].count(new_student['cuny']),total,[students[name]['cuny'] for name in team].count(new_student['cuny'])/total)
            return False

    if [students[name]['cuny'] for name in team].count(new_student['cuny']) ==0:
        return True

    if [students[name]['year'] for name in team].count(new_student['year']) != 0:
        if [students[name]['year'] for name in team].count(new_student['year'])/total > 0.8:
            #print([students[name]['year'] for name in team].count(new_student['year']),total,[students[name]['year'] for name in team].count(new_student['year'])/total)
            return False

    """"
    if 'Male' in new_student['gender'] and 'Male' in [students[name]['gender'] for name in team]:
        return False

    if [students[name]['cuny'] for name in team].count(new_student['cuny']) == 3:
        return False

    if [students[name]['year'] for name in team].count(new_student['year']) == 3:
        return False
    """


    # if [students[name]['cs_experience'] for name in team].count(new_student['cs_experience']) == 3:
    #     return False

    return True

def match_mutual(students: dict, companies: dict) -> Tuple[dict, dict]:
    """Match based on student rankings and company preferences"""
    #turning students.keys() into a list to squash dict obj not iterable bug
    all_students = list(students.keys())
    shuffle(all_students)
    for name in all_students:
        student = students[name]
        for company_name in student['ranked_companies']:
            company = companies[company_name]
            total = int(company['num_students'])
            #if len(company['team']) < int(company['num_students']) and name in company['prefer'] and is_good_fit(student, company['team'], students) and is_eligible(student,company_name,companies):
            if len(company['team']) < int(company['num_students']) and name in company['prefer'] and is_good_fit(student, company['team'], students, total) and is_eligible(student,company_name,companies):
                students[name]['matched_company'] = company_name
                companies[company_name]['team'].append(name)
                break

    return students, companies

def match_student_pref(students, companies) -> Tuple[dict, dict]:
    """Match based on student rankings"""
    unmatched_students = [name for name in students.keys() if students[name]['matched_company'] == None]
    shuffle(unmatched_students)
    for name in unmatched_students:
        student = students[name]
        for company_name in student['ranked_companies']:
            company = companies[company_name]
            #testing errors below
            #print(len(company['team']), type(len(company['team'])))
            #print(int(company['num_students']), type(int(company['num_students'])))
            #print(name, company)
            #print(name not in company['exclude'], type(name not in company['exclude']))
            #print(is_good_fit(student, company['team'], students), type(is_good_fit(student, company['team'], students)))
            #conclusion: name not in company['exclude'] may throw an error if exclude is left blank
            #set blank excludes or prefers to random letter like x to get around this

            total = int(company['num_students'])
            if len(company['team']) < int(company['num_students']) and name not in company['exclude'] and is_good_fit(student, company['team'], students, total) and is_eligible(student,company_name,companies):
                students[name]['matched_company'] = company_name
                #print('!!!!!!!',students[name],[company_name])
                companies[company_name]['team'].append(name)
                break
    return students, companies

def match_team_fit(students: dict, companies: dict) -> Tuple[dict, dict]:
    """Match based on team fit"""
    unmatched_students = [name for name in students.keys() if students[name]['matched_company'] == None]
    shuffle(unmatched_students)
    for name in unmatched_students:
        student = students[name]
        #print(companies)
        for company in companies:
            #print("test",companies[company]['team'])
            #print(companies[company]['num_students'], type(companies[company]['num_students']))
            #old code, couldn't index using company['team'] like we did before because we set company to something different here
            #if len(company['team']) < int(company['num_students']) and name not in company['exclude'] and is_good_fit(student, company['team'], students):
            #solution: properly index to find the company team length, new code line 75

            total = int(companies[company]['num_students'])
            if len(companies[company]['team']) < int(companies[company]['num_students']) and name not in companies[company]['exclude'] and is_good_fit(student, companies[company]['team'], students,total) and is_eligible(student,company,companies):
                #old code
                #students[name]['matched_company'] = company.key
                #companies[company.key]['team'].append(name)
                #new code
                students[name]['matched_company'] = company
                companies[company]['team'].append(name)
                break
    return students, companies

def match(students: dict, companies: dict) -> Tuple[dict, dict]:
    """"""
    students, companies = match_mutual(students, companies)
    students, companies = match_student_pref(students, companies)
    students, companies = match_team_fit(students, companies)
    return students, companies

def valid_match(students: dict, companies: dict) -> bool:
    """"""
    unmatched_students = [name for name in students.keys() if students[name]['matched_company'] == None]
    #print(students)
    #print(len(unmatched_students))
    if len(unmatched_students) > 0:
        return False
    return True
