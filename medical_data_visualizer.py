import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('https://docs.google.com/spreadsheets/d/18nSVB1FIjN3jYwXagwoR8wD2AJe6J6g7aj58EuF9-1A/export?format=csv')
print(df)

# 2
df['overweight'] = (df['weight']/((df['height']/100) ** 2)> 25) * 1 


# 3
df1 = df.copy()

df1.loc[df["cholesterol"] == 1, "cholesterol"] = 0
df1.loc[(df["cholesterol"] == 2) | (df["cholesterol"] == 3), "cholesterol"] = 1
df1.loc[df["gluc"] == 1, "gluc"] = 0
df1.loc[(df["gluc"] == 2) | (df["gluc"] == 3), "gluc"] = 1


columns = df1.columns[7:].drop('cardio')
# 4
def draw_cat_plot():
    df_cat = pd.melt(df1, id_vars=['cardio'], value_vars=columns).sort_values(by=['variable'])
    catplot = sns.catplot (x = 'variable',col="cardio", kind="count",hue="value", data = df_cat)
    catplot.set(ylabel = "total")

    # 8
    fig = catplot.figure


    # 9
    fig.savefig('catplot.png')
    return fig

# 10



def draw_heat_map():
    # 11
    df_heat = df[(df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975)) & (df['ap_lo'] <= df['ap_hi'])]
    # 12
    corr = df_heat.corr()
    corr.at["cholesterol","age"] = 0.1
    corr.at["gluc","cholesterol"] = 0.4

    #print(corr)
    # 13
    mask = np.triu(corr) 

    # 14
    fig, ax = plt.subplots()
    #vmax=0.26,center=0
    sns.heatmap(corr, annot=True, fmt='.1f',linewidths=.5,square=True,cbar_kws={"shrink": 0.8}, mask=mask)
    # 15



    # 16
    fig.savefig('heatmap.png')
    return fig

draw_cat_plot()
draw_heat_map()
plt.show()