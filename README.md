## 概要
GrainSize_2.pyはGrainSize1.pyの改良版です。
主な変更点は次のとおりです。

- 結晶粒界を格納するpt（ディクショナリ型）をpts（リスト型）に変更
- 試験線を座標値（testline_pts）として格納する方法に変更
- 読み込んだ画像の幅と撮影倍率から、画像の高さを140mmにしたときの倍率を算出し、これら画像の高さと倍率を解析に使用するように変更
- 不要な変数を削除

## 動作環境
GrainSize_2.pyは、Pythonがインストールされたパソコンで動作します。このプログラムの実行には、画像処理のライブラリOpenCVが必要です。

## 使い方
1. **GrainSize_2.py** を適当なフォルダに置きます。
1. **GrainSize_2.py**16行目の **Method**に試験線の種類（'Lines'または'Circles'）を設定します。
   'Lines' は4本の線、'Circles' は3個の同心円になります。
1. **GrainSize_2.py** の20～22行目を設定します。
- **PhotoPictureWidth** には、画像の幅（単位：mm）を入力します。
- **PhotoMagnification** には、顕微鏡で撮影した倍率を入力します。<br>
※プログラムの初期値は、画像を幅142mmで表示すると、倍率1000倍の組織画像になるという設定になっています。
- **miniSize** には、画像の幅に対して画像処理で認識させる結晶粒（輪郭）の最小サイズ（単位：μm）を入力します。
1. **GrainSize_2.py** の158行目の **iDir** には、ダイアログ「画像ファイルを選んでください」で最初に表示させたいフォルダを設定します。<br>
上記の **iDir** に設定したフォルダに **SUJ2_Mag1000_width142mm.jpg** のような組織画像を格納して、**GrainSize_2.py** を実行します。**GrainSize_2.py** と組織画像を格納したフォルダは全角文字を含まない名前としてください。<br>
1. プログラムを実行すると最初にダイアログ「画像ファイルを選んでください」が表示されるので、調べたい組織画像を選択します。少し待つと、試験線（3個の同心円または4本の線）が描画された組織画像が表示されます。小さい丸い点は試験線を横切る結晶粒界の位置を示しています。また、コンソールには<br>




Number of grain boundaries : 69<br>
Number of grain boundaries per 1 mm : 138.0<br>
Apparent grain size : 10.9<br>
が表示されます。<br>
これらは、同心円を横切る結晶粒界の個数、同心円の長さ1mm当たりの結晶粒界の数、粒度番号　を表しています。
1. 同心円状の丸い点はマウスの左クリックで追加、右クリックで削除できます。それに伴い、コンソールに表示される数値も更新されます。<br>
表示されているwindowの大きさは自由に変更できます。
1. 画像を閉じるか、任意のキーを押すと、プログラムは終了します。終了方法は、プログラムの最後の部分を書き換えれば変更できます。<br>
windowに表示されている画像は、読み込んだ画像ファイルと同じフォルダに_resultを付加した名前で終了時に自動保存されます。

## 画像ファイルについて
- SCM435_Mag1000_width142mm.jpg 機械構造用合金鋼SCM435の金属組織
- SUJ2_Mag1000_width142mm.jpg 高炭素クロム軸受鋼SUJ2の金属組織
いずれもAGS腐食液でエッチングしたもので、幅142mmで表示したときに倍率1000倍となります。これらの画像はプログラム **GrainSize_2.py** の **PhotoPictureWidth** と **PhotoMagnification** は変更せずに粒度番号を求めることができます。

## ご利用に関して
- このプログラムでは、結晶粒界が明瞭に現出されている組織画像に対して、結晶粒界を判別することができます。粒界が不明瞭なものについては粒界の検出ができません。
- **PictureWidth** と **Magnification** を組織画像に合わせて設定しないと結晶粒度が正しく求まりませんのでご注意ください。
- このプログラムは、JIS G0551の線分法を完全には対応しておりません。JIS G0551の内容をご理解の上、ご利用ください。
- ご利用結果について当方は責任は負いません。

## 開発環境
- Windows11
- VSC 1.85.2
- Python 3.9.18
- OpenCV 4.5.0


