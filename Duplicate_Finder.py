from concurrent.futures import as_completed, ProcessPoolExecutor
import json
from multiprocessing import  Process,Value,Lock,Queue,freeze_support
from pprint import pprint

from Profile import Profile

class Duplication(Process):
  
  def __init__(self,profiles):
    super(Duplication, self).__init__()
    self.profiles = profiles
    self.total_match_score = Value('i',0)
    self.matching_attributes = Queue()
    self.non_matching_attributes =Queue()
    
  def field_wise_duplicates(self,field,lock):
    
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
                with lock:
                  self.total_match_score.value -= 1
                self.non_matching_attributes.put(field)
            else:
                with lock:
                  self.total_match_score.value += 1
                self.matching_attributes.put(field)
    
    return json.dumps({"field" : field, "status" : "Done" })

  def findDuplicates(self,fields):
    
    lock = Lock()
    for field in fields:
      p = Process(target=self.field_wise_duplicates,args=(field,lock))
      p.start()
      p.join()
    # returnself.get_result()
      
  def get_queue(self,q):
    arr = []
    """
    function to print queue elements
    """
    if q.empty()==True:
      return None

    while not q.empty():
        arr.append(q.get())
    return arr

  def get_result(self):
    return {
      "profiles" : self.profiles,
      "total_match_score" : self.total_match_score.value ,
      "matching_attributes" : self.get_queue(self.matching_attributes) ,
      "non_matching_attributes" : self.get_queue(self.non_matching_attributes) ,

    }

def main():
  o1 = Profile(id=1,first_name = "Kanhai", last_name = "Shah",email_field = "kowkanhai@gmail.com")
  o2 = Profile(first_name = "Kanhai", last_name = "Shah",email_field = "knowkanhai@gmail.com")
  print(o1.get_profile())
  print(o1.get_profile())
  df = Duplication([o1.get_profile(),o2.get_profile()])
  df.findDuplicates(['email_field','first_name','last_name','id'])
  print(df.get_result())
  

if __name__ == '__main__':
  freeze_support()
  main()
    