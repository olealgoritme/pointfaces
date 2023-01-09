## Code is based on "Arun et al., 1987"
## -Ole Algoritme 2022-
import open3d as o3d
import numpy as np

## for our use case:
## pcd_src_file - the point cloud file containing captured facial landmarks
## pcd_dst_file - the point cloud file containing the canonical facial landmarks
class TransferCorrection:
  def __init__(self, pcd_src_file, pcd_dst_file, scale):
    self.pcd_src_file = pcd_src_file
    self.pcd_dst_file = pcd_dst_file
    self.scale = scale

  def apply(self):
    #Writing points with rows as the coordinates
    pcd_src = o3d.io.read_point_cloud(self.pcd_src_file)
    p1_t = np.asarray(pcd_src.points)
    pcd_dst = o3d.io.read_point_cloud(self.pcd_dst_file)
    p2_t = np.asarray(pcd_dst.points)

    #Take transpose as columns should be the points
    p1 = p1_t.transpose()
    p2 = p2_t.transpose()

    #Calculate centroids
    p1_c = np.mean(p1, axis = 1).reshape((-1,1)) #If you don't put reshape then the outcome is 1D with no rows/colums and is interpeted as rowvector in next minus operation, while it should be a column vector
    p2_c = np.mean(p2, axis = 1).reshape((-1,1))

    #Subtract centroids
    q1 = p1-p1_c
    q2 = p2-p2_c

    #Calculate covariance matrix
    H=np.matmul(q1,q2.transpose())

    #Calculate singular value decomposition (SVD)
    U, _, V_t = np.linalg.svd(H) #the SVD of linalg gives you Vt

    #Calculate rotation matrix
    R = np.matmul(V_t.transpose(),U.transpose())

    assert np.allclose(np.linalg.det(R), 1.0), "Rotation matrix of N-point registration not 1, see Arun et al. 1987"

    #Calculate translation matrix
    T = p2_c - np.matmul(R,p1_c)

    # picking the center as the 5th index of pcd_src
    src_center = pcd_src.points[5]

    #pcd_src.scale(self.scale, center=(src_center))
    pcd_src.rotate(R, center=(src_center))
    pcd_src.translate(T)
    return pcd_src
