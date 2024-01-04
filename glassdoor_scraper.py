# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 00:18:00 2022

@author: micha
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}

paginationUrlList = ['https://www.glassdoor.com/Job/seattle-data-analyst-jobs-SRCH_IL.0,7_IC1150505_KO8,20.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=data%2520analyst', 
                      'https://www.glassdoor.com/Job/seattle-data-analyst-jobs-SRCH_IL.0,7_IC1150505_KO8,20_IP2.htm?includeNoSalaryJobs=true&pgc=AB4AAYEAHgAAAAAAAAAAAAAAAfIkpUYAMQEBAQgAobqqabHThiH41Zd%2FV0ZskPNB3AxbpQX5LppJCuB3fomVwkRwAv2DkPAwgk4AAA%3D%3D',
                      'https://www.glassdoor.com/Job/seattle-data-analyst-jobs-SRCH_IL.0,7_IC1150505_KO8,20_IP3.htm?includeNoSalaryJobs=true&pgc=AB4AAoEAPAAAAAAAAAAAAAAAAfIkpUYASQEBARILjMiEUAfjSESQFv%2FS0H17lQf8k8MaNuVr77z1LxSPBs3RHQJvI8Vdbto2PuhBitPeY4eE0end%2BSxjib83fskVh1jbFUIAAA%3D%3D',
                      'https://www.glassdoor.com/Job/seattle-data-analyst-jobs-SRCH_IL.0,7_IC1150505_KO8,20_IP4.htm?includeNoSalaryJobs=true&pgc=AB4AA4EAWgAAAAAAAAAAAAAAAfIkpUYAXAEDARQqCRQGF4%2F%2BcYvyRzvUf6RaBgmTEaN0izoiGel%2FMbiV7%2Faapz3IRBnvNyIt06JcBB%2BT6WDnL7y3DbOnJ4vSBVurBbme59Yg2fHn6OdyNtPMrK2WpwV%2BYx8dAAA%3D',
                      'https://www.glassdoor.com/Job/seattle-data-analyst-jobs-SRCH_IL.0,7_IC1150505_KO8,20_IP5.htm?includeNoSalaryJobs=true&pgc=AB4ABIEAeAAAAAAAAAAAAAAAAfIkpUYAXgEBASYSJI8%2FuqWcmYtLOSVFYozfvOsM%2F06tYAXewKJnlNejOmLsl%2Bs5%2F4ZoFqsusqH2smmfEauzWkjAZ449oqDlkDxrCW82wXLsbxJQR3AT4g8X1y41uhWcwFFdIdoAAA%3D%3D']

paginationSoupList = []
for url in paginationUrlList:
    response = requests.get(url, headers = headers)
    paginationSoup = BeautifulSoup(response.text, 'html.parser')
    paginationSoupList.append(paginationSoup)

# --

#response = requests.get("https://www.glassdoor.com/Job/seattle-data-analyst-jobs-SRCH_IL.0,7_IC1150505_KO8,20.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=data%2520analyst", headers = headers) # send request to site with the url
jobUrlTemplate = "https://www.glassdoor.com{}" # for use in navigating to each jobUrl to get job description

pageCompanyList = []
pageLocationList = []
pageSalaryList = []
pageTitleList = []

pageDescriptionList = []
pageQualificationsList = []
for soup in paginationSoupList:
    
    #print(soup.prettify()) # Need to increase ipython console line limit to read all of it when you use prettify()
    
    companyResults = soup.find_all('td', attrs = {'class': 'company'})
    locationResults = soup.find_all('td', attrs = {'class': 'location'})
    jobResults = soup.find_all('td', attrs = {'class': 'job_title'})
    salaryResults = soup.find_all('span', attrs = {'class': 'css-1xe2xww e1wijj242'}) #fix missing vlaues
    
    companyList = []
    for tag in companyResults:
        companyList.append(tag.text.lower().strip())
    locationList = []
    for tag in locationResults:
        locationList.append(tag.text.lower().strip())
    # salaryList = []
    # for tag in salaryResults:
    #     salaryList.append(tag.text.lower().strip())
    jobTitleList = []
    for tag in jobResults: 
        jobTag = tag.find('a')    
        jobTitle = jobTag.text
        jobTitleList.append(jobTitle.lower().strip())

    pageCompanyList.append(companyList) # !!!! - LIST OF LIST
    pageLocationList.append(locationList) # !!!! - LIST OF LIST
    #pageSalaryList.append(salaryList) # !!!! - LIST OF LIST 
    pageTitleList.append(jobTitleList) # !!!! - LIST OF LIST 


    jobUrlList = []
    for tag in jobResults:
        jobTag = tag.find('a')
        jobUrl = jobUrlTemplate.format(jobTag['href']) # adds the suffix for the specific job onto the base www.glassdoor.com url 
        jobUrlList.append(jobUrl)

    
    #print(jobTitleList)
    #print(len(jobUrlList))


    jobDescriptionList = []
    salaryList = []
    for url in jobUrlList:
        jobPage = requests.get(url, headers = headers)
        jobPageSoup = BeautifulSoup(jobPage.text, 'html.parser')
        #print(jobPageSoup.prettify())
        salaryTag = jobPageSoup.find('span', attrs = {'class' : 'small css-10zcshf e1v3ed7e1'})
        #print(salaryTag)
        try:
            salary = salaryTag.text.strip() 
        except:
            print('No salary info')
            salary = 'NO SALARY INFO'
            
        try:
            descriptionTag = jobPageSoup.find_all('div', attrs = {'id': 'JobDescriptionContainer'})
            description = descriptionTag[0].text
        except:
            print('skipping page, no job description')
            description = 'NO DESCRIPTION FOUND'
        jobDescriptionList.append(description)
        salaryList.append(salary)
    pageSalaryList.append(salaryList)
    
    pageDescriptionList.append(jobDescriptionList) # !!!! - LIST OF LIST
    
    #key words to look for: Skills, Education, Experience, requirements, qualifications
    keyWords = ['experience', 'requirements', 'qualifications']
    
    jobQualificationsList = []
    for jobDescription in jobDescriptionList:
        jobDescription = jobDescription.lower().strip() # convert to lowercase for easier matching
        found = False
        for word in keyWords:
            location = jobDescription.find(word)
            #print('location:', location)
            if location != -1:
                #print('word:', word)
                found = True
                jobQualifications = jobDescription[location:]
                break # can break out of loop once one of the words is found
        if not found: 
            jobQualifications = 'QUALIFICATIONS NOT FOUND'
        #print(jobQualifications[:150])
        jobQualificationsList.append(jobQualifications)
    pageQualificationsList.append(jobQualificationsList) # !!!! - LIST OF LIST

fullQualificationsList = [q for sublist in pageQualificationsList for q in sublist]
fullTitleList = [q for sublist in pageTitleList for q in sublist]
fullCompanyList = [q for sublist in pageCompanyList for q in sublist]
fullLocationList = [q for sublist in pageLocationList for q in sublist]
fullDescriptionList = [q for sublist in pageDescriptionList for q in sublist]
fullSalaryList = [q for sublist in pageSalaryList for q in sublist]

qualificationsList = pd.DataFrame(fullQualificationsList)
titleList = pd.DataFrame(fullTitleList)
companyList = pd.DataFrame(fullCompanyList)
locationList = pd.DataFrame(fullLocationList)
descriptionList = pd.DataFrame(fullDescriptionList)
salaryList = pd.DataFrame(fullSalaryList)

df = pd.concat([titleList, companyList, locationList, salaryList, qualificationsList, descriptionList], axis = 1)
df.columns = ['Job Title', 'Company', 'Location', 'Salary', 'Qualifications', 'Full Description']

#df.to_csv("C:/Users/micha/Desktop/Python Projects/glassdoor.csv")
 
# NOTE: ANALYSIS IS PERFORMED IN glassdoorAnalysis.py