import cv2
from face_detector import find_faces
from face_landmarks import detect_marks, draw_marks


def initialize_mouth_model(img, ret, face_model, landmark_model):
    if not ret:
        return
    rects = find_faces(img, face_model)
    shape = None
    for rect in rects:
        shape = detect_marks(img, landmark_model, rect)
        draw_marks(img, shape)
    return img, shape


def run_mouth_open(img, ret, face_model, landmark_model, font, outer_points, d_outer, inner_points, d_inner):

    if not ret:
        return

    rects = find_faces(img, face_model)

    for rect in rects:
        shape = detect_marks(img, landmark_model, rect)
        cnt_outer = 0
        cnt_inner = 0
        for i, (p1, p2) in enumerate(outer_points):
            if d_outer[i] + 3 < shape[p2][1] - shape[p1][1]:
                cnt_outer += 1
        for i, (p1, p2) in enumerate(inner_points):
            if d_inner[i] + 2 <  shape[p2][1] - shape[p1][1]:
                cnt_inner += 1
        if cnt_outer > 3 and cnt_inner > 2:
            return True
    return False
