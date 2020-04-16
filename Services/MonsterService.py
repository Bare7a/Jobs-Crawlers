import math
from pyquery import PyQuery as pq

from Services.Models.Job import Job
from Services.Models.Service import Service

class MonsterService(Service):
  
  def getInitialUrlAddress(self):
    jobsCount = int(pq(f'https://www.monster.com/jobs/search/?q={self.jobName}').find('.mux-search-results').eq(0).attr('data-total-search-results'))
    self.lastPage = math.ceil(jobsCount / 25)

    self.currentPage = 1
    urlAddress = f'https://www.monster.com/jobs/search/pagination/?q={self.jobName}&isDynamicPage=true&isMKPagination=true&page={self.currentPage}'
    return urlAddress

  def getNextUrlAddress(self):
    self.currentPage = self.currentPage + 1

    if(self.lastPage >= self.currentPage):
      self.nextPageUrlAddress = f'https://www.monster.com/jobs/search/pagination/?q={self.jobName}&isDynamicPage=true&isMKPagination=true&page={self.currentPage}'
    else:
      self.nextPageUrlAddress = False
    
    return self.nextPageUrlAddress

  def getJobs(self, urlAddress):
    jobs = self.fetchJobsData(urlAddress)
    jobsCount = len(jobs)
    for i in range(jobsCount):
      job = jobs[i]
      job.description = self.fetchJobDescription(job.id)
    
    return jobs

  def fetchJobsData(self, urlAddress):   
    jobsData = self.getJSON(urlAddress)
    jobsDataCount = len(jobsData)

    jobs = []
    for i in range(jobsDataCount):
      jobData = jobsData[i]
      
      if('InlineApasAd' in jobData):
        continue
      
      jobId = jobData['MusangKingId']
      title = jobData['Title']
      company = jobData['Company']['Name']
      date = jobData['DatePosted']

      job = Job(jobId, title, 'N/A', company, date, 'N/A')
      jobs.append(job)

    return jobs

  def fetchJobDescription(self, jobId):
    urlAddress = f'https://job-openings.monster.com/v2/job/pure-json-view?jobid={jobId}'
    print(urlAddress)
    description = pq(self.getJSON(urlAddress)['jobDescription']).text()

    return description
