# -*- coding: utf-8 -*-
"""K_mean.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ae4dKAF9ZvjlJMDeI1BiZNPMfO3hbDem
"""

import numpy as np
import matplotlib.pyplot as plt

k = 3
num_iter = 1000

input = np.array([[-1,-1],[1,1],[1,3],[1,4],[-2,-2],[-3,-5],[-1,2],[-3,4],[1,5],[2,6],[1,7]])
print(input)
def random_initialization(k, input):
  while(True):
    centroids_idx = np.random.randint(len(input), size=(k))
    centroids = []
    centroids_idx1 = []
    for i in centroids_idx:
      if i not in centroids_idx1:
        centroids_idx1.append(i)
        centroids.append(input[i])
    if(len(centroids) == k):
      centroids1 = np.array(centroids)
      break
  return centroids1

def update_centroids(k, input):
  old_centroids = random_initialization(k, input)
  for _ in range(0, num_iter):  
    cluster = []
    sum = 0
    mean = []
    counter = 0
    for i in range(0, len(input)):
      min = np.linalg.norm(input[i] - old_centroids[0])
      for j in range(0, k):	
        dist = np.linalg.norm(input[i] - old_centroids[j])
        if(dist <= min):
          min = dist
          min_idx = j
      cluster.append(min_idx)
    for j in range(0, k):
      for i in range(0,len(cluster)):
        if(cluster[i]== j):
          counter += 1
          sum +=input[i]
      mean.append(sum/counter)
    centroids = mean
    old_centroids = centroids  
      
        
  return centroids, cluster
[centroids, cluster] = update_centroids(k , input)
for i in range(0, len(cluster)):
      if(cluster[i] == 0):
        cluster0 = input[i]
        plt.plot(cluster0[0], cluster0[1],'ro')
      if(cluster[i] == 1):
        cluster1 = input[i]
        plt.plot(cluster1[0], cluster1[1],'bo')
      if(cluster[i] == 2):
        cluster2 = input[i]
        plt.plot(cluster2[0], cluster2[1],'go')