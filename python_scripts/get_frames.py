import os
import sys
import glob
import numpy as np
import numpy as np
from numpy.lib.stride_tricks import as_strided
import gzip
import pickle
from PIL import Image
from keras.preprocessing.image import array_to_img,img_to_array


PATH_DATA = '../dataset/'

def get_dataset_number_frames(data_path=PATH_DATA):
	"""
	Example of use:
	gf.get_dataset_number_frames()

	return :
	{'../dataset/CLEAR/0/1496613715': 336,
	 '../dataset/CLEAR/12/1496614075': 353,	
    ...
    }

	"""	
	dict_path = {}
	weathers = os.listdir(PATH_DATA)
	for weather in weathers:
		if 'desktop.ini' not in weather:
			for hour in os.listdir(PATH_DATA+weather):
				for timestamp in os.listdir(PATH_DATA+weather+'/'+hour):
					_max = np.max([int(f[:-3]) for f in os.listdir(PATH_DATA+weather+'/'+hour+'/'+timestamp)])
					dict_path[PATH_DATA+weather+'/'+hour+'/'+timestamp] = _max
	return dict_path

def get_path_to_frames(dataset_frames,key):
	"""
	Example of use:
	gf.get_path_to_frames(dataset_number_frames,'../dataset/EXTRASUNNY/12/1496614796')

	return :
	['../dataset/EXTRASUNNY/12/1496614796/1.pz',
	 '../dataset/EXTRASUNNY/12/1496614796/2.pz',
	 '../dataset/EXTRASUNNY/12/1496614796/3.pz',
	 '../dataset/EXTRASUNNY/12/1496614796/4.pz',
	 ...
	]
    """
	return [key+'/'+str(i)+'.pz' for i in range(1,dataset_frames[key]) if os.path.exists(key+'/'+str(i)+'.pz')]


def frame2numpy(frame, frameSize):
	"""
	Example of use:
	frame2numpy(frame['frame'],frameSize=frameSize)

	return :
    numpy array of the images in the format : (heigth, width, 3)
	"""	
	buff = np.fromstring(frame, dtype='uint8')
	# Scanlines are aligned to 4 bytes in Windows bitmaps
	strideWidth = int((frameSize[0] * 3 + 3) / 4) * 4
	# Return a copy because custom strides are not supported by OpenCV.
	return as_strided(buff, strides=(strideWidth, 3, 1), shape=(frameSize[1], frameSize[0], 3)).copy()

def load_image(path,frameSize=(1280,640)):
	"""
	Example of use:
	gf.load_image(path)

	return :
    numpy array of the images in the format : (heigth, width, 3)
	"""	
	f = gzip.open(path, 'rb')
	frame = pickle.load(f)
	return frame2numpy(frame['frame'],frameSize=frameSize)

def get_frame(path,frameSize=(1280,640),dict_keys=['frame','speed','throttle','steering','brake'],active=False):
	"""
	Example of use:
	gf.get_frame(path) :
	return the obj as a dict


	gf.get_frame(path,active=True) :
	return the obj as a filtered dict with dict_keys keys.

	"""	
	f = gzip.open(path, 'rb')
	frame = pickle.load(f)
	frame['frame'] = frame2numpy(frame['frame'],frameSize=frameSize)
	if active == True:
		out = {}
		for key in dict_keys:
			out[key] = frame[key]
		return out
	return frame

def create_paths(path,indexes,shitf=False):
	"""
	Example of use:
	gf.create_paths(self._path,index_array,True)

	return paths ordered for the generator
	"""	
	if shitf:
		return [path+'/'+str(i+1)+'.pz' for i in indexes if os.path.exists(path+'/'+str(i)+'.pz')]
	else:
		return [path+'/'+str(i)+'.pz' for i in indexes if os.path.exists(path+'/'+str(i)+'.pz')]


def load_data_from_paths(paths,select=False):
	"""
	Example of use:
	gf.load_data_from_paths(paths)

	return data . Those data can be selected if select=True
	"""	
	data = []
	if not select:
		for path in paths:
			data.append(get_frame(path))
	else:
		for path in paths:
			data.append(get_frame(path,active=True))		
	return data

def extract_map(img):
	height,width,channel = img.shape
	print(height,width,channel)
	p_width = [0.03*width,0.16*width]
	p_height = [0.85*height,.99*height]
	img = array_to_img(img)
	img = img.crop((p_width[0],p_height[0],p_width[1],p_height[1]))
	return img_to_array(img)




