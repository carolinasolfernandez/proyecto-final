import numpy as np
from pykalman import KalmanFilter

'''
NO SE USA - NO FUNCIONA. 
'''

obj_detection = [
    (1, 1, [10, 20]),
    (3, 1, [30, 40]),
    (4, 1, [50, 60]),
]

interpolated_detections = []

for i in range(1, len(obj_detection)):
    curr_frame, obj_id, curr_measurement = obj_detection[i]
    prev_frame, _, prev_measurement = obj_detection[i-1]
    num_interpolated_frames = curr_frame - prev_frame - 1
    if num_interpolated_frames > 0:
        measurement_covariance = np.array([[1, 0], [0, 1]])
        kf = KalmanFilter(transition_matrices=[[1, 1], [0, 1]], observation_matrices=[[1, 0]],
                          transition_covariance=0.01 * np.eye(2), observation_covariance=measurement_covariance)
        (filtered_state_means, filtered_state_covariances) = kf.filter(prev_measurement)
        for j in range(num_interpolated_frames):
            interpolated_detection = kf.filter_update(filtered_state_means[-1], filtered_state_covariances[-1], 
                                                      curr_measurement)
            interpolated_detections.append((prev_frame + j + 1, obj_id, interpolated_detection[0]))

for i in obj_detection:
    interpolated_detections.append(i)

print(interpolated_detections)