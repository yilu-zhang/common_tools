import numpy as np 
from matplotlib import pyplot as plt
import sys 
       
if __name__=='__main__':
#  x = range(0,8,0.05)
  x=np.linspace(0.0, 8.0, 161)
  y1 = []
  y2 = []
  y3 = []
  a_f = 0.1
  a_s = 0.03
  for i in x:
    if i < 2:
      y1.append(0)
      y2.append(0)
      y3.append(0)
    elif i < 4:
      y1.append(254)
      y2.append((1-a_f)*y2[-1]+a_f*254)
      y3.append((1-a_s)*y3[-1]+a_s*254)
    else:
      y1.append(0)
      y2.append((1-a_f)*y2[-1])
      y3.append((1-a_s)*y3[-1])

  y1 = np.array(y1)
  y2 = np.array(y2)
  y3 = np.array(y3)
  plt.subplot(1,1,1)
  # plt.title("delta t") 
  plt.xlabel("Time [s]") 
  plt.ylabel("Value") 
  plt.plot(x,y1,color='gray',linewidth=1.0,linestyle="--",label="C",alpha = 1)
  #plt.plot(x,y2,color='b',linewidth=1.0,linestyle="0",label="Pf",alpha = 1)
  #plt.plot(x,y3,color='g',linewidth=1.0,linestyle="-",label="Ps",alpha = 1)
  plt.scatter(x,y2,color='r',linewidth=1.0,s=3.0,label="  ",alpha = 1)
  plt.scatter(x,y3,color='b',linewidth=1.0,s=3.0,label="  ",alpha = 1)
  #plt.legend(loc="lower center")
  #plt.legend(loc="lower right")
  plt.legend(loc="upper right")
  #plt.savefig(plt_save_name)
  plt.show()

