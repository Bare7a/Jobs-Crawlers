import os
import csv
import time
import requests
from Services.Models.Job import Job

class Service:
  def __init__(self, jobName):
    self.jobName = jobName
    self.nextPageUrlAddress = 'init'

    self.csvFile = False
    self.csvWriter = False
    self.currentTime = time.time()
    self.serviceName = self.__class__.__name__.replace('Service', '')
    self.fileName = f'{self.serviceName}-{self.jobName}-{self.currentTime}.csv'
    self.fileLocation = os.path.join(os.getcwd(),'Data', self.fileName)

  def getJobs(self):
    raise Exception('GET JOBS IS NOT IMPLEMENTED')

  def getInitialUrlAddress(self):
    raise Exception('GET INITIAL URL ADDRESS IS NOT IMPLEMENTED')

  def getNextUrlAddress(self):
    raise Exception('GET NEXT URL ADDRESS IS NOT IMPLEMENTED')


  def openCsvFile(self):
    if not os.path.isdir('Data'):
      os.makedirs('Data')
    
    self.csvFile = open(self.fileLocation, 'a+', encoding='utf-8')
    fieldNames = ['title', 'posType', 'company', 'date', 'description']
    self.csvWriter = csv.DictWriter(self.csvFile, fieldnames=fieldNames)
    self.csvWriter.writeheader()
    print(f'Opened a file at: {self.fileLocation}')

  def writeLineToCsvFile(self, job: Job):
    if self.csvFile == False or self.csvWriter == False:
      raise Exception('CSV FILE IS NOT OPENED')

    jsonObj = job.getJSON()
    self.csvWriter.writerow(jsonObj)

  def writeLinesToCsvFile(self, jobs: [Job]):
    if self.csvFile == False or self.csvWriter == False:
      raise Exception('CSV FILE IS NOT OPENED')

    jsonObjs = []
    jobCounts = len(jobs)
    for i in range(jobCounts):
      job = jobs[i]
      jsonObj = job.getJSON()
      jsonObjs.append(jsonObj)

    self.csvWriter.writerows(jsonObjs)

  def closeCsvFile(self):
    if self.csvFile:
      self.csvFile.close()
    print(f'Closed a file at: {self.fileLocation}')

  def setJobName(self, jobName):
    self.jobName = jobName

  def getJobName(self):
    return self.jobName

  def getHTML(self, urlAddress, retries=5):
    for i in range(retries):
      try:
        html = requests.get(urlAddress).text
        return html
      except:
        print(f'--- RETRYING TO FETCH HTML {i + 1}: {urlAddress}')

    print(f'--- FAILED TO FETCH HTML: {urlAddress}')
    return False

  def getJSON(self, urlAddress, retries=5):
    for i in range(retries):
      try:
        json = requests.get(urlAddress).json()
        return json
      except:
        print(f'--- RETRYING TO FETCH HTML {i + 1}: {urlAddress}')

    print(f'--- FAILED TO FETCH HTML: {urlAddress}')
    return False

  def getTEXT(self, urlAddress, retries=5):
    for i in range(retries):
      try:
        text = pq(urlAddress).text()
        return text
      except:
        print(f'--- RETRYING TO FETCH TEXT {i + 1}: {urlAddress}')
    
    print(f'--- FAILED TO FETCH TEXT: {urlAddress}')
    return False
