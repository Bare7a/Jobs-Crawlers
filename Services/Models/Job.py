class Job:
  def __init__(self, id, title, posType, company, date, description):
    self.id = id or 'N/A'
    self.title = title or 'N/A'
    self.posType = posType or 'N/A'
    self.company = company or 'N/A'
    self.date = date or 'N/A'
    self.description = description or 'N/A'

  def __repr__(self):
    return f'{self.title}, {self.posType}, {self.company}, {self.date}, {len(self.description)}'

  def getJSON(self):
    return { 'title': self.title, 'posType': self.posType, 'company': self.company, 'date': self.date, 'description': self.description }
