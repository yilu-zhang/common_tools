import numpy as np 
from matplotlib import pyplot as plt
import sys 

def open_t_file(path):
  t=[]
  with open(path, 'r') as f:
    for line in f.readlines():
      #print("test 1")
      line_str = line.split()
      if(len(line_str)==8):
        #print("test 2")
        t.append(float(line_str[0][6:]))
  return t
       
if __name__=='__main__':
  # t
  # file_name = "/home/yiluzhang/Desktop/experiment/carto/traj_1/3/reloc.txt"
  file_name = sys.argv[1]
  plt_save_name = file_name[0:file_name.rfind('.')]+"_evo.png"
  file_save_name = file_name[0:file_name.rfind('.')] + "_evo.txt"
  with open(file_save_name, 'w') as f:
    pass
  print("the file name is: " + file_name)
  print("the plt save name is: " + plt_save_name)
  print("the file save name is: " + file_save_name)
  t =  open_t_file(file_name)

  t0=t[0]
  t_sum = t[-1] - t[0]
  correct_t = [x-t0 for x in t]

  delta_t = []
  delta_t_sum = 0.0
  delta_t_cnt = 0
  t1 = t[0]
  for x in t:
    delta_t_tmp = x - t1
    if delta_t_tmp > 2:
      with open(file_save_name, 'a') as f:
        f.write("the delta t in " + str(x) + " is: " + str(delta_t_tmp) + '\n')
      print("the delta t in " + str(x) + " is: " + str(delta_t_tmp))
    if delta_t_tmp <= 2:
      delta_t_sum = delta_t_sum + delta_t_tmp
      delta_t_cnt = delta_t_cnt + 1
    if(delta_t_tmp > 20):
      delta_t_tmp = 25
    delta_t.append(delta_t_tmp)
    t1  = x
  
  if(delta_t_cnt > 0):
    print("Successs rate s/s: " + str(delta_t_sum) + "/" + str(t_sum) + ' = ' + str(100*delta_t_sum/t_sum) + '%')
    print("Frequency is: " + str(delta_t_cnt/delta_t_sum) + " HZ")
    with open(file_save_name, 'a') as f:
      f.write("Successs rate s/s=: " + str(delta_t_sum) + "/" + str(t_sum) + ' = ' + str(100*delta_t_sum/t_sum) + '%\n')
      f.write("Frequency is: " + str(delta_t_cnt/delta_t_sum) + " HZ" + '\n')
    #print(delta_t_cnt/delta_t_sum)
  x1 = np.array(correct_t)
  y1 =  np.array(delta_t)

  '''#plt.title("velocity") 
  #plt.xlabel("t [s]") 
  #plt.ylabel("x [m/s]") 
  x1 = []
  x2 = []
  y1 = []
  y2 = []
  y3 = []
  plt.plot(x1,y1,color='r',linewidth=1.0,linestyle="-",label="Ground Truth",alpha = 1)
  plt.plot(x1,y2,color='b',linewidth=1.0,linestyle="-",label="Proposed",alpha = 1)
  plt.plot(x2,y3,color='k',linewidth=1.0,linestyle="-",label="VINS-Mono",alpha = 1)
  plt.legend(loc="center")
  plt.show()'''


  plt.subplot(1,1,1)
  plt.title("delta t") 
  plt.xlabel("t [s]") 
  plt.ylabel("delta_t [s]") 
  plt.plot(x1,y1,color='r',linewidth=1.0,linestyle="-",alpha = 1)
  #plt.legend(loc="lower center")
  #plt.legend(loc="lower right")
  # plt.legend(loc="upper left")
  plt.savefig(plt_save_name)
  plt.show()

  '''
  plt.subplot(3,1,2)
  y4 =  np.array(e_vel_y)
  y5 =  np.array(vel_y)
  y6 =  np.array(v_vel_y)
  #plt.title("velocity") 
  #plt.xlabel("t [s]") 
  plt.ylabel("y [m/s]") 
  plt.plot(x1,y4,color='r',linewidth=1.0,linestyle="-",label="Ground Truth",alpha = 1)
  plt.plot(x1,y5,color='b',linewidth=0.5,linestyle="--",label="Proposed",alpha = 1)
  plt.plot(x2,y6,color='k',linewidth=0.5,linestyle="-.",label="VINS-Mono",alpha = 1)
  #plt.legend(loc="lower center")
  #plt.show()

  plt.subplot(3,1,3)
  y7 =  np.array(e_vel_z)
  y8 =  np.array(vel_z)
  y9 =  np.array(v_vel_z)
  #plt.title("velocity") 
  plt.xlabel("t [s]") 
  plt.ylabel("z [m/s]") 
  plt.plot(x1,y7,color='r',linewidth=1.0,linestyle="-",label="Ground Truth",alpha = 1)
  plt.plot(x1,y8,color='b',linewidth=0.5,linestyle="--",label="Proposed",alpha = 1)
  plt.plot(x2,y9,color='k',linewidth=0.5,linestyle="-.",label="VINS-Mono",alpha = 1)
  plt.legend(loc="upper right")
  plt.show()'''


