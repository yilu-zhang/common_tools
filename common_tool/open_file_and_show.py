import numpy as np 
from matplotlib import pyplot as plt 
import sys

def open_file(path):
  memory = []
  cpu = []
 
  with open(path, 'r') as f:
    line_cnt=1
    for line in f.readlines():
      line_str = line.split()
      if(line_cnt==1):
        memory=[float(data) for data in line_str]
      if(line_cnt==2):
        cpu=[float(data) for data in line_str]
      line_cnt = line_cnt + 1        
  return memory,cpu


if __name__=='__main__':
  if len(sys.argv)!=4:
    print("please input right arg")
    sys.exit()
  memory_u,cpu_u =  open_file(sys.argv[1])
  memory_oe,cpu_oe =  open_file(sys.argv[2])
  #print(memory_u)
  #print(cpu_u)
  plt_save_path = sys.argv[3] + "/"
  plt_save_name_m = plt_save_path + "memory_com.png"
  plt_save_name_c = plt_save_path + "cpu_com.png"

  t = range(len(memory_u))
  #print(t)
  
  
  x = np.array(t)
  y1 =  np.array(memory_u)
  y2 =  np.array(memory_oe)
  y3 =  np.array(cpu_u)
  y4 =  np.array(cpu_oe)

  #plt.subplot(1,1,1)
  plt.title("Memory comparision chart") 
  plt.xlabel("t [s]") 
  plt.ylabel("Memory [MB]") 
  plt.plot(x,y1,color='r',linewidth=0.5,linestyle="-",label="Ubuntu",alpha = 1)
  plt.plot(x,y2,color='b',linewidth=0.5,linestyle="-",label="OpenEuler",alpha = 1)
  plt.legend(loc="lower center")
  plt.savefig(plt_save_name_m)
  plt.show()

  #plt.subplot(1,1,1)
  plt.title("CPU comparision chart") 
  plt.xlabel("t [s]") 
  plt.ylabel("CPU [%]") 
  plt.plot(x,y3,color='r',linewidth=0.5,linestyle="-",label="Ubuntu",alpha = 1)
  plt.plot(x,y4,color='b',linewidth=0.5,linestyle="-",label="OpenEuler",alpha = 1)
  plt.legend(loc="upper center")
  plt.savefig(plt_save_name_c)
  plt.show()

