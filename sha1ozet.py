from hashlib import sha1
import sys
import os
import codecs
import subprocess

def getDizinYolu(baslangicDizinYolu):
	subDir=[]
	yol = subprocess.check_output(["ls",baslangicDizinYolu])
	yol = str(yol)
	tempYol = ""
	for i in range(len(yol)):
		if (i>1 and i< (len(yol)-3)):
			tempYol+=yol[i]
	print("---------------------")
	baslangicDizinYolu+=tempYol
	#print("baslangicDizinYolu" + baslangicDizinYolu)
	for subdir in os.listdir(baslangicDizinYolu):
		subDir.append(subdir)
	dondur = (baslangicDizinYolu+"/"+subDir[1])
	return dondur
	

	

def getSha1(filePath):
    m = sha1()
    if os.path.exists(filePath):
        with codecs.open(filePath,"r",encoding='ISO-8859-1', errors='ignore') as fp:
            data = fp.read()
            m.update(data.encode('ISO-8859-1'))
        return m.hexdigest()
    else:
        print ("File Not Found")
        
ozetYolu = r"/home/neslihan/Masaüstü/ozetdosyasi"
#dizinYolu2= r"/home/neslihan/Masaüstü/ozet1"
#dizinYolu1 = r"/run/user/1000/gvfs/mtp:host=%5Busb%3A003%2C010%5D/Dahili olarak paylaşılan depolama alanı/system"
#dizinYolu = r"/run/user/1000/gvfs/mtp:host=%5Busb%3A003%2C004%5D/Dahili olarak paylaşılan depolama alanı/Android/data/com.instagram.android"

baslangicDizinYolu = r"/run/user/1000/gvfs/"
try:
	subDirSha1 = str(getDizinYolu(baslangicDizinYolu))
	dizinYolu = subDirSha1+"/Android/data"
	#print("dizinYolu "+dizinYolu)
except Exception as e:
	print("USB baglantisini kontrol edin !")
	dizinYolu = ""

if (os.path.isfile(ozetYolu))==False:
    ozetDosyasi = open(ozetYolu,"a")
    ozetDosyasi.close()
print("Basladi")
i=0
try:
	for root, dirs, files in os.walk(dizinYolu, topdown=False):
		print(i)
		i=i+1
		yazilacak=""
		for name in files:
			yol = os.path.join(root, name)
			try:
				ozet = getSha1(yol)
			except Exception as e:
				print("Bu dosya türü okunamıyor")
				ozet = "Okunamayan dosya turu"
			finally:				
				ozetdosya = open(ozetYolu,"a")
				dosyaadi = name
				yazilacak = ""+yol+" ----> "+ozet+"\n"
				ozetdosya.write(yazilacak)
				ozetdosya.close()
except Exception as e:
	print(yazilacak)
	print(yol)
	print(dosyaadi)
	print(e)
finally:
	print("Bitti..Finally")

print("Bitti..")
        
