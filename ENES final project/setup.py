from ast import Continue
from dataclasses import dataclass
from email.mime import image
from setuptools import setup
from lidar import lidar as ld
import dataclasses


data = dataclasses
road = image 
space = ld [data]


ld.setup()
if space > 2:
    print("Keep moving")
    Continue

elif space < 2:
    print ("Stop. Change direction")
    Continue

else: road == image
setup()
