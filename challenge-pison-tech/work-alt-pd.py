import scipy
import scipy.fft
import scipy.signal
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

IN_FILE = './intern_set.csv'
C1 = 'ch1'
C2 = 'timestamp'

#sns.set_theme(style="whitegrid", palette="rocket")
#sns.set_theme(style="whitegrid")
sns.set_theme()
def plott(df: pd.DataFrame, x:str, y:str, xname:str = '', yname:str = '') -> None:
	f = sns.lineplot(data=df, x=x, y=y)
	#if xname:
	#	f.set(xlabel=xname)
	#if yname:
	#	f.set(ylabel=yname)
	plt.show()

# import csv with pandas
INPUT_FILE="./intern_set.csv"
df = pd.read_csv(INPUT_FILE, usecols=[C1, C2])

plott(df, x=C2, y=C1)

# resample signal to fix rampant oversampling.
unique_timestamps = len(np.unique(df['timestamp']))
arr = scipy.signal.resample(df, unique_timestamps)


# compute fft

