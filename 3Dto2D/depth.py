import os
import sys
import numpy as np
import cv2
import json

# 提取房间高度参数，只能提取1-3层
high_list=[1.8,2.0,2.1] #输出几个高度的平面图 单位米
#每个高度取的阈值 如高度为1.5,阈值0.25时取得1.5-0.25到1.5+0.25米点云做输出
high_thre = 0.2

# 深度相机参数
cx = 314.5
cy = 235.5
fx = 570.3422241210938
fy = 570.3422241210938
depth_scale = 1000.0

camera_pitch = -7.18*np.pi/180.0 # 仰视为正
camera_height = 1.48 # 相机高度

# 输出2D图分辨率
image_width = 640
image_height = 480

def getdict(filename=None):
    '''
    输入json文件名
    返回字典对象
    '''
    try:
        if filename:
            f=open(filename)
            dic=json.load(f)
            return dic
        else:
            return{}
    except Exception as e:
        print('getdict error',e)
        return {}

# 通过相机的camera_pitch得到从相机坐标系到xy平面与地面平行坐标系的旋转矩阵
def pitch_to_Rpc(pitch):
    R_pc = np.zeros((3,3))
    R_pc[0][0] = 1.0
    R_pc[1][1] = np.cos(pitch)
    R_pc[1][2] = -np.sin(pitch)
    R_pc[2][1] = np.sin(pitch)
    R_pc[2][2] = np.cos(pitch)
    return R_pc


# 通过航向角theta得到从xy平面与地面平行坐标系到世界坐标系的旋转矩阵R_wp
def raw_to_Rwp(theta):
    R_wp = np.zeros((3,3))
    R_wp[0][0] = np.cos(theta)
    R_wp[0][1] = -np.sin(theta)
    R_wp[1][0] = np.sin(theta)
    R_wp[1][1] = np.cos(theta)
    R_wp[2][2] = 1
    return R_wp

# 将xy平面与地面平行坐标系的点p_p转换成世界坐标系的点p_w
def tf(R_wp,x,y,p_p):
    #print('坐标转换')  
    t_wp = np.array([x,y,camera_height])
    p_w = np.add(np.dot(R_wp,p_p),t_wp)
    return list(p_w)


def get_depth_file_and_process(filename,R_pc,theta,x,y):
    #读入cv或numpy
    img=cv2.imread(filename,cv2.IMREAD_ANYDEPTH)
    pointdata_k = []
    R_wp = raw_to_Rwp(theta)
    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            depth = img[row,col]
            
            if depth >= 10 and depth <= 60000:
                p_c = []
                depth = depth/depth_scale
                # 相机坐标系：y轴对应深度方向，x轴与地面平行
                # p_c为相机坐标系点云               
                p_c.append((col-cx)*depth/fx)   # x            
                p_c.append(depth)              # z
                p_c.append((cy-row)*depth/fy)   # -y

                # 将相机坐标系点云转换到xy平面与地面平行的坐标系点云p_p
                p_p = np.dot(R_pc,np.array(p_c)) 

                p_w = tf(R_wp,x,y,p_p)
                pointdata_k.append(p_w)
    return pointdata_k


def createdepthfile(inputfile,outputpath=None):
    _dic=getdict(inputfile)
    _R_pc = pitch_to_Rpc(camera_pitch)
    if len(_dic)>0:
        pointdata=[]#伪代码
        img_cnt = 0
        for k,v in _dic.items():
            #print('k:%s,v: %s'%(k,v))
            _x,_y=k.split('_')
            _x = float(_x)
            _y = float(_y)
            
            for _k,_v in v.items():
                img_cnt = img_cnt + 1
                print("process image %d"%(img_cnt))
                _theta=float(_k)
                #_x _y _theta 就是当前点云数据的坐标和航向
                #print('depthfile=',_v)
                #print('x=%s,y=%s,theta=%s'%(_x,_y,_theta))
                #_data就是对应的位姿观察的世界坐标系的点云
                #点云转换到世界坐标系，增加到文件（列表）中
                _data = get_depth_file_and_process(_v,_R_pc,_theta,_x,_y)
                pointdata.append(_data)               
                
            #print(len(pointdata))
            #points_num = 0
            #for img_points in pointdata:
                #points_num = points_num + len(img_points)
            #print(points_num)

            num_2D_img = len(high_list)
            layer_max_x=[float("-inf")]*num_2D_img
            layer_min_x=[float("inf")]*num_2D_img
            layer_max_y=[float("-inf")]*num_2D_img
            layer_min_y=[float("inf")]*num_2D_img
            point_2D = {}
            for i in range(num_2D_img):
                point_2D[i]=[]
            #print(len(layer_max_x))

            for img_points in pointdata:
                for point_w in img_points:
                    for i in range(num_2D_img):                       
                        if point_w[2]>=high_list[i] and point_w[2]<=(high_list[i]+high_thre):
                            if(point_w[0]>layer_max_x[i]):
                                layer_max_x[i]=point_w[0]
                            if(point_w[0]<layer_min_x[i]):
                                layer_min_x[i]=point_w[0]
                            if(point_w[1]>layer_max_y[i]):
                                layer_max_y[i]=point_w[1]
                            if(point_w[1]<layer_min_y[i]):
                                layer_min_y[i]=point_w[1]
                            point_2D[i].append([point_w[0],point_w[1]])

        #如果outputpath is None 则输出到当前目录，否则输出到制定目录路
        if(outputpath==None):    
            path = ""   
        else:
            path = outputpath       
        img_out=np.zeros((image_height,image_width,3),dtype=np.uint8) # BGR
        img_out[:,:,:]=255
        min_scale_factor = []
        for i in range(num_2D_img):
            detal_x = layer_max_x[i] - layer_min_x[i]
            detal_y = layer_max_y[i] - layer_min_y[i]
            min_scale_factor.append(min((img_out.shape[1]-100)/detal_x,(img_out.shape[0]-100)/detal_y))
        scale_factor = min(min_scale_factor)
        max_y = max(layer_max_y)
        min_x = min(layer_min_x)
                            
        # print(scale_factor)
        for i in range(num_2D_img):
            for point in point_2D[i]:
                img_out[int(scale_factor*(max_y-point[1]))+50,int(scale_factor*(point[0]-min_x))+50,i] = 0
                
        path1 = path + str(scale_factor) + "_" + str(min_x) + "_" + str(max_y) +"_"+str(num_2D_img)+"_"+str(high_thre)
        for i in range(num_2D_img):
            path1 = path1 + "_" + str(high_list[i])
        path1 = path1 + ".jpg"
        print('The path of output image is:%s'%(path1))
        cv2.imwrite(path1,img_out)
                
    else:
        print('len of dic is 0')


def test(args):
    print('args',args)
    if len(args)>2:
        createdepthfile(args[1],args[2])
    elif len(args)>1:
        createdepthfile(args[1])
    else:
        print('args error')

if __name__=='__main__':
    print('''
            ---demo---
            python3 depth.py [inputpath][outputpath]
            ''')
    test(sys.argv)
    pass

