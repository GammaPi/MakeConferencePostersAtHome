byimport math
import pdf2image
import numpy as np
import os
from PIL import Image,ImageDraw,ImageFont
from tqdm import tqdm
import logging
logger=logging.getLogger(__name__)
Image.MAX_IMAGE_PIXELS = 777600000
'''
Author: Steven Tang
Version: 1.1
'''


def inchToPixel(inch, dpi):
    '''
    Convert inch to text
    :param inch: inches
    :param dpi: Dots per inch
    :return: Pixel value
    '''
    return int(inch * dpi)


def pixelToInch(pixel, dpi):
    '''
    Convert pixel to inch
    :param pixel: pixel number
    :param dpi: Dots per inch
    :return: Pixel value
    '''
    return pixel / dpi

class Config:
    def __init__(self):
        self.pdfPath=None
        self.paperWidth=None
        self.paperHeight=None
        self.minGlueBorderSize=None
        self.printerPPI=None

def generateImage(content, rowI, colI, currtingIndicator,paperSize:tuple):

    shouldCutLeft, shouldCutRight, shouldCutTop, shouldCutBottom = currtingIndicator

    newImg=Image.new('RGB',size=paperSize,color=(255,255,255))

    paperWidth,paperHeight=paperSize

    '''
    Paste image at center
    '''
    contentX=(paperWidth-content.width)//2
    contentY=(paperHeight-content.height)//2
    contentXp=contentX+content.width
    contentYp=contentY+content.height
    newImg.paste(content,(contentX,contentY))

    '''
    Calculate coordinates
    '''

    newImgDraw=ImageDraw.Draw(newImg)
    borderColor=['#d3d3d3','#646464']
    borderColorBoxCoords=[
        # Left border
        ((0, 0), (contentX, paperHeight)),
        # Right border
        ((contentXp, 0), (paperWidth, paperHeight)),
        #Top Border
        ((0, 0), (paperWidth, contentY)),
        #Bottom Border
        ((0, contentYp), (paperWidth, paperHeight))
    ]
    borderLineCoords = [
        # Left border
        ((contentX-5, 0), (contentX, paperHeight)),
        # Right border
        ((contentXp, 0), (contentXp+5, paperHeight)),
        # Top Border
        ((0, contentY-5), (paperWidth, contentY)),
        # Bottom Border
        ((0, contentYp), (paperWidth, contentYp+5))
    ]
    textLeftTopAnchor=[None,None,None,None] #Calculated below


    '''
    Draw border color
    '''
    for i,v in enumerate(currtingIndicator):
        if v==False:
            newImgDraw.rectangle(borderColorBoxCoords[i], fill=borderColor[v])
    for i, v in enumerate(currtingIndicator):
        if v==True:
            newImgDraw.rectangle(borderColorBoxCoords[i], fill=borderColor[v])
    '''
    Search optimal font size
    '''
    optimalFont = ImageFont.truetype(''.join([os.path.dirname(os.path.realpath(__file__)), os.sep, 'Roboto-Black.ttf']),
                             size=100)
    for i, v in enumerate(currtingIndicator):
        leftTop = borderColorBoxCoords[i][0]
        rightBottom = borderColorBoxCoords[i][1]
        textLeftTopAnchor[i] = [(leftTop[0] + rightBottom[0]) / 2, (leftTop[1] + rightBottom[1]) / 2]
        text = None
        if v == True:
            text = '(%d,%d)\nCUT/FOLD' % (rowI, colI)
        else:
            text = '(%d,%d)\nGLUE' % (rowI, colI)

        while True:
            textL, textT, textR, textB = newImgDraw.textbbox((0,0), text, optimalFont, align='center')
            if ((textR - textL) < contentX * 0.6 and (textB - textT) < contentY * 0.6):
                textLeftTopAnchor[i][0] -= (textR - textL) / 2
                textLeftTopAnchor[i][1] -= (textB - textT) / 2
                break
            else:
                optimalFont = ImageFont.truetype('Roboto-Black.ttf', size=optimalFont.size - 10)

    '''
    Draw text and cutting hints
    '''
    for i, v in enumerate(currtingIndicator):
        newImgDraw.rectangle(borderLineCoords[i],fill='black')
        text=None
        fillColor=None
        if v==True:
            text='(%d,%d)\nCUT/FOLD'%(rowI,colI)
            fillColor='white'
        else:
            text='(%d,%d)\nGLUE'%(rowI,colI)
            fillColor='black'
        newImgDraw.text(textLeftTopAnchor[i],text,fillColor,align='center',font=optimalFont)

    return newImg


def processAndSavePages(pageId,oriImg,config:Config):

    glueBorderSize = inchToPixel(config.minGlueBorderSize, config.printerPPI)
    pageWidth=inchToPixel(config.paperWidth, config.printerPPI)
    pageHeight=inchToPixel(config.paperHeight, config.printerPPI)
    imagePatchWidth = pageWidth-glueBorderSize
    imagePatchHeight = pageHeight-glueBorderSize

    paperNumberRows = math.ceil((oriImg.height) / (imagePatchHeight-2*glueBorderSize))
    paperNumberCols = math.ceil((oriImg.width) / (imagePatchWidth-2*glueBorderSize))

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

    imageList=[]
    contentHeight = oriImg.height / paperNumberRows
    contentWidth = oriImg.width / paperNumberCols
    for curRow in tqdm(range(paperNumberRows)):
        for curCol in range(paperNumberCols):
            x = curCol * contentWidth
            y = curRow * contentHeight
            imagePatch=oriImg.crop([x,y,x + contentWidth, y + contentHeight])
            curImg = generateImage(imagePatch, curRow, curCol,
                          (leftCuttingMethodArray[curRow, curCol],
                           rightCuttingMethodArray[curRow, curCol],
                           topCuttingMethodArray[curRow, curCol],
                           bottomCuttingMethodArray[curRow, curCol]),
                                   (pageWidth,pageHeight))
            imageList.append(curImg)

    with open('output_page%d.pdf'%(pageId),'wb') as f:
        imageList[0].save(f,format='PDF',save_all=True,append_images=imageList[1:],dpi=(config.printerPPI,config.printerPPI),
                          creator="https://github.com/GammaPi/MakeConferencePostersAtHome")


if __name__ == '__main__':
    config=Config()
    config.pdfPath= input('PDF Path:\n')
    config.paperWidth = float(input('Paper Width (In inches):\n'))
    config.paperHeight = float(input('Paper Height (In inches):\n'))
    config.minGlueBorderSize = float(input('Min Glue Border Width (In inches):\n'))
    config.printerPPI = 300

    imageList = pdf2image.convert_from_path(config.pdfPath,dpi=config.printerPPI)
    for i,curImg in tqdm(enumerate(imageList),position=0):
        processAndSavePages(i,curImg,config)


