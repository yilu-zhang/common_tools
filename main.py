import pose_converter as pcon
import numpy as np

if __name__=='__main__':
    pose_quat11=np.array([0.0633993,-0.2808802,0.0389721,0.9568532])
    pose_quat12 = np.array([0.0061888, -0.3262824, 0.0056991, 0.9452349])
    pose_quat21 = np.array([0.0006064, -0.0299213, -0.0224097, 0.9993008])
    pose_quat22 = np.array([-0.0739520, -0.0972755, -0.0345085, 0.9919061])
    T12_1 = pcon.quat_mutiply_quat(pose_quat11,pcon.q_inverse(pose_quat12))
    #T12_11 = pcon.quat_mutiply_quat(pose_quat11, pcon.q_inverse(pose_quat12))
    T12_2 = pcon.quat_mutiply_quat(pose_quat21, pcon.q_inverse(pose_quat22))
    print(T12_1)
    print(T12_2)
    #print(pcon.q_inverse(pose_quat))
    pose_mat_1=pcon.quaternion_to_rotation_matrix(T12_1)
    pose_mat_2 = pcon.quaternion_to_rotation_matrix(T12_2)
    print(pose_mat_1)
    print(pose_mat_2)