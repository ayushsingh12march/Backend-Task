class Profile:
  
  _object = None 

  def __init__(self,first_name,last_name,email_field, **kwargs):
    if first_name == None or last_name == None or email_field == None:
      raise Exception("first_name, last_name, email_field are mandatory")
    self._object = {
      'first_name' : first_name,
      'last_name' : last_name,
      'email_field' : email_field
    }
    
    # get other fields entered by the user
    for key,val in kwargs.items():
      self._object[key] = val
  
  def get_profile(self):
    return self._object
    
    
    