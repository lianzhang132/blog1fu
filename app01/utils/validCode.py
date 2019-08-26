import random
def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def get_valid_code_img(request):
    # 方式1:
    # with open("lufei.jpg","rb") as f:
    #     data=f.read()

    # 方式2: # pip install pillow

    # from PIL import Image
    # img=Image.new("RGB",(270,40),color=get_random_color())
    #
    # with open("validCode.png","wb") as f:
    #     img.save(f,"png")
    #
    # with open("validCode.png","rb") as f:
    #     data=f.read()


    # 方式3:

    # from PIL import Image
    # from io import BytesIO
    #
    # img=Image.new("RGB",(270,40),color=get_random_color())
    # f=BytesIO()
    # img.save(f,"png")
    # data=f.getvalue()



    # 方式4:

    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO
    import random

    img = Image.new("RGB", (270, 40), color=get_random_color())#生成一个宽270*高40的画布，背景颜色随机

    draw = ImageDraw.Draw(img)#进行绘画
    kumo_font = ImageFont.truetype("static/font/kumo.ttf", size=32)#字体  字体大小

    valid_code_str = ""

    for i in range(1):
        random_num = str(random.randint(0, 9))#0-9的随机数  9
        random_low_alpha = chr(random.randint(97, 122))#a 到 z 随机的一个小写字母  b
        random_upper_alpha = chr(random.randint(65, 90))#A 到 Z 随机的一个大写字母  Q
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])        #2
        draw.text((i * 50 + 20, 5), random_char, get_random_color(), font=kumo_font) #往长方形上写字
        # 保存验证码字符串
        valid_code_str += random_char #85656
    #
    width=270
    height=40
    for i in range(10):
        # draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())#画小点
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color()) #小线段
    request.session["valid_code_str"] = valid_code_str

    '''
    1 sdajsdq33asdasd
    2 COOKIE {"sessionid":sdajsdq33asdasd}
    3 django-session
      session-key       session-data
      sdajsdq33asdasd   {"valid_code_str":"12345"}
    '''
    f = BytesIO()
    img.save(f, "png") #png
    data = f.getvalue()
    return data