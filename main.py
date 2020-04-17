from PIL import Image, ImageFont, ImageDraw
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

SIZE_X = 860
SIZE_Y = 450
LECNAME_SIZE = (800, 180)
LECNAME_OFF = (30, 35)
JUDGE_SIZE = (300, 170)
JUDGE_OFF = (30, 250)

judgeSymbol = ['SSS', 'SS', 'S', 'A', 'B', 'C', 'D', 'F', '-']
judgeColor = {"SSS": (195, 196, 91), "SS": (195, 196, 91), "S": (195, 196, 91),
              "A": (207, 41, 4), "B": (9, 138, 224), "C": (244, 138, 28),
              "D": (138, 48, 201), "F": (131, 123, 138), "-": (0, 0, 0)}


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

        x = offX + (sizeX - textSize[0]) / 2
        y = offY + (sizeY - textSize[1]) / 2

        image.text((x, y), text, fontColor, font=font)
        return image


# baseImage = loadImage("assets/image/base3.png")
# processImageTitle = addTitleToImage(baseImage, "検索結果", 28, (1, 229, 80))
#
# processImageLec = addTextToImage(baseImage, "lecname", "自然地理学", fontFile="UDDigiKyokashoN-B.ttc", fontSize=51,
#                                  fontColor=(255, 255, 255))
# processImageJudge = addTextToImage(baseImage, "judge", "B", fontFile="mssansBI.ttf", fontSize=85,
#                                    fontColor=judgeColor["B"])
# baseImage.save("d.png")


@app.route("/", methods=["GET"])
def disp():
    searchType = request.args.get('type')
    lectureName = request.args.get('lecname')
    rakutanJudge = request.args.get('judge')

    # validation check
    if searchType != "rakutan" or searchType != "onitan":
        searchType = "normal"
    if rakutanJudge not in judgeSymbol:
        rakutanJudge = "-"

    process = ogpImage()
    baseImage = process.loadImage("assets/image/base3.png")
    processImageTitle = process.addTitleToImage(baseImage, "検索結果", 28, (1, 229, 80))

    processImageLec = process.addTextToImage(baseImage, "lecname", "自然地理学", fontFile="UDDigiKyokashoN-B.ttc",
                                             fontSize=51, fontColor=(255, 255, 255))
    processImageJudge = process.addTextToImage(baseImage, "judge", "B", fontFile="mssansBI.ttf", fontSize=85,
                                               fontColor=judgeColor["B"])
    baseImage.save("tmp/1.png")

    return render_template("index.html", searchType=searchType, lectureName=lectureName, rakutanJudge=rakutanJudge)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
