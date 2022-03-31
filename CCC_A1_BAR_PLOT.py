#!/usr/bin/env python
# coding: utf-8

# In[41]:



import numpy as np
import matplotlib.pyplot as plt

#transfering minutes to seconds
n11c = 6.15*60
n18c = 3.03*60
n28c = 3.01*60
# creating the dataset
data = {'1node_1core':n11c, '1nodes_8cores':n18c, '2nodes_8cores':n28c}
courses = list(data.keys())
values = list(data.values())
  
fig = plt.figure(figsize = (10,5))
 
#showing the plot
plt.bar(courses, values, color ='lightskyblue',
        width = 0.5)
  

plt.xlabel("#nodes&#cores")
plt.ylabel("Time for execution (second)")
plt.title("Bar plot of the time for execution")
plt.show()
plt.savefig('time_for_execution_bar_plot.png')

