import math

import numpy as np
import cv2

'''
Author: Steven Tang
Version: 1.0
'''


def inchToPixel(inch, dpi):
    '''
    Convert inch to text
    :param inch: inches
    :param dpi: Dots per inch
    :return: Pixel value
    '''
    return int(float(inch) * float(dpi))


def pixelToInch(pixel, dpi):
    '''
    Convert pixel to inch
    :param pixel: pixel number
    :param dpi: Dots per inch
    :return: Pixel value
    '''
    return int(pixel) // float(dpi)


def drawTextAtCenter(image, text):
    '''
    Draw text at the center of an image
    '''
    # rlt=image.copy(image)

    imgRows, imgCols, _ = image.shape

    fontFace = cv2.FONT_HERSHEY_DUPLEX
    fontScale = 4.0
    thickness = 4

    (textW, textH), _ = cv2.getTextSize(text, fontFace=fontFace, fontScale=fontScale, thickness=thickness)

    return cv2.putText(image, text, (imgCols // 2 - textW // 2, imgRows // 2 - textH // 2), fontFace=fontFace,
                       fontScale=fontScale, thickness=thickness, color=(0, 0, 0))


def generateImage(content, rowI, colI, currtingIndicator, borderWidth):
    shouldCutLeft, shouldCutRight, shouldCutTop, shouldCutBottom = currtingIndicator

    contentWithBorderRows = content.shape[0] + borderWidth * 2
    contentWithBorderCols = content.shape[1] + borderWidth * 2

    newImg = np.ones(shape=(contentWithBorderRows, contentWithBorderCols, 3)) * 255

    borderLeft = newImg[:, 0:borderWidth, :]
    borderRight = newImg[:, contentWithBorderCols - (borderWidth):, :]
    borderTop = newImg[0:borderWidth, :, :]
    borderBottom = newImg[contentWithBorderRows - (borderWidth):, :, :]
    contentImg = newImg[borderWidth: contentWithBorderRows - (borderWidth),
                 borderWidth: contentWithBorderCols - (borderWidth), :]

    contentImg[:, :, :] = content[:, :, :]

    # Draw seperators
    borderLeft[:, -10:, :] = 0
    borderRight[:, :10, :] = 0
    borderTop[-10:, :, :] = 0
    borderBottom[10:, -10:, :] = 0

    if shouldCutLeft:
        borderLeft[:, :, :] = 200

    if shouldCutRight:
        borderRight[:, :, :] = 200

    if shouldCutTop:
        borderTop[:, :, :] = 200

    if shouldCutBottom:
        borderBottom[:, :, :] = 200

    borderLeft[:, :, :] = drawTextAtCenter(borderLeft, str('%d,%d' % (rowI, colI)))
    borderRight[:, :, :] = drawTextAtCenter(borderRight,str('%d,%d' % (rowI, colI)))
    borderTop[:, :, :] = drawTextAtCenter(borderTop, str('%d,%d' % (rowI, colI)))
    borderBottom[:, :, :] = drawTextAtCenter(borderBottom, str('%d,%d' % (rowI, colI)))

    cv2.imwrite(str((rowI, colI)) + '.jpg', newImg)
    # cv2.waitKey()


if __name__ == '__main__':
    paperWidth = input('Paper Width (In inches)')
    paperHeight = input('Paper Height (In inches)')

    minGlueBorderWidth = input('Min Glue Border Width (In inches)')
    printerPPI = input('Printer PPI')
    imagePath=input('Image Path')

    oriImg = cv2.imread(imagePath)
    posterHeight = oriImg.shape[0]
    posterWidth = oriImg.shape[1]

    # cv2.namedWindow('Ori', cv2.WINDOW_NORMAL)
    # cv2.imshow('Ori', oriImg)
    # cv2.waitKey()

    paperWidth = inchToPixel(paperWidth, printerPPI)
    paperHeight = inchToPixel(paperHeight, printerPPI)
    minGlueBorderWidth = inchToPixel(minGlueBorderWidth, printerPPI)

    paperNumberRows = math.ceil(posterHeight / paperHeight)
    paperNumberCols = math.ceil(posterWidth / paperWidth)

    topCuttingMethodArray = np.zeros(shape=(paperNumberRows, paperNumberCols), dtype=int)
    leftCuttingMethodArray = np.zeros(shape=(paperNumberRows, paperNumberCols), dtype=int)
    rightCuttingMethodArray = np.zeros(shape=(paperNumberRows, paperNumberCols), dtype=int)
    bottomCuttingMethodArray = np.zeros(shape=(paperNumberRows, paperNumberCols), dtype=int)

    topCuttingMethodArray[0, :] = 1
    leftCuttingMethodArray[:, 0] = 1
    rightCuttingMethodArray[:, 0:] = 1
    bottomCuttingMethodArray[0:, :] = 1

    totalCutNum = (topCuttingMethodArray == 1).shape[1] + \
                  (leftCuttingMethodArray == 1).shape[1] + \
                  (rightCuttingMethodArray == 1).shape[1] + \
                  (bottomCuttingMethodArray == 1).shape[1]

    for curRow in range(paperNumberRows):
        for curCol in range(paperNumberCols):
            contentRows = posterHeight // paperNumberRows
            contentCols = posterWidth // paperNumberCols

            generateImage(oriImg[curRow * contentRows:min(posterHeight, (curRow + 1) * contentRows),
                          curCol * contentCols:min(posterWidth, (curCol + 1) * contentCols), :], curRow, curCol,
                          (leftCuttingMethodArray[curRow, curCol],
                           rightCuttingMethodArray[curRow, curCol],
                           topCuttingMethodArray[curRow, curCol],
                           bottomCuttingMethodArray[curRow, curCol]), minGlueBorderWidth)
