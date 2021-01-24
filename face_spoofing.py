import numpy as np
import cv2


def calc_hist(img):
    histogram = [0] * 3
    for j in range(3):
        histr = cv2.calcHist([img], [j], None, [256], [0, 256])
        histr *= 255.0 / histr.max()
        histogram[j] = histr
    return np.array(histogram)


def run_face_spoof(img, ret, find_faces, clf, face_model):
    if not ret:
        return
    sample_number = 1
    count = 0
    measures = np.zeros(sample_number, dtype=np.float)
    faces = find_faces(img, face_model)

    measures[count % sample_number] = 0
    spoofed = []
    for x, y, x1, y1 in faces:

        roi = img[y:y1, x:x1]

        img_ycrcb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB)
        img_luv = cv2.cvtColor(roi, cv2.COLOR_BGR2LUV)

        ycrcb_hist = calc_hist(img_ycrcb)
        luv_hist = calc_hist(img_luv)

        feature_vector = np.append(ycrcb_hist.ravel(), luv_hist.ravel())
        feature_vector = feature_vector.reshape(1, len(feature_vector))

        prediction = clf.predict_proba(feature_vector)
        prob = prediction[0][1]

        measures[count % sample_number] = prob

        if 0 not in measures:
            if np.mean(measures) >= 0.7:
                spoofed.append(False)
            else:
                spoofed.append(True)
    count += 1
    return spoofed
