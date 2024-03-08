# coding: utf-8
#ライブラリのインポート
import cv2
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.simpledialog as simpledialog
import numpy as np
import math

#変数の初期化
pt = {}
m = 0
n = 0
AddPoints = 0
DeletePoints = 0

# PictureWidthとMagnificationは組織画像に合致した値に設定すること！
# 下は、画像を幅142mmで表示すると、倍率1000倍の組織画像になるという設定である
#PictureWidth = 142 #画像の幅（単位：mm）
#Magnification = 1000 #撮影倍率
PictureWidth = 100 #画像の幅（単位：mm）
Magnification = 100 #撮影倍率
Width=640#表示させる画像の幅（高さは元画像から計算）
AnalysisPictureHeight = 140

#マウスの操作があるとき呼ばれる関数
def callback(event, x, y, flags, param):
    global pt, m, n, AddPoints, DeletePoints

    #マウスの左ボタンがクリックされたとき
    if event == cv2.EVENT_LBUTTONDOWN:

        x_value = x-center_x
        y_value = y-center_y

        #三つのほぼ円周上を左クリックしたときのみ点を追加
        if abs(math.sqrt(x_value**2 + y_value**2) - int(Radius1*Width)) < 2 \
        or abs(math.sqrt(x_value**2 + y_value**2) - int(Radius2*Width)) < 2 \
        or abs(math.sqrt(x_value**2 + y_value**2) - int(Radius3*Width)) < 2:
            m = n
            pt[n] = (x, y)
            n = n + 1
            AddPoints = AddPoints + 1
            DrawFigure()

    #マウスの右ボタンがクリックされたとき
    if event == cv2.EVENT_RBUTTONDOWN:
        flag = 0
        #pt[]からクリック位置に近い点を探す
        for i in pt:
            if abs(pt[i][0] - x) < 5 and abs(pt[i][1] - y) < 5:
                point = i
                flag = 1
        if flag == 1:
            del pt[point]   #Dictで定義されている。pt[]の番号1、2、・・・の部分はkeyとなる。
            DeletePoints = DeletePoints + 1
        DrawFigure()

def DrawFigure():

    global img_color, copy_img_color

    #リサイズ後のimg_colorのクローン
    copy_img_color = img_color.copy()

    center_x = int(Width / 2)
    center_y = int(Height / 2)

    #cv2.line(copy_img_color, center_x-, pt2, color, thickness=2, lineType=cv2.LINE_8, shift=0)
    #cv2.circle(copy_img_color, (center_x, center_y), int(Radius1*Width), (0,0,255), thickness=2) #円描画
    #cv2.circle(copy_img_color, (center_x, center_y), int(Radius2*Width), (0,0,255), thickness=2) #円描画
    #cv2.circle(copy_img_color, (center_x, center_y), int(Radius3*Width), (0,0,255), thickness=2) #円描画

    for i in pt:
        cv2.circle(copy_img_color, pt[i], int(Width/100), (255,0,0), thickness=2) #円描画

    points_num = len(pt)
    #cv2.putText(copy_img_color, "Number of grain boundary : " + str(len(pt)) , (int(Width/20), int(Height/15)), cv2.FONT_HERSHEY_PLAIN, Height/400, (255, 255, 255), 2, cv2.LINE_AA)

    point_num_per_1mm = points_num / (500 / Magnification)
	# G0551の式A.11と式A.14の関係を使用（A.11からG(ASTM)を求め、それA.14を使ってGに変換）
    grain_number = -3.3335 + 6.6439 * math.log10(point_num_per_1mm)
    print(f'Number of grain boundaries : {points_num}')
    print(f'Number of grain boundaries per 1 mm : {point_num_per_1mm}')
    print(f'Apparent grain size : {grain_number :.1f}')
    cv2.namedWindow("Result", 16) #組織画像のwindow内で右クリックのメニューを非表示にする
    cv2.imshow("Result", copy_img_color)

#ファイル選択（c:\Dataの拡張子jpgを開く場合）
tk.Tk().withdraw()
fTyp = [("jpg", "*.jpg"), ("BMP", "*.bmp"), ("png", "*.png"), ("tiff", "*.tif")] #画像の種類を選択
iDir='C:/Data'
fname=filedialog.askopenfilename(filetypes=fTyp,initialdir=iDir) 

#ダイアログでPictureWidthとMagnificationを入力
tk.Tk().withdraw()
PhotoMagnification = simpledialog.askstring('画像の倍率入力', '画像の倍率を入力してください', initialvalue="1000")
tk.Tk().withdraw()
PhotoPictureWidth = simpledialog.askstring('画像の幅入力', f'{PhotoMagnification}倍で表示するための画像の幅を入力してください', initialvalue="142")
PhotoMagnification = int(PhotoMagnification)
PhotoPictureWidth = int(PhotoPictureWidth)
print(f'Photo Magnification = {PhotoMagnification}, type = {type(PhotoMagnification)}, Photo Picture Width = {PictureWidth}, type = {type(PhotoPictureWidth)}')

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

center_x = int(Width / 2)
center_y = int(Height / 2)

Flag1 = 0
Flag1_1 = 0
for i in range(1000):
    x1 = int((PictureWidth/2 - 60)/PictureWidth*Width)
    y1 = int((70-50 + i / 10)/PictureHeight*Height)
    kido = img_gray_inv_binary[y1, x1]
    if kido == 255 :
        Flag1 = 1
        if Flag1 == 1 and Flag1_1 == 0:
            m = n
            pt[n] = (x1, y1)
            n = n + 1
    elif kido != 255 :
        Flag1 = 0
    else :
        continue
    Flag1_1 = Flag1

Flag2 = 0
Flag2_1 = 0
for i in range(1000):
    x1 = int((PictureWidth/2 - 50 + i / 10)/PictureWidth*Width)
    y1 = int((130)/PictureHeight*Height)
    kido = img_gray_inv_binary[y1, x1]
    if kido == 255 :
        Flag2 = 1
        if Flag2 == 1 and Flag2_1 == 0:
            m = n
            pt[n] = (x1, y1)
            n = n + 1
    elif kido != 255 :
        Flag2 = 0
    else :
        continue
    Flag2_1 = Flag2

Flag3 = 0
Flag3_1 = 0
for i in range(1000):
    x1 = int((PictureWidth/2 - 50 + i / 10)/PictureWidth*Width)
    y1 = int((70-50 + i / 10)/PictureHeight*Height)
    kido = img_gray_inv_binary[y1, x1]
    if kido == 255 :
        Flag3 = 1
        if Flag3 == 1 and Flag3_1 == 0:
            m = n
            pt[n] = (x1, y1)
            n = n + 1
    elif kido != 255 :
        Flag3 = 0
    else :
        continue
    Flag3_1 = Flag3

Flag4 = 0
Flag4_1 = 0
for i in range(1000):
    x1 = int((PictureWidth/2 - 50 + i / 10)/PictureWidth*Width)
    y1 = int((70+50 - i / 10)/PictureHeight*Height)
    kido = img_gray_inv_binary[y1, x1]
    if kido == 255 :
        Flag4 = 1
        if Flag4 == 1 and Flag4_1 == 0:
            m = n
            pt[n] = (x1, y1)
            n = n + 1
    elif kido != 255 :
        Flag4 = 0
    else :
        continue
    Flag4_1 = Flag4

DrawFigure()

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

