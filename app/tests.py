from cmath import nan
import pandas as pd

df = pd.read_excel("Libro1 - copia.xlsx", index_col = None, sheet_name = "ENVIABLES")

print(df)
mlist = df['Estado'].tolist()

print(mlist)


new_df = pd.DataFrame({'Estado' : [None,2,5,6,7,2,6,8,'Hola',"Amigos"]})


df.update(new_df)
print(df)
