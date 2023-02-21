import pandas as pd
import numpy as np
import scipy
import matplotlib.pyplot as plt
import seaborn as sns
#import os

#############################
# GET IMPORT FOR EFFICIENCY #
#############################

# data, ch1 (uV, Ve-6), timestamp
INPUT_FILE="./intern_set.csv"

# check if intern_set.1.csv exists
# if yes => skip
# if no  => ...
#           get min num of #s after decimal in each column => 
#           copy file without periods and add e+YY to each col name
# THIS IS FOOLHARDY I CARE ABT EFFICIENCY TOO MUCH.

#import_dtypes = {'timestamp':pd.UInt32Dtype, 'default':pd.Float64Index}
#import_dtypes = {'timestamp':pd.}
# df = pd.read_csv(INPUT_FILE, dtype=import_dtypes)
# numpy has slay datatypes not pandas
# col0: data #
# col1: ch1 (V)
# col2: timestamp (s)
raw_df = pd.read_csv(INPUT_FILE, index_col=0)

#np.

idx_min = np.int64(raw_df.first_valid_index())  # <class 'numpy.int64'>
idx_max = raw_df.last_valid_index()   # <class 'numpy.int64'>

# only accurate up to µV
df = raw_df
#df.rename(columns={'ch1': 'ch1-uV', 'timestamp': 'timestamp-us'})
#df['ch1-uV'].apply(lambda x: x * 1e+06)
#df['timestamp-us'].apply(lambda x: x * 1e+03)

################################
# fix oversampling of emg data #
################################


############################
# predefine graphing funcs #
############################

sns.set_style()

#  *, xlabel: str, ylabel: str
def intern_plot(dataframe: pd.DataFrame, x: str ='ch1', y: str = 'timestamp') -> None:
	"""Use Seaborn to make pretty of any quick n dirty data
	
	Args:
	    dataframe (pd.DataFrame): selectpandas dataframe
	    x (str): name of column from dataframe for x-axis
	    y (str): name of column from dataframe for y-axis
	    xlabel (str): label for x-axis
	    ylabel (str): label for y-axis
	"""

	# evaluate the dataframe keywords or smth

	# plot
	sns.lineplot(data=dataframe, x=x, y=y)

	# show it
	plt.show()

##################
# start analysis #
##################
# ch1 = voltage (uV = Ve-06)

# display raw data
#intern_plot(raw_df)

#timestamp_delta = None
#for i in range(idx_min, idx_min+10):
#	old_timestamp_delta = timestamp_delta
#	timestamp_delta = (raw_df['timestamp'][i+1] - raw_df['timestamp'][i])
#	print(timestamp_delta)



###################
# start filtering #
###################

# filter a lil
#scipy.





#sns.relplot(data=df, kind="line", uni);
#sns.lineplot(data=df, x='', '')











