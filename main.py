from file_io import load_students, load_companies
from match import match, valid_match

def main():
    # students = {
    #     'ConnollyRachel': {'first': 'Rachel', 'last': 'Connolly', 'gender': ['Female'],
    #                  'cuny': 'Queens College', 'year': 1,
    #                  'cs_experience': 'Beginner', 'interests': [],
    #                  'ranked_companies': ['Company A', 'Company B', 'Company C'],
    #                  'matched_company': None}
    # }

    app_file = 'data/student_applications.csv'
    enrollment_file = 'data/student_enrollment.csv'
    student_pref_file = 'data/student_pref.csv'
    students = load_students(app_file, enrollment_file, student_pref_file)

    # companies = {
    #     'Company A': {'prefer': ['12345678'],'exclude': [],
    #                   'num_students': 5, 'team': [], 'sponsored': True, 'f1_j1': True},
    #     'Company B': {'prefer': [],'exclude': [],
    #                   'num_students': 5, 'team': [], 'sponsored': False, 'f1_j1': False},
    #     'Company C': {'prefer': [],'exclude': [],
    #                   'num_students': 5, 'team': [], 'sponsored': False, 'f1_j1': False}
    # }

    company_info_file = 'data/company_info.csv'
    company_pref_file = 'data/company_pref.csv'
    companies = load_companies(company_info_file, company_pref_file)

    # TODO: Validate files

    match_counter = 0
    while not valid_match(students, companies) and match_counter < 1000:
        students, companies = match(students, companies)
        match_counter += 1

    if match_counter == 1000:
        unmatched_students = [name for name in students.keys() if students[name]['matched_company'] == None]
        with open('unmatched.csv', 'w') as f:
            f.write('Last, First, Emplid, CUNY, Year, Gender, Format, Student Pref\n')
            for name in unmatched_students:
                f.write(f"{students[name]['last']}, {students[name]['first']}, {students[name]['EMPLID']},{students[name]['cuny']},{students[name]['year']},{students[name]['gender']},{students[name]['sformat']},{students[name]['ranked_companies']}\n")

    with open('matches.csv', 'w') as f:
        f.write('Last, First, Emplid, Team, CUNY, Year, Gender, Format, Student Pref\n')
        for name in students:
            if students[name]['matched_company']:
                f.write(f"{students[name]['last']}, {students[name]['first']},{students[name]['EMPLID']},{students[name]['matched_company']},{students[name]['cuny']},{students[name]['year']},{students[name]['gender']},{students[name]['sformat']},{students[name]['ranked_companies']}\n")
    return

if __name__ == "__main__":
    main()
