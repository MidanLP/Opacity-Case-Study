import matplotlib.pyplot as plt
import pandas as pd

df1 = pd.read_excel("time_output.xlsx", sheet_name="Testing Timings")

#df2 = pd.read_excel("time_output.xlsx", sheet_name="Server, Cache")

#df3 = pd.read_excel("time_data.xlsx", sheet_name="Sheet1")

plt.figure(figsize=(8, 6))

plt.boxplot(df1["Time"].dropna(), vert=True, patch_artist=True, positions=[1], widths=0.6, labels=["normal Time"]) #Values vor standard  measurement

plt.boxplot(df1["Bust"].dropna(), vert=True, patch_artist=True, positions=[2], widths=0.6, labels=["bust Time"]) #Values vor Cache-Bust measurement

#plt.boxplot(df3["Time_Value"].dropna(), vert=True, patch_artist=True, positions=[3], widths=0.6, labels=["Server, cache"])

plt.title("Timing result")
plt.ylabel("Time Value in Ms")
#plt.xticks([1, 2, 3], ['local, cache','local, no cache', 'Server, cache'])

plt.savefig("CacheVsBust.png") #name of file to be created
plt.show()
