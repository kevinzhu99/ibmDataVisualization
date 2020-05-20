import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

df_can = pd.read_excel('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/Canada.xlsx',
                       sheet_name='Canada by Citizenship',
                       skiprows=range(20),
                       skipfooter=2
                      )

print('Data downloaded and read into a dataframe!')


df_can.drop(['AREA', 'REG', 'DEV', 'Type', 'Coverage'], axis = 1, inplace = True)

df_can.rename(columns = {'OdName': 'Country', 'AreaName' : 'Continent', 'RegName': 'Region'}, inplace = True)
#purpose of this is to keep consistency, making all columns strings instead of int
df_can_columns = list(map(str, df_can.columns))

#Set the country name as index, useful for quickly looking up countries using strings
df_can.set_index('Country', inplace = True)

df_can['Total'] = df_can.sum(axis = 1)

years = list(map(str, range(1980, 2013)))
print('data dimensions', df_can.shape)


mpl.style.use('ggplot')

#pie charts: Groupby continent
df_continents = df_can.groupby('Continent', axis = 0).sum()

colors_list = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen', 'pink']
explode_list = [0.1, 0, 0, 0, 0.1, 0.1] # ratio for each continent with which to offset each wedge.

# autopct create %, start angle represent starting point
df_continents['Total'].plot(kind='pie',
                            #sets the image size to 5inches wide and 6inches high
                            figsize=(15, 8),
                            autopct='%1.1f%%',
                            startangle=90,
                            shadow=True,
                            labels=None,  # turn off labels on pie chart
                            pctdistance=1.12,
                            # the ratio between the center of each pie slice and the start of the text generated by autopct
                            colors=colors_list,  # add custom colors
                            explode=explode_list  # 'explode' lowest 3 continents
                            )

plt.title('Immigration to Canada by Continent [1980 - 2013]')
plt.axis('equal') # Sets the pie chart to look like a circle.
plt.legend(labels=df_continents.index, loc='upper left')

plt.show()

#Question: Using a pie chart, explore the proportion (percentage) of new immigrants grouped by continents in the year 2013.
### type your answer here
colors_list = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgreen', 'pink']
explode_list = [0.1, 0, 0, 0, 0.1, 0.1]

df_continents['2013'].plot(kind = 'pie',
                          figsize = (15,8),
                          autopct = '%1.1f%%',
                          startangle = 90,
                          shadow = True,
                          labels = None,
                          pctdistance = 1.12,
                          )
plt.title = ('Immigration to Canada by Continent 2013')
plt.axis('equal')
plt.legend(labels = df_continents.index, loc = 'upper right')

plt.show()


#boxplots
#df_Cl = df_can.loc[['China', 'India'], years].transpose()
#df_Cl

#df_Cl.describe()
#df_Cl.plot(kind = "box",
#          figsize = (10,7))
#plt.title('Box plots of Immigrants from China and India (1980 - 2013)')
#plt.xlabel('Number of Immigrants')
#plt.show

#subplots
fig = plt.figure() # create figure

ax0 = fig.add_subplot(1, 2, 1) # add subplot 1 (1 row, 2 columns, first plot)
ax1 = fig.add_subplot(1, 2, 2) # add subplot 2 (1 row, 2 columns, second plot). See tip below**

# Subplot 1: Box plot
df_Cl.plot(kind='box', color='blue', vert=False, figsize=(20, 6), ax=ax0) # add to subplot 1
ax0.set_title('Box Plots of Immigrants from China and India (1980 - 2013)')
ax0.set_xlabel('Number of Immigrants')
ax0.set_ylabel('Countries')

# Subplot 2: Line plot
df_Cl.plot(kind='line', figsize=(20, 6), ax=ax1) # add to subplot 2
ax1.set_title ('Line Plots of Immigrants from China and India (1980 - 2013)')
ax1.set_ylabel('Number of Immigrants')
ax1.set_xlabel('Years')

plt.show()

#Question: Create a box plot to visualize the distribution of the top 15 countries (based on total immigration) grouped by the decades 1980s, 1990s, and 2000s.
df_top15 = df_can.sort_values(['Total'], ascending=False, axis=0).head(15)
df_top15
list1 = list(map(str,range(1980,1990)))
list2 = list(map(str,range(1990,2000)))
list3 = list(map(str,range(2000,2010)))

df_80s = df_top15.loc[:, list1].sum(axis = 1)
df_90s = df_top15.loc[:, list2].sum(axis = 1)
df_00s = df_top15.loc[:, list3].sum(axis = 1)

new_df = pd.DataFrame({'1980s': df_80s, '1990s' : df_90s, '2000s': df_00s})

new_df.head()
new_df.describe()
new_df.plot(kind='box', figsize=(10, 6))
plt.title('Immigration from top 15 countries for decades 80s, 90s and 2000s')
plt.show()
# let's check how many entries fall above the outlier threshold
new_df[new_df['2000s']> 209611.5]

#scatterplot
# we can use the sum() method to get the total population per year
df_tot = pd.DataFrame(df_can[years].sum(axis=0))

# change the years to type int (useful for regression later on)
df_tot.index = map(int, df_tot.index)

# reset the index to put in back in as a column in the df_tot dataframe
df_tot.reset_index(inplace = True)

# rename columns
df_tot.columns = ['year', 'total']

# view the final dataframe
df_tot.head()

x = df_tot['year']
y = df_tot['total']
fit = np.polyfit(x,y,deg = 1)
df_tot.plot(kind='scatter', x='year', y='total', figsize=(10, 6), color='darkblue')

plt.title('Total Immigration to Canada from 1980 - 2013')
plt.xlabel('Year')
plt.ylabel('Number of Immigrants')

# plot line of best fit
plt.plot(x, fit[0] * x + fit[1], color='red') # recall that x is the Years
plt.annotate('y={0:.0f} x + {1:.0f}'.format(fit[0], fit[1]), xy=(2000, 150000))

plt.show()

# print out the line of best fit
'No. Immigrants = {0:.0f} * Year + {1:.0f}'.format(fit[0], fit[1])



#Question: Create a scatter plot of the total immigration from Denmark, Norway, and Sweden to Canada from 1980 to 2013?
df_countries = df_can.loc[['Denmark', "Norway", 'Sweden'], years].transpose()

df_total = pd.DataFrame(df_countries.sum(axis = 1))

df_total.reset_index(inplace = True)

df_total.columns = ['year', 'total']

df_total.head()

df_total.plot(kind = 'scatter',
             x = 'year',
             y = 'total',
             figsize = (10,6),
             color = 'red')

plt.title("Immigration between Denmark, Norway and Sweden")
plt.xlabel("Total")
plt.ylabel("Year")

plt.show()

#bubble plots
#Argentina's great depression

df_can_t = df_cam[years].transpose()
df_can_t.index = map(int, df_can_t)
df_can_t.index.name = 'Year'
df_can_t.reset_index(inplace = True)
df_can_t.head()

# normalize Brazil data
norm_brazil = (df_can_t['Brazil'] - df_can_t['Brazil'].min()) / (df_can_t['Brazil'].max() - df_can_t['Brazil'].min())

# normalize Argentina data
norm_argentina = (df_can_t['Argentina'] - df_can_t['Argentina'].min()) / (df_can_t['Argentina'].max() - df_can_t['Argentina'].min())

# Brazil
ax0 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='Brazil',
                    figsize=(14, 8),
                    alpha=0.5,                  # transparency
                    color='green',
                    s=norm_brazil * 2000 + 10,  # pass in weights
                    xlim=(1975, 2015)
                   )

# Argentina
ax1 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='Argentina',
                    alpha=0.5,
                    color="blue",
                    s=norm_argentina * 2000 + 10,
                    ax = ax0
                   )

ax0.set_ylabel('Number of Immigrants')
ax0.set_title('Immigration from Brazil and Argentina from 1980 - 2013')
ax0.legend(['Brazil', 'Argentina'], loc='upper left', fontsize='x-large')


#Question: Previously in this lab, we created box plots to compare immigration from China and India to Canada. Create bubble plots of immigration from China and India to visualize any differences with time from 1980 to 2013. You can use df_can_t that we defined and used in the previous example.
### type your answer here
norm_China = (df_can_t['China'] - df_can_t['China'].min())/(df_can_t['China'].max() - df_can_t['China'].min())
norm_India = (df_can_t['India'] - df_can_t['India'].min()) / (df_can_t['India'].max() - df_can_t['India'].min())

### type your answer here
ax2 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='China',
                    figsize=(14, 8),
                    alpha=0.5,                  # transparency
                    color='green',
                    s=norm_China * 2000 + 10,  # pass in weights
                    xlim=(1975, 2015)
                   )

# Argentina
ax3 = df_can_t.plot(kind='scatter',
                    x='Year',
                    y='India',
                    alpha=0.5,
                    color="blue",
                    s=norm_India * 2000 + 10,
                    ax = ax2
                   )

ax0.set_ylabel('Number of Immigrants')
ax0.set_title('Immigration from China and India from 1980 - 2013')
ax0.legend(['China', 'India'], loc='upper left', fontsize='x-large')







