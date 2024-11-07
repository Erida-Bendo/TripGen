import pandas as pd

df = pd.read_excel("./resources/Trip Generation Old Tool.xlsm", "NF-Sets")
print(df.iloc[4,4+5*0])
