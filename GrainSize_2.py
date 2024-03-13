# coding: utf-8
#ライブラリのインポート
import cv2
import tkinter
from tkinter import filedialog
import numpy as np
import math

#変数の初期化
pts = []
testline_pts = []

n = 0
AddPoints = 0
DeletePoints = 0

# PictureWidthとMagnificationは組織画像に合致した値に設定すること！
# 下は、画像を幅142mmで表示すると、倍率1000倍の組織画像になるという設定である

Width=640#表示させる画像の幅（高さは元画像から計算）

AnalysisPictureHeight = 140
PhotoMagnification = 1000 #撮影倍率
PhotoPictureWidth = 142 #画像の幅
PictureWidth = 100 #解析時の画像の幅（単位：mm）、初期値100
Magnification = 500 #解析時の撮影倍率、初期値500



#マウスの左右ボタンがクリックされたときの処理
def callback(event, x, y, flags, param):
    global pts, n, AddPoints, DeletePoints

    #マウスの左ボタンがクリックされたとき
    if event == cv2.EVENT_LBUTTONDOWN:
        i = 0
        for testline_pt in testline_pts:
            #クリック位置(x,y)とtestline_ptsとの距離を求める
            #distance = math.sqrt(math.pow((x - _pt[1]), 2) + math.pow((y - _pt[0]), 2))
            #print(distance)
            if math.sqrt(math.pow((x - testline_pt[1]), 2) + math.pow((y - testline_pt[0]), 2)) < 2:
                pts.append([y, x])
                n = n + 1
                AddPoints = AddPoints + 1
                DrawFigure()

    #マウスの右ボタンがクリックされたとき
    if event == cv2.EVENT_RBUTTONDOWN:
        flag = 0
        i = 0
        #pt[]からクリック位置に近い点を探す
        for pt in pts:
            if abs(pt[0] - y) < 5 and abs(pt[1] - x) < 5:
                point = i
                flag = 1
            i += 1
        if flag == 1:
            pts.pop(point)
            DeletePoints = DeletePoints + 1
        DrawFigure()

# 試験線と粒界位置を更新描画
def DrawFigure():

    global img_color, copy_img_color

    #リサイズ後のimg_colorのクローン
    copy_img_color = img_color.copy()

    center_x = int(Width / 2)
    center_y = int(Height / 2)

    cv2.circle(copy_img_color, (center_x, center_y), int(Radius1*Width), (0,0,255), thickness=2) #円描画
    cv2.circle(copy_img_color, (center_x, center_y), int(Radius2*Width), (0,0,255), thickness=2) #円描画
    cv2.circle(copy_img_color, (center_x, center_y), int(Radius3*Width), (0,0,255), thickness=2) #円描画

    for _pt in pts:
        cv2.circle(copy_img_color, (_pt[1], _pt[0]), int(Width/100), (255,0,0), thickness=2) #円描画

    points_num = len(pts)
    #cv2.putText(copy_img_color, "Number of grain boundary : " + str(len(pt)) , (int(Width/20), int(Height/15)), cv2.FONT_HERSHEY_PLAIN, Height/400, (255, 255, 255), 2, cv2.LINE_AA)

    point_num_per_1mm = points_num / (500 / Magnification)
	# G0551の式A.11と式A.14の関係を使用（A.11からG(ASTM)を求め、それA.14を使ってGに変換）
    grain_number = -3.3335 + 6.6439 * math.log10(point_num_per_1mm)
    print(f'Number of grain boundaries : {points_num}')
    print(f'Number of grain boundaries per 1 mm : {point_num_per_1mm}')
    print(f'Apparent grain size : {grain_number :.1f}')
    cv2.namedWindow("Result", 16) #組織画像のwindow内で右クリックのメニューを非表示にする
    cv2.imshow("Result", copy_img_color)

# 試験線の座標値を抽出
def generate_testline_point():

    global testline_pts
    center_x = int(Width / 2)
    center_y = int(Height / 2)

    for i in range(360):
        theata_rad = i * math.pi/180
        x1 = int(center_x + Radius1*Width * math.cos(theata_rad))
        y1 = int(center_y + Radius1*Width * math.sin(theata_rad))
        testline_pts.append([y1, x1])

        x2 = int(center_x + Radius2*Width * math.cos(theata_rad))
        y2 = int(center_y + Radius2*Width * math.sin(theata_rad))
        testline_pts.append([y2, x2])

        x3 = int(center_x + Radius3*Width * math.cos(theata_rad))
        y3 = int(center_y + Radius3*Width * math.sin(theata_rad))
        testline_pts.append([y3, x3])

#ファイル選択（c:\Dataの拡張子jpgを開く場合）
root=tkinter.Tk()
root.withdraw()
fTyp = [("jpg", "*.jpg"), ("BMP", "*.bmp"), ("png", "*.png"), ("tiff", "*.tif")] #画像の種類を選択
iDir = 'C:/Data'
fname=filedialog.askopenfilename(filetypes=fTyp,initialdir=iDir)

#ファイル読み込み
img_color= cv2.imread(fname) #画像ファイルのデータをimg_colorに代入
img_gray = cv2.imread(fname, cv2.IMREAD_GRAYSCALE) #画像ファイルのデータをグレースケールでimg_grayに代入

img_height, img_width = img_gray.shape #画像ファイルのサイズの取得

Height=int(Width*img_height/img_width)

#ここに、解析用の画像の幅と倍率の計算処理を入れる
PhotoPictureHeight = PhotoPictureWidth * img_height/img_width
Magnification = (AnalysisPictureHeight/PhotoPictureHeight)*PhotoMagnification
PictureWidth = PhotoPictureWidth * Magnification / PhotoMagnification
PictureHeight = PictureWidth * img_height/img_width
miniGraSize=10/PictureWidth #（認識させる最小サイズ）/（画像の幅）
Radius1 = 79.58/2/PictureWidth
Radius2 = 53.05/2/PictureWidth
Radius3 = 26.53/2/PictureWidth

img_color = cv2.resize(img_color, (Width, Height))
img_gray = cv2.resize(img_gray, (Width, Height))

#リサイズ後のimg_colorのクローン
copy_img_color = img_color.copy()

#img_grayを反転二値化してimg_gray_inv_binaryに代入、二値化閾値は大津の二値化を使用
ret, img_gray_inv_binary=cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
contours, hier = cv2.findContours(img_gray_inv_binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

#各輪郭について最小外接円を求め、その円の半径がwidth*miniGraSizeより小さい輪郭をcontours1に格納
#その輪郭内を塗りつぶし
contours1 = [e for e in contours if int(Width * miniGraSize)  > int(cv2.minEnclosingCircle(e)[1]*2)]

cv2.drawContours(img_gray_inv_binary, contours1, -1, (0, 0, 0), -1)

Flag1 = 0
Flag1_1 = 0

# 試験線の座標値を抽出
generate_testline_point()

#　試験線の座標値上の輝度値が255の座標を粒界として検出
for testline_pt in testline_pts:
    y1 = testline_pt[0]
    x1 = testline_pt[1]
    print(x1,y1)
    kido = img_gray_inv_binary[y1, x1]
    if kido == 255 :
        Flag1 = 1
        if Flag1 == 1 and Flag1_1 == 0:
            pts.append(testline_pt)
    elif kido != 255 :
        Flag1 = 0
    else :
        continue
    Flag1_1 = Flag1

# 試験線と粒界位置を描画
DrawFigure()

# マウスクリックで呼ばれる関数
cv2.setMouseCallback('Result',callback)

# 任意のキーまたは「閉じる」ボタンをクリックするとウィンドウを閉じてプログラムを終了する
while True:
    key = cv2.waitKey(100) & 0xff
    if key != 255 or cv2.getWindowProperty('Result', cv2.WND_PROP_VISIBLE) !=  1:
        break
cv2.destroyAllWindows()

# 終了時の画像の保存（画像ファイル名＋_resultで同じフォルダに保存）
src = fname
idx = src.rfind(r".")
result_filename = (src[:idx] + "_result." + src[idx + 1 :])
cv2.imwrite(result_filename, copy_img_color)
