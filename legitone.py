try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 
  
# to search 
query = "Barcelona Unique Experiences"
  
for j in search(query, tld="co.in", num=30, stop=1, pause=2): 
    print(j)