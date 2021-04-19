import psutil
import time
import sys

if __name__=='__main__':
  if len(sys.argv)!=3:
    print("please input right arg")
    sys.exit()
  record_cnt = float(sys.argv[1])*60
  file_name = sys.argv[2]
  print("The data is save to "+file_name)

  memory_list = []
  cpu_list = []
  while record_cnt > 0:
    memory_tmp=psutil.virtual_memory().used/(1024*1024)
    cpu_tmp = psutil.cpu_percent(0)
    memory_list.append(memory_tmp)
    cpu_list.append(cpu_tmp)
    record_cnt = record_cnt - 1
    time.sleep(1)
  #print(memory_list)
  #print(cpu_list)
  with open(file_name, 'w') as f:
    for data in memory_list:
      f.write(str(data)+" ") 
    f.write('\n')
    for data in cpu_list:  
      f.write(str(data)+" ")
