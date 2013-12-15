#!/usr/bin/env python

import sys, os
import SimpleITK as sitk
import cv2

from scipy.stats.mstats import mquantiles

size = int(sys.argv[1])
input = sys.argv[2]
output = sys.argv[3]

img = sitk.ReadImage(input)
data = sitk.GetArrayFromImage( img ).astype("float")

if len(data.shape) not in [2,3] :
    exit(1)
    
## Contrast-stretch with saturation
q = mquantiles(data.flatten(),[0.01,0.99])
if q[1] > q[0]: # no error for constant intensity images
    data[data<q[0]] = q[0]
    data[data>q[1]] = q[1]
data -= data.min()
data /= data.max()
data *= 255
data = data.astype('uint8')

if len(data.shape) == 3:
    data = data[data.shape[0]/2,:,:,]

if data.shape[0] < data.shape[1]:
    new_size = (size, (data.shape[0]*size)/data.shape[1])
else:
    new_size = (data.shape[1]*size/data.shape[0], size)

thumbnail = cv2.resize( data,new_size)

cv2.imwrite(output+".png",thumbnail)
os.rename(output+".png",output)

