import cv2

image = cv2.imread("6Pxoh5ac-ngx7-5FDY-0diJ-gl9Nbw2P81dG.jpg")

def image_prep(image=image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    rgb_min = (150, 160, 150)
    rgb_max = (170, 170, 170)
    thresh = cv2.inRange(image, rgb_min, rgb_max)
    r = cv2.bitwise_not(thresh)
    opening = cv2.morphologyEx(r, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    contours, hierarchy = cv2.findContours(closing.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    epsilon = 0.05 * cv2.arcLength(contours[0], True)
    approx = cv2.approxPolyDP(contours[0], epsilon, True)
    res = cv2.bitwise_and(image, image, mask=closing)
    pts = np.float32([approx[0][0], approx[3][0], approx[1][0], approx[2][0]])
    pts2 = np.float32([[0, 0], [400, 0], [0, 400], [400, 400]])
    M = cv2.getPerspectiveTransform(pts, pts2)
    dst = cv2.warpPerspective(image, M, (400, 400))
    return dst

def color_encode(dst=dst):
    color_dict = {0: [255, 255, 255],  # white
                1: [0, 0, 0],  # black
                2: [0, 0, 255],  # red
                3: [0, 136, 255],  # orange
                4: [0, 255, 255],  # yellow
                5: [0, 255, 0],  # green
                6: [255, 255, 0],  # cyan
                7: [255, 0, 0],  # blue
                8: [255, 0, 136],  # violet
                9: [255, 0, 255]}  # magenta
    code = ''
    for i in range(4):
        for j in range(4):
            bgr = dst[i * 100 + 50][j * 100 + 50]
            for k, v in color_dict.items():
                if abs(v[0] - bgr[0]) <= 5 and abs(v[1] - bgr[1]) <= 5 and abs(v[2] - bgr[2]) <= 5:
                    code += str(k)
                    break
    return code

def encode(code=code):
    if (int(code[1]) + int(code[4]) == 7) & (int(code[8]) + int(code[13]) != 7):
        return code
    elif (int(code[7]) + int(code[2]) == 7) & (int(code[1]) + int(code[4]) != 7):
        result = ''
        for i in range(4):
            for j in range(4):
                result += code[3 - i + 4*j]
        return result
    elif (int(code[11]) + int(code[14]) == 7) & (int(code[2]) + int(code[7]) != 7):
        result = ''
        for i in range(4):
            for j in range(4):
                result += code[15 - 4*i - j]
        return result
    else:
        result = ''
        for i in range(4):
            for j in range(4):
                result += code[12 + i - 4*j]
        return result

if __name__ == "__main__":
  image = cv2.imread(input('Demo mode started. Type the file name here and press Enter: '))
  dst = image_prep()
  print('result: ', encode())
