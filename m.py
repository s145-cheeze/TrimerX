# -*- coding: utf-8 -*-
import os
from functools import cmp_to_key
import numpy as np
import cv2


SRC_DIR = 'src'
DST_DIR = 'dst'


def apply_adaptive_threshold(image, radius=15, C=5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 2 * radius + 1, C)


def find_external_contours(thresh):
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    external_num = hierarchy.shape[1] if hierarchy is not None else 0
    return contours[0:external_num]


def extract_rects_from_controus(contours, min_perimeter, max_perimeter):
    frames = []
    for contour in contours:
        frame = cv2.minAreaRect(contour)
        center, size, angle = frame
        # 縦・横が逆になっている場合、90度回転させる
        if angle < -45:
            size = tuple(reversed(size))
            angle = angle + 90
        w, h = size
        perimeter = 2 * (w + h)
        if min_perimeter < perimeter < max_perimeter and abs(angle) < 3.0 and 0.1 <= min(w, h) / max(w, h) <= 1.0:
            frames.append((center, (w + 2, h + 2), angle))  # パディングを加える
    return frames


def cmp_frame(tolerance):
    def _cmp(lhs, rhs):
        return (lhs > rhs) - (lhs < rhs)

    def _cmp_frame(lhs, rhs):
        if lhs[0] == rhs[0]:
            return 0
        x1, y1 = lhs[0]
        x2, y2 = rhs[0]
        if abs(x1 - x2) < tolerance:
            return _cmp(y1, y2)
        else:
            return _cmp(x2, x1)

    return _cmp_frame


def cut_frame(image, rect):
    center, size, angle = rect
    size = int(np.round(size[0])), int(np.round(size[1]))
    box = cv2.boxPoints(rect)
    M = cv2.getAffineTransform(np.float32(box[1:4]),  np.float32([[0, 0], [size[0], 0], [size[0], size[1]]]))
    return cv2.warpAffine(image, M, size)


def cut_frames(image):
    height, width, ch = image.shape

    # 二値化
    thresh = apply_adaptive_threshold(image)

    # 一番外側の輪郭wだけを抽出
    contours = find_external_contours(thresh)

    # 抽出した輪郭からコマの四角形だけを取り出す
    min_perimeter, max_perimeter = (width + height) * 0.25,  (width + height) * 1.5
    rects = extract_rects_from_controus(contours, min_perimeter, max_perimeter)

    # 抽出した四角形をソートする
    tolerance = width / 3 if width < height else width / 6
    rects = sorted(rects, key=cmp_to_key(cmp_frame(tolerance)))

    # コマの部分の画像を切り出す
    frames = []
    for rect in rects:
        frame = cut_frame(image, rect)
        frames.append(frame)
    return frames


def main():
    for root, dirs, files in os.walk(SRC_DIR):
        rel_path = os.path.relpath(root, SRC_DIR)
        dst_dir = os.path.join(DST_DIR, rel_path)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)

        for file in files:
            name, ext = os.path.splitext(file)
            print(name)
            if ext.lower() not in {".jpg", ".png" ,".gif", ".JPG", ".PNG" ,".GIF"}:
                continue
            file_path = os.path.join(root, file)
            image = cv2.imread(file_path)
            frames = cut_frames(image)
            for i, frame in enumerate(frames):
                print(i)
                dst_path = os.path.join(dst_dir, name + '_' + str(i + 1) + ext)
                cv2.imwrite(dst_path, frame)

if __name__ == '__main__':
    main()
