import datetime
import hashlib
import requests
import urllib.parse

from PIL import Image, ImageFont, ImageDraw
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

SIZE_X = 860
SIZE_Y = 450
LECNAME_SIZE = (800, 180)
LECNAME_OFF = (30, 40)
JUDGE_SIZE = (300, 170)
JUDGE_OFF = (30, 250)

judgeSymbol = ['SSS', 'SS', 'S', 'A', 'B', 'C', 'D', 'F', '?']
judgeColor = {"SSS": (195, 196, 91), "SS": (195, 196, 91), "S": (195, 196, 91),
              "A": (207, 41, 4), "B": (9, 138, 224), "C": (244, 138, 28),
              "D": (138, 48, 201), "F": (131, 123, 138), "?": (131, 123, 138)}


class ogpImage:
    def __init__(self):
        pass

    def loadImage(self, path):
        imageObj = Image.open(path).copy()
        return imageObj

    def addTitleToImage(self, img, text, fontSize, fontColor):
        font = ImageFont.truetype("assets/fonts/UDDigiKyokashoN-B.ttc", fontSize)
        image = ImageDraw.Draw(img)

        x = 45
        y = 50

        image.text((x, y), text, fontColor, font=font)
        return image

    def addTextToImage(self, img, types, text, fontFile, fontSize, fontColor):
        font = ImageFont.truetype("assets/fonts/{}".format(fontFile), fontSize)
        # font = ImageFont.truetype("assets/fonts/mssansBI.ttf", fontSize)
        image = ImageDraw.Draw(img)

        textSize = image.textsize(text, font=font)

        if types == "lecname":
            sizeX, sizeY = LECNAME_SIZE
            offX, offY = LECNAME_OFF
        elif types == "judge":
            sizeX, sizeY = JUDGE_SIZE
            offX, offY = JUDGE_OFF
        else:
            sizeX, sizeY = (100, 100)
            offX, offY = (30, 30)

        while textSize[0] + 10 > sizeX:
            fontSize -= 2
            font = ImageFont.truetype("assets/fonts/{}".format(fontFile), fontSize)
            textSize = image.textsize(text, font=font)

        x = offX + (sizeX - textSize[0]) / 2
        y = offY + (sizeY - textSize[1]) / 2

        image.text((x, y), text, fontColor, font=font)
        return image


@app.route("/", methods=["GET"])
def hello():
    imageID = request.args.get('gid')
    if (imageID is None) or (not imageID.isalnum()):
        imageURL = "default.png"
    else:
        imageURL = imageID + ".png"

    return render_template("index.html", imageURL=imageURL)


@app.route("/gen", methods=["GET"])
def disp():
    searchType = request.args.get('type')
    lectureName = request.args.get('lecname')
    facultyName = request.args.get('facname')
    rakutanJudge = request.args.get('judge')

    # validation check

    if searchType != "rakutan" and searchType != "onitan" and searchType != "jinsha":
        searchType = "normal"
    if rakutanJudge not in judgeSymbol:
        rakutanJudge = "?"
    if lectureName is None:
        lectureName = "Sample Text"
    if facultyName is None:
        facultyName = '---'

    # searchType
    if searchType == "rakutan":
        titleVal = ("楽単おみくじ", (255, 126, 65))
    elif searchType == "onitan":
        titleVal = ("鬼単おみくじ", (109, 123, 255))
    elif searchType == "jinsha":
        titleVal = ("人社おみくじ", (204, 145, 62))
    else:
        titleVal = ("検索", (1, 229, 80))

    process = ogpImage()
    baseImage = process.loadImage("assets/image/base3.png")
    processImageTitle = process.addTitleToImage(baseImage, titleVal[0] + "結果", 28, titleVal[1])
    processImageLec = process.addTextToImage(baseImage, "lecname", lectureName, fontFile="UDDigiKyokashoN-B.ttc",
                                             fontSize=51, fontColor=(255, 255, 255))
    processImageJudge = process.addTextToImage(baseImage, "judge", rakutanJudge, fontFile="mssansBI.ttf", fontSize=85,
                                               fontColor=judgeColor[rakutanJudge])

    tmpName = lectureName + facultyName

    fileName = hashlib.md5(tmpName.encode()).hexdigest()

    baseImage.save("static/tmp/{}.png".format(fileName))

    if searchType != "normal":
        tweetText = urllib.parse.quote(
            "{}の結果「{}」[{}]はらくたん判定{}でした".format(titleVal[0], lectureName, facultyName, rakutanJudge))
    else:
        tweetText = urllib.parse.quote("「{}」[{}]はらくたん判定{}でした".format(lectureName, facultyName, rakutanJudge))

    hashtag = urllib.parse.quote("京大楽単bot")

    redirectURL = "https://twitter.com/share?url=https://ku-rakutan.das82.com/?gid={}&text={}&hashtags={}".format(
        fileName,
        tweetText,
        hashtag)

    return redirect(redirectURL, code=302)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
