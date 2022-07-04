from fuzzywuzzy import fuzz
import json
from multiprocessing import  Process,Value,Lock,Queue,freeze_support
from Profile import Profile

class Duplication(Process):
  
  def __init__(self,profiles):
    super(Duplication, self).__init__()
    ## atleast 2 profiles are needed
    if (len(profiles)<2):
      raise Exception("Atleast 2 profiles are needed for comparison")
    
    self.profiles = profiles
    self.total_match_score = Value('i',0)
    self.matching_attributes = Queue()
    self.non_matching_attributes =Queue()
    self.ignored_attributes = Queue()

  def field_wise_duplicates(self,field,lock):
    """
      logic :- if all profile have this field and they match , increase total score to 1 again. If none of them have the field or even one of them does not have the field, skip the comparison and do not change the total score. If all of them have the field and any one of them is  different, reduce 1 from the total score.
    """
    n=len(self.profiles)
    match_count = 0
    field_count = 0
    lookup_field = self.profiles[0].get(field)
    if lookup_field != None:
      for profile in self.profiles:
        if profile.get(field) != None:
          field_count+=1
        if profile.get(field) == lookup_field:
          match_count+=1

      if field_count == n:          
        if match_count != n:
          #If all of them have the field and any one of them is  different, reduce 1 from the total score.
          with lock:
            self.total_match_score.value -= 1
          self.non_matching_attributes.put(field)
        else:
          #if all profile have this field and they match , increase total score to 1 again
          with lock:
            self.total_match_score.value += 1
          self.matching_attributes.put(field)
      else:
        #If none of them have the field or even one of them does not have the field, skip the comparison and do not change the total score
        self.ignored_attributes.put(field)
    
    return json.dumps({"field" : field, "status" : "Done" })

  def name_email_matcher(self,field, lock):
    """
      In profile first_name, last_name, email_fields are mandatory, therefore whenever atleast one of the field is entered, the fuzz match is done for all the 3 fields
    """
    min_match = 101
    first_string = self.profiles[0].get('first_name') + self.profiles[0].get('last_name') + self.profiles[0].get('email_field')
    for profile in self.profiles:
      full_detail  = profile.get('first_name') + profile.get('last_name') + profile.get('email_field')
      min_match = min(min_match,fuzz.ratio(first_string,full_detail))
    
    if min_match>80:
      with lock:
        self.total_match_score.value += 1
      self.matching_attributes.put('first_name')
      self.matching_attributes.put('last_name')
      self.matching_attributes.put('email_field')

  def findDuplicates(self,fields):
    """
      multiprocess on fields and find field wise duplicates.

      self.name_email_matcher :- In profile first_name, last_name, email_fields are mandatory, therefore whenever atleast one of the field is entered, the fuzz match is done for all the 3 fields

      self.field_wise_duplicates :- Other fields also contribute to total match score

    """
    full_name_check = False
    lock = Lock()
    for field in fields:
      if full_name_check == False and (field == 'first_name' or field == 'last_name' or field == 'email_field'):
        full_name_check = True
        p = Process(target=self.name_email_matcher,args=(field,lock))
        p.start()
        p.join()
      elif field != 'last_name' and field != 'email_field' and field != 'id' and field != 'first_name':
        p = Process(target=self.field_wise_duplicates,args=(field,lock))
        p.start()
        p.join()
    
      
  def get_queue_entries(self,q):
    
    """
    function to return queue elements in list
    """
    arr = []
    if q.empty()==True:
      return None

    while not q.empty():
        arr.append(q.get())
    return arr

  def get_result(self):
    return {
      "profiles" : self.profiles,
      "total_match_score" : self.total_match_score.value ,
      "matching_attributes" : self.get_queue_entries(self.matching_attributes) ,
      "non_matching_attributes" : self.get_queue_entries(self.non_matching_attributes) ,
      "ignored_attributes" : self.get_queue_entries(self.ignored_attributes)

    }

def main():
  ######################### Try your inputs here ####################################
  o1 = Profile(id=1,first_name = "Kanhai", last_name = "Shah",email_field = "kowkanhai@gmail.com", random_field=1)
  o2 = Profile(first_name = "Kanhai", last_name = "Shah",email_field = "knowkanhai@gmail.com")
  df = Duplication([o1.get_profile(),o2.get_profile()]) # pass profiles to findDuplicate for
  df.findDuplicates(['email_field','first_name','last_name','random_field']) # find duplicate fields
  print(df.get_result())
  

if __name__ == '__main__':
  freeze_support()
  main()
    