import matplotlib.pyplot as plt
import gzip
import numpy as np
import pickle
import locale

locale.getdefaultlocale()

f = gzip.open('\dataset\CLEAR\0\1497985686\0.pz', encoding=locale.getdefaultlocale()[1])
frame = pickle.load(f)

f = np.array(frame)

print(f.shape())