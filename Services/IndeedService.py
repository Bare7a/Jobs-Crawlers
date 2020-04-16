from pyquery import PyQuery as pq

from Services.Models.Job import Job
from Services.Models.Service import Service

class IndeedService(Service):
  
  def getInitialUrlAddress(self):
    urlAddress = f'https://www.indeed.com/jobs?q={self.jobName}&start=0'
    return urlAddress

  def getNextUrlAddress(self):
    return self.nextPageUrlAddress

  def getJobs(self, urlAddress):
    jobs = []
    jobIds = self.fetchJobIds(urlAddress)
    jobIdsCount = len(jobIds)
    for i in range(jobIdsCount):
      jobId = jobIds[i]
      job = self.fetchJobData(jobId)
      jobs.append(job)
    
    return jobs

  def fetchJobIds(self, urlAddress):   
    html = self.getHTML(urlAddress)
    d = pq(html)
    jobIdElems = d('.jobsearch-SerpJobCard')
    jobIdCount = jobIdElems.size()

    jobIds = []
    for i in range(jobIdCount):
      jobIdElem = jobIdElems.eq(i)
      jobId = jobIdElem.attr("data-jk")
      jobIds.append(jobId)

    pagesElems = d('.pagination a')
    pagesCount = pagesElems.size()
    nextPageElem = pagesElems.eq(pagesCount - 1)
    nextPageElemNumber = nextPageElem.text()

    if nextPageElemNumber == '' or 'Next' in nextPageElemNumber or 'next' in nextPageElemNumber:
      nextPageUri = nextPageElem.attr('href')
      self.nextPageUrlAddress = f'https://www.indeed.com{nextPageUri}'
    else:
      self.nextPageUrlAddress = False
    
    return jobIds

  def fetchJobData(self, jobId):
    infoUrlAddress = f'https://www.indeed.com/viewjob?jk={jobId}&from=vjs&vjs=1&dup=1'
    data = self.getJSON(infoUrlAddress)

    date = data['vfvm']['jobAgeRelative']
    title = data['jobTitle']
    company = data['vfvm']['jobSource']
    posType = data['jtsT']

    descriptionUrlAddress = f'https://www.indeed.com/rpc/jobdescs?jks={jobId}'
    description = pq((self.getJSON(descriptionUrlAddress))[jobId]).text()

    job = Job(jobId, title, posType, company, date, description)
    return job
