import numpy as np 
from matplotlib import pyplot as plt 

def open_e_file(path):
  t=[]
  e_vel_x = []
  e_vel_y = []
  e_vel_z = []
  vel_x = []
  vel_y = []
  vel_z = []
  with open(path, 'r') as f:
    for line in f.readlines():
      line_str = line.split()
      if(len(line_str)==7):
        t.append(float(line_str[0]))
        e_vel_x.append(float(line_str[1]))
        e_vel_y.append(float(line_str[2]))
        e_vel_z.append(float(line_str[3]))
        vel_x.append(float(line_str[4]))
        vel_y.append(float(line_str[5]))
        vel_z.append(float(line_str[6]))
  return t,e_vel_x,e_vel_y,e_vel_z,vel_x,vel_y,vel_z

def open_v_file(path):
  t=[]
  v_vel_x = []
  v_vel_y = []
  v_vel_z = []
  with open(path, 'r') as f:
    for line in f.readlines():
      line_str = line.split()
      if(len(line_str)==4):
        t.append(float(line_str[0]))
        v_vel_x.append(float(line_str[1]))
        v_vel_y.append(float(line_str[2]))
        v_vel_z.append(float(line_str[3]))
  return t,v_vel_x,v_vel_y,v_vel_z
        

if __name__=='__main__':
  # lab_circle1/static_start
  #t_e,e_vel_x,e_vel_y,e_vel_z,vel_x,vel_y,vel_z =  open_e_file("/home/yiluzhang/experiment/vins/camera/kinect2/paper/lab_circle1/static_start/vies_vel.txt")
  #t_v,v_vel_x,v_vel_y,v_vel_z =  open_v_file("/home/yiluzhang/experiment/vins/camera/kinect2/paper/lab_circle1/static_start/vins_vel.txt")

  # lab_circle1/circle_start
  #t_e,e_vel_x,e_vel_y,e_vel_z,vel_x,vel_y,vel_z =  open_e_file("/home/yiluzhang/experiment/vins/camera/kinect2/paper/lab_circle1/circle_start/vies_vel.txt")
  #t_v,v_vel_x,v_vel_y,v_vel_z =  open_v_file("/home/yiluzhang/experiment/vins/camera/kinect2/paper/lab_circle1/circle_start/vins_vel.txt")

  # lab_circle2
  #t_e,e_vel_x,e_vel_y,e_vel_z,vel_x,vel_y,vel_z =  open_e_file("/home/yiluzhang/experiment/vins/camera/kinect2/paper/lab_circle2/vies_vel.txt")
  #t_v,v_vel_x,v_vel_y,v_vel_z =  open_v_file("/home/yiluzhang/experiment/vins/camera/kinect2/paper/lab_circle2/vins_vel.txt")

  # lab_rectangle
  t_e,e_vel_x,e_vel_y,e_vel_z,vel_x,vel_y,vel_z =  open_e_file("/home/yiluzhang/experiment/vins/camera/kinect2/paper/lab_rectangle/vies_vel.txt")
  t_v,v_vel_x,v_vel_y,v_vel_z =  open_v_file("/home/yiluzhang/experiment/vins/camera/kinect2/paper/lab_rectangle/vins_vel.txt")

  

  t0=t_e[0]
  correct_t_e = [x-t0 for x in t_e]
  correct_t_v = [x-t0 for x in t_v]

  x1 = np.array(correct_t_e)
  x2 = np.array(correct_t_v) 
  y1 =  np.array(e_vel_x)
  y2 =  np.array(vel_x)
  y3 =  np.array(v_vel_x)

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


  plt.subplot(3,1,1)
  plt.title("velocity") 
  #plt.xlabel("t [s]") 
  plt.ylabel("x [m/s]") 
  plt.plot(x1,y1,color='r',linewidth=1.0,linestyle="-",label="Ground Truth",alpha = 1)
  plt.plot(x1,y2,color='b',linewidth=0.5,linestyle="--",label="Proposed",alpha = 1)
  plt.plot(x2,y3,color='k',linewidth=0.5,linestyle="-.",label="VINS-Mono",alpha = 1)
  #plt.legend(loc="lower center")
  #plt.legend(loc="lower right")
  #plt.legend(loc="upper center")
  #plt.show()

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
  plt.show()


