# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 22:51:33 2023

@author: micha
"""
# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# Load csv file containing scraped data from Glassdoor job postings
df = pd.read_csv("C:/Users/micha/Desktop/Coding Projects (older)/Python Projects/glassdoor.csv")


df1 = df[-df['Job Title'].str.contains('senior|sr.|sr ')] # Filter out senior level positions 


# Sample the list of qualifications from the job descriptions and build a list of relevant skills
    # go through and check that it is selecting only skills and not other text
    # clean through keywords that are not useful, (ex. writ, informa, etc.), creating unique tags and combining tage (eg. reports and reporting instead of report. organizational skills and organzied instead of organiz)
    
for i in range(len(df1)): 
    print(list(df1['Qualifications'])[i])
    print('=================\n' * 3)
    print('\n\n\n\n\n')
        
    
skills = {'sql':0, 'python':0, ' r ':0, ' r,':0, 'visualiz':0, 'communicate':0, 'javascript':0, 'programming':0,  'data management':0, 'collaborat':0,
         'relational':0, 'reports':0, 'reporting':0,  'quality check':0, 'detail':0, 'details':0, 'confidential':0, 'sas':0, 'gis':0, 'excel':0, 'tableau':0,
         'powerbi':0, 'power bi':0, 'visio ':0, 'jira':0, 'problem-solving':0, 'problem solving':0, 'manipulat':0, 'gathering':0, 'toad':0, 'knime':0, 
         'crystal':0, 'customer service':0, 'annotation':0, 'wrangl':0, 'metric':0, 'aws':0, 'imperfect':0, 'modeling':0, 
         'large-scale':0, 'big data':0, 'large data':0, 'organizational skills':0, 'organized':0}
# skills to add: reports and reporting, powerbi and power bi, large scale, big data etc. 



#-----------------------------

df1['Qualifications'].str.lower()
for skill in skills.keys():
    for qs in df1['Qualifications']:
        if skill in qs:
            skills[skill] += 1
# could loop through and do this by seeing which are close enough to each other 
skills['reports'] += skills['reporting']
del skills['reporting']
skills['power bi'] += skills['powerbi']
del skills['powerbi']
skills['large data'] += skills['big data'] + skills['large-scale']
del skills['big data']
del skills['large-scale']
skills['organizational skills'] += skills['organized']
del skills['organized']
skills['detail'] -= skills['details'] # removes instances of 'job details', 'see more details', etc. 
del skills['details']
skills['problem solving'] += skills['problem-solving']
del skills['problem-solving']

skillsSorted = {key: val for key, val in sorted(skills.items(), key = lambda x: x[1], reverse = True)}
skillsSorted

# Highest frequency skills >60 are report writing, excel, SQL
# >=30 are visualization, collaboration, communication, statistics, problem solving, tableau, attn to detail
# >=20 are python, power bi, AWS, large data sets, modeling, data management
 
print(set(df1['Company']))
from collections import Counter
companies = Counter(list(df1['Company']))
companiesSorted = {key: val for key, val in sorted(companies.items(), key = lambda x: x[1], reverse = True)}
companiesSorted # top company is insight global (5), a contracting agency. Jobs are spread across many different companies without one accounting for a large proportion  


# find all remote jobs 
# create plot that shows proportion of skills 


# Re-name some of the skillsSorted dictionary keys for better labels in plotting 

plt.pie(list(skillsSorted.values())[:10], labels = list(skillsSorted.keys())[:10], autopct = '%.0f%%')
plt.show()

df1['Location'].value_counts().plot.bar()

# -- this doesn't accurately count number of remote jobs
remoteCount = 0
for title in df1['Job Title']:
    if 'remote' in title:
        remoteCount += 1
    elif 'hybrid' in title:
        remoteCount += 1
remoteCount # 5  
# --


patternEmployerEst = re.compile("Employer est.:")
patternGlassdoorEst = re.compile("(Glassdoor est.)")

tempSalaryList = []
salaryTypeList = []
for salary in df1['Salary']:
    if patternEmployerEst.search(salary):
        #print('employer est')
        match = patternEmployerEst.search(salary)
        tempSalaryList.append(salary[match.span()[1]:])
        salaryTypeList.append('Employer Est.')
        
    elif patternGlassdoorEst.search(salary):
        #print('glassdoor est')
        match = patternGlassdoorEst.search(salary)
        tempSalaryList.append(salary[:match.span()[0]-2])
        salaryTypeList.append('Glassdoor Est.')
    else:
        print('neither type of estimate found')
        print(salary)
        tempSalaryList.append('NO SALARY INFO')
        salaryTypeList.append('NO INFO')
        
print(salaryTypeList)
df1['Salary Estimate Type'] = salaryTypeList       


rangeSalaryList = []
avgSalaryList = []
for salary in tempSalaryList:
    if salary == 'NO SALARY INFO':
        rangeSalaryList.append(None)
        avgSalaryList.append(None)
        continue  
    salary = salary.replace('$', '')
    if 'K' in salary:
        if ' - ' in salary: 
            lowerEst = int(salary.split('K')[0]) * 1000
            upperEst = int(salary.split('K')[-2].split('-')[-1]) * 1000
            
            rangeSalaryList.append((lowerEst, upperEst))
            avgSalaryList.append(np.mean([lowerEst, upperEst]))
            #print(lowerEst, upperEst)
        else:
            print('- not in salary:', salary)
            est = int(salary.split('K')[0]) * 1000
            print('salary after:', est)
            
            rangeSalaryList.append((lowerEst, upperEst))
            avgSalaryList.append(np.mean([lowerEst, upperEst]))
            
    elif 'Per Hour' in salary:
        if ' - ' in salary:
            salary = salary.replace(' Per Hour', '')
            lowerEst = int(round(float(salary.split(' - ')[0]) * 40 * 52, 0))
            upperEst = int(round(float(salary.split(' - ')[1]) * 40 * 52, 0))
            
            rangeSalaryList.append((lowerEst, upperEst))
            avgSalaryList.append(np.mean([lowerEst, upperEst]))
            #print(lowerEst, upperEst)
        else:
            print('- not in salary:', salary)
            est = int(round(float(salary.split(' Per Hour')[0]) * 40 * 52, 0))        
            print('salary after', est)
            
            rangeSalaryList.append(est)
            avgSalaryList.append(est)
           
    else:
        print('Exception', salary) # No exceptions 

df1['rangeSalary'] = rangeSalaryList        
df1['avgSalary'] = avgSalaryList
         

plt.hist(df1['avgSalary'].dropna(), color = 'blue', edgecolor = 'black')

dfAvgSalaryByLocation = df1.groupby(['Location'])
dfAvgSalaryByLocation