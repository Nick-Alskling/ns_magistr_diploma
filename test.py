import pandas as pd
df = pd.DataFrame({"col1" : range(1,5), 
                   "col2" : ['A A','B B','A A','B B'],
                   "col3" : ['A A','A A','B B','B B']
                   })
myvar1 = 'col2'
newdf2 = df.query("{0} == 'A A'".format(myvar1))
print(newdf2)