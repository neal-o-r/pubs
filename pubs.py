import pandas as pd
import matplotlib.pyplot as plt

# use a nice plotting style
plt.style.use('fivethirtyeight')

# read in csv data
df = pd.read_csv('renewed-liquor-licence-register.csv')


def county_bars(df):

	# get a data frame of pubs
	# we make a copy here, otherwise df_pubs would not be a seperate
	# object in memory
	df_pubs = df[df.Licence_Type == "Publican's Licence (7-Day Ordinary)"].copy()

	print('There are {} pubs in Ireland'.format(len(df_pubs)))

	# Dublin is broken up into post codes, replace anything with 
	# 'Dublin' in it with the string 'Co. Dublin'
	df_pubs['County'] = df_pubs['County'].apply(lambda x: 
				'Co. Dublin' if 'Dublin' in x else x)

	# group by county and count the number of trading names in each
	# make a bar plot
	df_pubs.groupby('County').Trading_Name.count().plot(kind='bar')
	
	plt.show()
