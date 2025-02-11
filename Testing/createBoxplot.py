import matplotlib.pyplot as plt
import pandas as pd

df1 = pd.read_excel("time_data.xlsx", sheet_name="Sheet1")

df2 = pd.read_excel("times_server.xlsx", sheet_name="Sheet1")

plt.figure(figsize=(8, 6))

plt.boxplot(df1["Time_Value"].dropna(), vert=True, patch_artist=True, positions=[1], widths=0.6, labels=["local"])

plt.boxplot(df2["Time_Value"].dropna(), vert=True, patch_artist=True, positions=[2], widths=0.6, labels=["Server"])

plt.title("Comparison ")
plt.ylabel("Time Value in Ms")
plt.xticks([1, 2], ['local', 'Server'])

plt.savefig("boxplot_comparison.png")
plt.show()
