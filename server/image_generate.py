#-*- coding:utf-8 -*-
from __future__ import print_function
import base64
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import StringIO
from io import BytesIO
import math
import matplotlib.pyplot as plt

def Image_to_Base64(image):
    """ 将PIL图像对象，转换成HTML中能直接使用的src地址 """
    output = BytesIO()
    image.save(output, format='jpeg')
    base64_str = base64.b64encode(output.getvalue()).decode('ASCII')
    image_src = 'data:image/jpeg;base64,' + base64_str
    return image_src


def Get_Image(arg):
    """ 根据指定参数生成一张图片 """
    image = Image.new("RGB", (200, 100), (0, 0, 0))     # 生成图片
    drawBrush = ImageDraw.Draw(image)                   # 创建画刷，用来写文字到图片img上
    ttfont = ImageFont.truetype('C:\Windows\Fonts\Dengb.ttf', 20)   # 华文等线字体
    drawBrush.text((10, 0), '这是动态生成的图片', fill=(0, 0, 0), font=ttfont)
    drawBrush.text((10, 50), arg+'='+str(eval(arg)),fill=(0, 0, 0), font=ttfont)
    drawBrush.rectangle((5,5,195,95),fill=None,outline=(100,100,200))
    drawBrush.line((5,5,195,95),fill=(100,200,100),width=5)
    return image

def Get_Bar_Graph(arg):
    """ 根据指定参数生成一张图片 """
    plt.bar([1,2,3,4,5,6,7,8,9],[5,2,7,8,2,6,2,7,12])
    plt.legend()
    plt.xlabel('station code')
    plt.ylabel('number of received')
    plt.title('Received')
    plt.savefig('/tmp/temp_image.jpg')
    image=Image.open('/tmp/temp_image.jpg')
    return image


def Draw_Arrow(drawBrush,x0,y0,x1,y1,angle,radio,color):
    len_0 = math.sqrt((x0-x1)*(x0-x1) +(y0-y1)*(y0-y1))

    if x1>x0:
        sign=-1
    else:
        sign=1

    x2=x1+sign*len_0*radio * math.cos(angle)
    y2=y1+len_0*radio * math.sin(angle)
    x3=x1+sign*len_0*radio * math.cos(angle)
    y3=y1-len_0*radio * math.sin(angle)
    drawBrush.line((x0,y0+sign,x1,y1+sign),fill=color,width=4)
    drawBrush.line((x1,y1+sign,x2,y2+sign),fill=color,width=3)
    drawBrush.line((x1,y1+sign,x3,y3+sign),fill=color,width=3)

chinese={1:"一",2:'二',3:'三',4:'四',5:'五',6:'六',7:'七',8:'八',9:'九',10:'十'}

def Get_Image_floor(count,rec,col,floor):
    """ 根据指定参数生成一张图片 """

    image = Image.new("RGB", (210, 120), (255, 255, 255))       # 生成图片
    drawBrush = ImageDraw.Draw(image)                           # 创建画刷，用来写文字到图片img上
    font_big = ImageFont.truetype('C:\Windows\Fonts\Dengb.ttf', 20)   # 华文等线字体
    font_mid = ImageFont.truetype("C:\Windows\Fonts\Dengb.ttf", 16)
    font_small = ImageFont.truetype("C:\Windows\Fonts\Dengb.ttf", 12)
    if rec == 0:
        len_add = 0
    else:
        len_add = -140
    if col == 1:
        yel = -255
    else:
        pass
    drawBrush.rectangle((140+len_add,0,209+len_add,99),fill=None,outline=(0,0,0))   #画方框
    drawBrush.rectangle((145+len_add,5,204+len_add,94),fill=None,outline=(0,0,0))   #画方框

    drawBrush.rectangle((150+len_add,15,199+len_add,45),fill=(0,255,0),outline=(0,255,0))  #画绿色填充部分
    drawBrush.rectangle((150+len_add,55,199+len_add,85),fill=(0,255,0),outline=(0,255,0))  #画绿色填充部分

    arrow_len=30
    drawBrush.line((72,15,138,15),fill=(0,0,0),width=5)                    #画中间部分四条线
    drawBrush.line((72,45,138,45),fill=(0,0,0),width=5)
    drawBrush.line((72,55,138,55),fill=(0,0,0),width=5)
    drawBrush.line((72,85,138,85),fill=(0,0,0),width=5)
    drawBrush.rectangle((72,15,138,45),fill=(255,255,255+yel),outline=(255,255,255))
    drawBrush.rectangle((72,55,138,85),fill=(255,255,255+yel),outline=(255,255,255))
    Draw_Arrow(drawBrush,75,30,75+arrow_len,30,math.pi/6,0.3,(0,0,255))        #画中间部分的箭头
    Draw_Arrow(drawBrush,75+arrow_len,70,75,70,math.pi/6,0.3,(0,0,255))

    if count == 2:
        drawBrush.line((2-len_add,15,68-len_add,15),fill=(0,0,0),width=5)                   #画边上四条线
        drawBrush.line((2-len_add,45,68-len_add,45),fill=(0,0,0),width=5)
        drawBrush.line((2-len_add,55,68-len_add,55),fill=(0,0,0),width=5)
        drawBrush.line((2-len_add,85,68-len_add,85),fill=(0,0,0),width=5)
        drawBrush.rectangle((2-len_add,15,68-len_add,45),fill=(255,255,255+yel),outline=(255,255,255))
        drawBrush.rectangle((2-len_add,55,68-len_add,85),fill=(255,255,255+yel),outline=(255,255,255))
        Draw_Arrow(drawBrush,20-len_add,30,20+arrow_len-len_add,30,math.pi/6,0.3,(0,0,255))
           
        Draw_Arrow(drawBrush,20+arrow_len-len_add,70,20-len_add,70,math.pi/6,0.3,(0,0,255))
    else:
        pass
    flo2=chinese[floor]

    drawBrush.text((10, 105), '楼层'+flo2+'，正在上行', fill=(0, 0, 0), font=font_small)
    # image.show()
    return image

if __name__ == '__main__':
    Get_Image_floor(1,1,1,6).show()    #第一个参数表示有几部分 1为1部分，0为两部分；第二个参数表示方框在哪边，0为在右，1为在左
                                       #第三个参数表示是否正在运行（是否有黄底），1为有，0为无
                                       #第四、五个参数表示楼层