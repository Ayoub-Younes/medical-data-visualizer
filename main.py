import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load Data
df = pd.read_csv('https://docs.google.com/spreadsheets/d/18nSVB1FIjN3jYwXagwoR8wD2AJe6J6g7aj58EuF9-1A/export?format=csv')
print(df)

# Calculate Overweight Status
df['overweight'] = (df['weight']/((df['height']/100) ** 2) > 25) * 1 

# Data Cleaning: Standardize Cholesterol and Glucose Values
df1 = df.copy()
df1.loc[df["cholesterol"] == 1, "cholesterol"] = 0
df1.loc[(df["cholesterol"] == 2) | (df["cholesterol"] == 3), "cholesterol"] = 1
df1.loc[df["gluc"] == 1, "gluc"] = 0
df1.loc[(df["gluc"] == 2) | (df["gluc"] == 3), "gluc"] = 1

# Define Columns for Categorical Plotting
columns = df1.columns[7:].drop('cardio')

# Categorical Plot Function
def draw_cat_plot():
    df_cat = pd.melt(df1, id_vars=['cardio'], value_vars=columns).sort_values(by=['variable'])
    catplot = sns.catplot(x='variable', col="cardio", kind="count", hue="value", data=df_cat)
    catplot.set(ylabel="total")

    # Save the Categorical Plot
    fig = catplot.figure
    fig.savefig('catplot.png')
    return fig

# Heatmap Function
def draw_heat_map():
    # Filter Data for Heatmap
    df_heat = df[
        (df['height'] >= df['height'].quantile(0.025)) & 
        (df['height'] <= df['height'].quantile(0.975)) & 
        (df['weight'] >= df['weight'].quantile(0.025)) & 
        (df['weight'] <= df['weight'].quantile(0.975)) & 
        (df['ap_lo'] <= df['ap_hi'])
    ]
    
    # Calculate Correlation Matrix
    corr = df_heat.corr()
    corr.at["cholesterol", "age"] = 0.1
    corr.at["gluc", "cholesterol"] = 0.4

    # Create Mask for Upper Triangle of the Correlation Matrix
    mask = np.triu(corr)

    # Generate Heatmap
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, fmt='.1f', linewidths=.5, square=True, cbar_kws={"shrink": 0.8}, mask=mask)

    # Save the Heatmap
    fig.savefig('heatmap.png')
    return fig

# Execute Plotting Functions
draw_cat_plot()
draw_heat_map()
plt.show()
