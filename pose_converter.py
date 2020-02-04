import numpy as np

def q_conjugate(quat):
    q = quat.copy()
    q = q * np.sqrt(1.0 / np.dot(q, q))
    i = 1
    while (i < 4):
        q[i] = -q[i]
        i=i+1
    return q

def q_inverse(quat):
    q = quat.copy()
    q = q * np.sqrt(1.0 / np.dot(q,q))
    return q_conjugate(q)

def quat_mutiply_quat(quat1,quat2):
    q1 = quat1.copy()
    q2 = quat2.copy()
    q = np.array([q1[0]*q2[0]-q1[1]*q2[1]-q1[2]*q2[2]-q1[3]*q2[3],
                 q1[0]*q2[1]+q1[1]*q2[0]+q1[2]*q2[3]-q1[3]*q2[2],
                 q1[0]*q2[2]-q1[1]*q2[3]+q1[2]*q2[0]+q1[3]*q2[1],
                 q1[0]*q2[3]+q1[1]*q2[2]-q1[2]*q2[1]+q1[3]*q2[0]],
                 dtype=q1.dtype)
    print(q)
    return (q * np.sqrt(1.0 / np.dot(q,q)))


def quaternion_to_rotation_matrix(quat):
  q = quat.copy()
  n = np.dot(q, q)
  #print(n)
  if n < np.finfo(q.dtype).eps:
    return np.identity(4)
  q = q * np.sqrt(2.0 / n) # ||q||=1,使q模为1，这里取2方便计算R
  #print(np.dot(q,q))
  q = np.outer(q, q)
  #print(q)
  rot_matrix = np.array(
    [[1.0 - q[2, 2] - q[3, 3], q[1, 2] + q[3, 0], q[1, 3] - q[2, 0], 0.0],
     [q[1, 2] - q[3, 0], 1.0 - q[1, 1] - q[3, 3], q[2, 3] + q[1, 0], 0.0],
     [q[1, 3] + q[2, 0], q[2, 3] - q[1, 0], 1.0 - q[1, 1] - q[2, 2], 0.0],
     [0.0, 0.0, 0.0, 1.0]],
    dtype=q.dtype)
  return rot_matrix