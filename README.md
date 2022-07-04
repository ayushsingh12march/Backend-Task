# Expectations the solution fulfills :-
* The code can run on multi core machines with better performance as `multiprocessor` concept of python is used.
* The code can `scale` for more than 2 pofiles.
* The fields are extensible, any number of fields are supported by `Profile class`.
<br>
<br>
<br>

# How to run the code

* clone the repo and install requirements.txt packages in your respective container/virtualenv
* run :-
```
python3 Duplicate_Finder.py    
```
<br>
<br>
<br>

# To try custom inputs, modify main function accordigly
```
def main():

  o1 = Profile(id=1,first_name = "Kanhai", last_name = "Shah",email_field = "kowkanhai@gmail.com", random_field=1)
  o2 = Profile(first_name = "Kanhai", last_name = "Shah",email_field = "knowkanhai@gmail.com")
  df = Duplication([o1.get_profile(),o2.get_profile()])
  df.findDuplicates(['email_field','first_name','last_name','random_field'])
  print(df.get_result())
```

<br>
<br>
<br>

# Small logic I tweeked :-
<ol>
    <li> It is given in question that :- 
    * if first_name + last_name + email match between two profiles is greater than
80% (you can try using a library like https://pypi.org/project/fuzzywuzzy/), increase the match score to 1

<li> Also in <strong>find_duplicates</strong> sometimes all these 3 fields are not passed
</ol>


*  To resolve this confusion, what I have done :-
    * If any of `first_name, last_name, email_field` is passed, the fuzz logic is performed as in every Profile these fields are mandatory to be there and they will be there.
    * if fuzz_logic gives >80% match, total_match_score is incremented by 1
