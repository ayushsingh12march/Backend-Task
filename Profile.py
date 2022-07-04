class Profile:
  _object = None 
  def __init__(self,first_name,last_name,email_field, **kwargs):
    ###### check for data type ######
    self._object = {
      'first_name' : first_name,
      'last_name' : last_name,
      'email_field' : email_field
    }
    
    for key,val in kwargs.items():
      self._object[key] = val
  
  def get_profile(self):
    return self._object
    
    ###### check for data type ######
    
    