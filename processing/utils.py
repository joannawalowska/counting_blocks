from typing import List

import cv2
import numpy as np
from statistics import mean
import math

wynik = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
before = []
conturss = []

# https://learnopencv.com/shape-matching-using-hu-moments-c-python/
def calculate_mon(warped):
    moments = cv2.moments(warped)
    huMoments = cv2.HuMoments(moments)
    for i in range(0, 7):
        huMoments[i] = -1 * math.copysign(1.0, huMoments[i]) * math.log10(abs(huMoments[i]))
    return huMoments

#ustalenie koloru danego klocka
def get_colors(hsv):
    global before
    before.clear()

    def kol(mask, num):
        mean_val = cv2.mean(hsv, mask=mask)
        h = mean_val[0]
        s = mean_val[1]
        v = mean_val[2]

        if h != 0 and s != 0 and v != 0:
            if num == 5:
                return 5
            elif num == 6:
                return 6
            elif num == 9:
                return 9
            elif num == 7:
                return 7
            elif num == 8:
                return 8
            else:
                return 10
        else:
            return 10


    # niebieski
    low_blue = np.array([100, 85, 50])
    hig_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, low_blue, hig_blue)
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=2)
    before.append(kol(mask, 7))

    # zielony
    low_green = np.array([37, 75, 39])
    hig_green = np.array([89, 255, 255])
    mask2 = cv2.inRange(hsv, low_green, hig_green)
    mask2 = cv2.erode(mask2, np.ones((3, 3), np.uint8), iterations=2)
    before.append(kol(mask2, 6))

    # czerwony
    lower1 = np.array([0, 90, 0])
    upper1 = np.array([5, 255, 255])
    lower2 = np.array([160, 100, 20])
    upper2 = np.array([179, 255, 255])
    lower_mask = cv2.inRange(hsv, lower1, upper1)
    upper_mask = cv2.inRange(hsv, lower2, upper2)
    red_mask = lower_mask + upper_mask
    red_mask = cv2.erode(red_mask, np.ones((3, 3), np.uint8), iterations=2)
    before.append(kol(red_mask, 5))

    #żółty
    low_rel = np.array([19, 130, 100])
    hig_rel = np.array([40, 255, 255])
    mask3 = cv2.inRange(hsv, low_rel, hig_rel)
    mask3 = cv2.erode(mask3, np.ones((3, 3), np.uint8), iterations=2)
    before.append(kol(mask3, 9))

    #biały
    loww_rel = np.array([0, 0, 170])
    higg_rel = np.array([93, 48, 255])
    mask4 = cv2.inRange(hsv, loww_rel, higg_rel)
    mask4 = cv2.erode(mask4, np.ones((3, 3), np.uint8), iterations=2)
    before.append(kol(mask4, 8))

    flag = True
    kolor = 0
    kolor_of = 8


    for i in before:
        if i != 10:
            if flag == False:
                if kolor == i:
                    kolor_of = i
                else:
                    kolor_of = 10
                    break
            else:
                kolor = i
                kolor_of = i
                flag = False

    return kolor_of

#wczytanie i przetwotrzenie klocków bazowych
def make_conturs(lista):
    global conturss


    for img in lista:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        edges = cv2.Canny(gray, 12, 87)

        # niebieski
        low_blue = np.array([100, 85, 50])
        hig_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, low_blue, hig_blue)

        # zielony
        low_green = np.array([37, 75, 39])
        hig_green = np.array([89, 255, 255])
        mask2 = cv2.inRange(hsv, low_green, hig_green)

        # czerwony
        lower1 = np.array([0, 90, 0])
        upper1 = np.array([5, 255, 255])
        lower2 = np.array([160, 100, 20])
        upper2 = np.array([179, 255, 255])
        lower_mask = cv2.inRange(hsv, lower1, upper1)
        upper_mask = cv2.inRange(hsv, lower2, upper2)
        red_mask = lower_mask + upper_mask

        # żółty
        low_rel = np.array([19, 130, 100])
        hig_rel = np.array([40, 255, 255])
        mask3 = cv2.inRange(hsv, low_rel, hig_rel)
        masks_all = mask + mask2 + red_mask + mask3
        out = cv2.bitwise_and(img, img, mask=masks_all)

        dilation = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
        ret, dilation = cv2.threshold(dilation, 0, 255, cv2.THRESH_BINARY)

        dilation = dilation + edges

        dilation = cv2.dilate(dilation, np.ones((3, 3), np.uint8), iterations=2)
        erosion = cv2.erode(dilation, np.ones((2, 2), np.uint8), iterations=2)

        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for num, cnt in enumerate(contours):
            area = cv2.contourArea(cnt)
            if area > 3000:
                img = cv2.drawContours(erosion, [cnt], 0, (255, 255, 255), thickness=cv2.FILLED)

        ret, dilationn = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
        erosion = cv2.erode(dilationn, np.ones((3, 3), np.uint8), iterations=3)

        conturss.append(erosion)

#wstępne obrobienie zdjęcia
def first(img):
    alpha = 1.4
    beta = -50.0
    img = img.astype('int32')
    img = alpha * img + beta
    img = np.clip(img, 0, 255)
    img = img.astype('uint8')

    blur = cv2.pyrMeanShiftFiltering(img, 8, 11)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    edges = cv2.Canny(gray, 12, 80)

    # niebieski
    low_blue = np.array([100, 85, 50])
    hig_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, low_blue, hig_blue)

    # zielony
    low_green = np.array([37, 75, 39])
    hig_green = np.array([89, 255, 255])
    mask2 = cv2.inRange(hsv, low_green, hig_green)

    # czerwony
    lower1 = np.array([0, 90, 0])
    upper1 = np.array([5, 255, 255])
    lower2 = np.array([160, 100, 20])
    upper2 = np.array([179, 255, 255])
    lower_mask = cv2.inRange(hsv, lower1, upper1)
    upper_mask = cv2.inRange(hsv, lower2, upper2)
    red_mask = lower_mask + upper_mask

    # żółty
    low_rel = np.array([19, 130, 100])
    hig_rel = np.array([40, 255, 255])
    mask3 = cv2.inRange(hsv, low_rel, hig_rel)
    masks_all = mask + mask2 + red_mask + mask3
    out = cv2.bitwise_and(img, img, mask=masks_all)

    gray_again = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    ret, thresh_to_com = cv2.threshold(gray_again, 0, 255, cv2.THRESH_BINARY)

    combaind = thresh_to_com + edges

    dilation = cv2.dilate(combaind, np.ones((3, 3), np.uint8), iterations=2)
    erosion = cv2.erode(dilation, np.ones((2, 2), np.uint8), iterations=3)

    contours, hierarchy = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for num, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area > 2800:
            img = cv2.drawContours(thresh_to_com, [cnt], 0, (255, 255, 255), thickness=cv2.FILLED)


    ret, last_thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    erosion = cv2.erode(last_thresh, np.ones((3, 3), np.uint8), iterations=3)
    img2 = cv2.drawContours(erosion, contours, -1, (0, 0, 0), 22)
    masked = cv2.bitwise_and(hsv, hsv, mask=img2)
    erosion = cv2.erode(last_thresh, np.ones((3, 3), np.uint8), iterations=3)

    return erosion, masked

# https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html
def perform_processing(image: np.ndarray, lista) -> List[int]:
    # print(f'image.shape: {image.shape}')
    global wynik, before
    wynik = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    make_conturs(lista)

    width = int(image.shape[1] * 0.4)
    height = int(image.shape[0] * 0.4)
    dim = (width, height)
    img = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    lista_sr = []

    imgg, maskedd = first(img)

    contours, hierarchy = cv2.findContours(imgg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # odrzucenie konturów najmniejszych konturów
    for cn in contours:
        area = cv2.contourArea(cn)
        if area > 3000:
            lista_sr.append(area)

    sr = mean(lista_sr)
    wzor1 = []
    wzor11 = []
    wzor111 = []

    wzor3 = []
    wzor33 = []
    wzor333 = []

    wzor5 = []
    wzor55 = []
    wzor555 = []

    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        area = cv2.contourArea(cnt)
        if area > 0.75 * sr:
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            width = int(rect[1][0])
            height = int(rect[1][1])
            src_pts = box.astype("float32")
            dst_pts = np.array([[0, height - 1],
                                [0, 0],
                                [width - 1, 0],
                                [width - 1, height - 1]], dtype="float32")
            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            warped = cv2.warpPerspective(imgg, M, (width, height))
            warped_hsv = cv2.warpPerspective(maskedd, M, (width, height))
            stosunek = width / height
            # wyznaczanie momentów
            war = calculate_mon(warped)

            for i, m in enumerate(conturss):
                war2 = calculate_mon(m)
                roz = abs(war - war2)
                idx = i

                if idx == 0:
                    if roz[0] < 0.19 and roz[1] < 0.6 and roz[2] < 3.1 and roz[3] < 3. and (
                            (stosunek > 1.9 and stosunek < 3.8) or (stosunek > 0.1 and stosunek < 0.48)):  # wzor 1
                        wzor1.append(area)
                        wzor11.append(cnt)
                        wzor111.append(warped_hsv)

                elif idx == 1:
                    if roz[0] < 0.04 and roz[1] < 1 and roz[2] < 0.8 and roz[3] < 1.5 and (
                            ((stosunek > 1.05) and (stosunek < 1.7)) or (stosunek > 0.6 and stosunek < 1)):  # wzor 2
                        img = cv2.drawContours(img, [cnt], 0, (0, 0, 255), 5)
                        wynik[get_colors(warped_hsv)] = wynik[get_colors(warped_hsv)] + 1
                        wynik[1] = wynik[1] + 1

                elif idx == 2:
                    if roz[0] < 0.1 and roz[1] < 0.5 and roz[2] < 0.5 and roz[3] < 0.7 and (stosunek > 0.6) and (
                            stosunek < 1.65):  # wzor 3,
                        wzor3.append(area)
                        wzor33.append(cnt)
                        wzor333.append(warped_hsv)

                elif idx == 3:
                    if roz[0] < 0.04 and roz[1] < 2.5 and roz[2] < 2.2 and roz[3] < 2:  # wzor 4
                        wynik[3] = wynik[3] + 1
                        wynik[get_colors(warped_hsv)] = wynik[get_colors(warped_hsv)] + 1

                elif idx == 4:
                    if roz[0] < 0.06 and roz[1] < 0.6 and roz[2] < 2.7 and roz[
                        3] < 2.6 and stosunek > 0.6 and stosunek < 1.9:  # wzor 5
                        wzor5.append(area)
                        wzor55.append(cnt)
                        wzor555.append(warped_hsv)

    if wzor55:
        for i, z in enumerate(wzor55):
            if (wzor5[i] > 0.7 * max(wzor5) or wzor5[i] > 0.80 * mean(wzor5)):
                wynik[get_colors(wzor555[i])] = wynik[get_colors(wzor555[i])] + 1
                wynik[4] = wynik[4] + 1

    if wzor33:
        for i, z in enumerate(wzor33):
            if wzor3[i] > 0.65 * max(wzor3):
                wynik[get_colors(wzor333[i])] = wynik[get_colors(wzor333[i])] + 1
                wynik[2] = wynik[2] + 1

    if wzor11:
        for i, z in enumerate(wzor11):
            if wzor1[i] > 0.60 * max(wzor1) or wzor1[i] > 0.7 * mean(wzor1):
                wynik[get_colors(wzor111[i])] = wynik[get_colors(wzor111[i])] + 1
                wynik[0] = wynik[0] + 1


    return wynik


