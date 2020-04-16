from Services.IndeedService import IndeedService
from Services.MonsterService import MonsterService


def main():
  Services = []
  Services.append(IndeedService)
  Services.append(MonsterService)

  Service = selectService(Services)

  jobName = input('Job name: ')
  service = Service(jobName)

  service.openCsvFile()
  nextPageUrlAddress = service.getInitialUrlAddress()
  while not nextPageUrlAddress == False:
    print(f'Fetching data from page: {nextPageUrlAddress}')

    jobs = service.getJobs(nextPageUrlAddress)
    jobsCount = len(jobs)
    for i in range(jobsCount):
      print(f'    {jobs[i]}')

    nextPageUrlAddress = service.getNextUrlAddress()
    service.writeLinesToCsvFile(jobs)
  service.closeCsvFile()

def selectService(services):
  serviceId = False
  servicesCount = len(services)
  print('--- Select a Service ---')
  print()
  while(not(serviceId)):
    for i in range(servicesCount):
      id = i + 1
      service = services[i]
      serviceName = service.__name__
      print(f'[{id}] {serviceName}')
    print()
    serviceId = input('Service Number [1 - {servicesCount}]: '.format(servicesCount=servicesCount))
    try:
      serviceId = int(serviceId)
      if(serviceId > servicesCount or serviceId < 1):
        serviceId = False
    except:
      serviceId = False
  print()
  serviceId = serviceId - 1
  service = services[serviceId]
  return service

main()