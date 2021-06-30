import base64
# from PIL import Image


# 图片验证码图片获取base64转图片，保存为imgCode.jpg
def base64Tojpg(kaptcha):
    imgdata = base64.b64decode(kaptcha)
    file = open('imgCode.jpg', 'wb')
    file.write(imgdata)


# base64解码
def base64Totext(kaptchaToken):
    textdata = base64.b64decode(kaptchaToken)
    imageCode = textdata.decode()
    # imageCode = textdata.decode()[-4:]
    return imageCode


# 图片内字符提取
# def jpgToText(self):
#     # path = "imgCode.jpg"
#     # 读取图片
#     image = Image.open("imgCode.jpg")
#     pix = image.load()
#     width = image.size[0]
#     height = image.size[1]
#     # 生成新的图片
#     image_r = Image.new("RGB", (width, height))
#     image_g = Image.new("RGB", (width, height))
#     image_b = Image.new("RGB", (width, height))
#     # 提取黑色干扰像素
#     for x in range(width):
#         for y in range(height):
#             r, g, b = pix[x, y]
#             n = r // 128 * 255
#             # 填充入新的图片
#             image_r.putpixel((x, y), (n, n, n))
#     # 提取黑色干扰像素
#     for x in range(width):
#         for y in range(height):
#             r, g, b = pix[x, y]
#             n = b//128*255
#             # 填充入新的图片
#             image_b.putpixel((x, y), (n, n, n))
#     # 提取空白部分
#     for x in range(width):
#         for y in range(height):
#             r, g, b = pix[x, y]
#             n = g // 128 * 255
#             # 填充入新的图片
#             image_g.putpixel((x, y), (n, n, n))
#     image.close()
#     # 保存新图片
#     image_r.save('r_new.jpg')
#     image_g.save('g_new.jpg')
#     image_b.save('b_new.jpg')
#     image_new = image_b
#     # 识别新生成的图片内字符
#
#     # im = pytesseract.image_to_string(image_new)
#     # return im


if __name__ == "__main__":
    # #     kaptcha = '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'
    # #     x = imagCodeToText().base64Tojpg(kaptchaToken)
    #     kaptchaToken = "S0FQVENIQW15ZjU="
    kaptchaToken = "bUpIFNz5keTr9ymlKy4pKw=="
    base = ""
    x = base64Totext(base)
    print(x)
