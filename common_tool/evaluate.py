import numpy as np 
import math

def open_file(path):
  t=[]
  pose = []
  with open(path, 'r') as f:
    for line in f.readlines():
      line_str = line.split()
      if(len(line_str)==13):
        t.append(float(line_str[0]))
        line_str.pop(0)
        pose.append([float(x) for x in line_str])
  return t,pose

if __name__ == '__main__':
  #test RMSE:0.034591
  e_t,e_pose = open_file("/home/yiluzhang/experiment/vins/camera/kinect2/paper/lab_rectangle/vies_pose.txt")
  v_t,v_pose = open_file("/home/yiluzhang/experiment/vins/camera/kinect2/paper/lab_rectangle/vins_pose.txt")

  e_len = len(e_t)
  v_len = len(v_t)
  
  e_cnt = 0
  v_cnt = 0
  error_sum = 0.0
  sum_cnt = 0
  first_equal = 0
  rat_0 = np.zeros([3,3],dtype = float)
  trans_0 = np.zeros([3,1],dtype = float)
  print(v_len,e_len)
  while v_cnt < v_len:
    #print(v_cnt,e_cnt)
    if e_cnt == e_len:
      break; 
    while e_cnt < e_len:
      if v_t[v_cnt] == e_t[e_cnt]:
      #if math.fabs(v_t[v_cnt] - e_t[e_cnt])<0.035:
        if(first_equal == 0):
          e_rat = np.array(e_pose[e_cnt][3:12]).reshape(3,3)
          e_rat = np.transpose(e_rat)
          e_trans = -np.dot(e_rat,np.array(e_pose[e_cnt][0:3]).reshape(3,1))
          v_rat = np.array(v_pose[v_cnt][3:12]).reshape(3,3)
          v_rat = e_rat
          v_rat = np.transpose(v_rat)
          v_trans = -np.dot(v_rat,np.array(v_pose[v_cnt][0:3]).reshape(3,1))
          rat_0 = np.dot(e_rat, v_rat)
          trans_0 = np.dot(e_rat,v_trans)+e_trans
          first_equal=1
          v_cnt = v_cnt+1
          e_cnt = e_cnt+1
          break;
        else:
          tmp_e_rat = np.array(e_pose[e_cnt][3:12]).reshape(3,3)
          tmp_e_trans = np.array(e_pose[e_cnt][0:3]).reshape(3,1)
          tmp_v_rat = np.array(v_pose[v_cnt][3:12]).reshape(3,3)
          tmp_v_trans = np.array(v_pose[v_cnt][0:3]).reshape(3,1)
          tmp_trans = np.dot(np.dot(tmp_e_rat, rat_0),tmp_v_trans)+np.dot(tmp_e_rat, trans_0)+tmp_e_trans
          error_sum = error_sum + np.vdot(tmp_trans,tmp_trans)
          sum_cnt = sum_cnt+1
          v_cnt = v_cnt+1
          e_cnt = e_cnt+1
          break;
      elif v_t[v_cnt] >= e_t[e_cnt]:
        e_cnt = e_cnt+1
        break;
      else:
        #print('1')
        v_cnt = v_cnt+1
        break;

  print("The count is:",sum_cnt)
  print("The RMSE is:",math.sqrt(error_sum/sum_cnt))
  

  
