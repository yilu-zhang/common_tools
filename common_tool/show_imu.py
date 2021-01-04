import numpy as np 
from matplotlib import pyplot as plt 

def open_file(path):
  t=[]
  ang_vel_x = []
  ang_vel_y = []
  ang_vel_z = []
  vel_x = []
  vel_y = []
  vel_z = []
  with open(path, 'r') as f:
    for line in f.readlines():
      line_str = line.split()
      if(len(line_str)==7):
        t.append(float(line_str[0]))
        ang_vel_x.append(float(line_str[1]))
        ang_vel_y.append(float(line_str[2]))
        ang_vel_z.append(float(line_str[3]))
        vel_x.append(float(line_str[4]))
        vel_y.append(float(line_str[5]))
        vel_z.append(float(line_str[6]))
  return t,ang_vel_x,ang_vel_y,ang_vel_z,vel_x,vel_y,vel_z


if __name__=='__main__':
  t_e,ang_vel_x,ang_vel_y,ang_vel_z,vel_x,vel_y,vel_z =  open_file("/home/yiluzhang/experiment/vins/camera/kinect2/paper/lab_rectangle/imu_data.txt")
  #t_e,ang_vel_x,ang_vel_y,ang_vel_z,vel_x,vel_y,vel_z =  open_file("/home/yiluzhang/experiment/vins/camera/kinect2/paper/lab_rectangle/vins_imu_data_40_140.txt")

  t0=t_e[0]
  correct_t_e = [x-t0 for x in t_e]

  x = np.array(correct_t_e)
  y1 =  np.array(ang_vel_x)
  y2 =  np.array(ang_vel_y)
  y3 =  np.array(ang_vel_z)
  y4 =  np.array(vel_x)
  y5 =  np.array(vel_y)
  y6 =  np.array(vel_z)

  plt.subplot(3,1,1)
  plt.title("angle velocity") 
  #plt.xlabel("t [s]") 
  plt.ylabel("x [rad/s]") 
  plt.plot(x,y1,color='r',linewidth=0.5,linestyle="-",label="Encoder",alpha = 1)
  #plt.plot(x1,y2,color='b',linewidth=0.5,linestyle="--",label="Our method",alpha = 1)
  #plt.plot(x2,y3,color='k',linewidth=0.5,linestyle="-.",label="VINS-mono",alpha = 1)
  #plt.legend(loc="lower center")
  #plt.show()

  plt.subplot(3,1,2)
  #plt.title("velocity") 
  #plt.xlabel("t [s]") 
  plt.ylabel("y [rad/s]") 
  plt.plot(x,y2,color='r',linewidth=0.5,linestyle="-",label="Encoder",alpha = 1)
  #plt.plot(x1,y5,color='b',linewidth=0.5,linestyle="--",label="Our method",alpha = 1)
  #plt.plot(x2,y6,color='k',linewidth=0.5,linestyle="-.",label="VINS-mono",alpha = 1)
  #plt.legend(loc="lower center")
  #plt.show()

  plt.subplot(3,1,3)
  #plt.title("velocity") 
  plt.xlabel("t [s]") 
  plt.ylabel("z [rad/s]") 
  plt.plot(x,y3,color='r',linewidth=0.5,linestyle="-",label="Encoder",alpha = 1)
  #plt.plot(x1,y8,color='b',linewidth=0.5,linestyle="--",label="Our method",alpha = 1)
  #plt.plot(x2,y9,color='k',linewidth=0.5,linestyle="-.",label="VINS-mono",alpha = 1)
  #plt.legend(loc="upper right")
  plt.show()


  plt.subplot(3,1,1)
  plt.title("linear acceleration") 
  #plt.xlabel("t [s]") 
  plt.ylabel("x [m/s^2]") 
  plt.plot(x,y4,color='r',linewidth=0.5,linestyle="-",label="Encoder",alpha = 1)
  #plt.plot(x1,y2,color='b',linewidth=0.5,linestyle="--",label="Our method",alpha = 1)
  #plt.plot(x2,y3,color='k',linewidth=0.5,linestyle="-.",label="VINS-mono",alpha = 1)
  #plt.legend(loc="lower center")
  #plt.show()

  plt.subplot(3,1,2)
  #plt.title("velocity") 
  #plt.xlabel("t [s]") 
  plt.ylabel("y [m/s^s]") 
  plt.plot(x,y5,color='r',linewidth=0.5,linestyle="-",label="Encoder",alpha = 1)
  #plt.plot(x1,y5,color='b',linewidth=0.5,linestyle="--",label="Our method",alpha = 1)
  #plt.plot(x2,y6,color='k',linewidth=0.5,linestyle="-.",label="VINS-mono",alpha = 1)
  #plt.legend(loc="lower center")
  #plt.show()

  plt.subplot(3,1,3)
  #plt.title("velocity") 
  plt.xlabel("t [s]") 
  plt.ylabel("z [m/s^2]") 
  plt.plot(x,y6,color='r',linewidth=0.5,linestyle="-",label="Encoder",alpha = 1)
  #plt.plot(x1,y8,color='b',linewidth=0.5,linestyle="--",label="Our method",alpha = 1)
  #plt.plot(x2,y9,color='k',linewidth=0.5,linestyle="-.",label="VINS-mono",alpha = 1)
  #plt.legend(loc="upper right")
  plt.show()


