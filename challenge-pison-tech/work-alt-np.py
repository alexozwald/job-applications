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
xdef = 'timestamp (s)'
ydef = ''
def plott(arr: np.ndarray, x: str =C1, y: str =C1, *, xname:str=xdef, yname:str=ydef) -> None:
	#fig = sns.lineplot(data=arr, x=x, y=y)
	f = sns.lineplot(x=arr[:,0], y=arr[:,1])
	f.set(xlabel=xname, ylabel=yname)
	plt.show()

# import csv with pandas
INPUT_FILE="./intern_set.csv"
df = pd.read_csv(INPUT_FILE, usecols=[C1, C2])

# switch to numpy array
arr = np.array(df)
plott(arr, xname='timestamp', yname='volts')

# resample signal to fix rampant oversampling.
unique_timestamps = len(np.unique(arr))
arr = scipy.signal.resample(arr, unique_timestamps)


# compute fft

