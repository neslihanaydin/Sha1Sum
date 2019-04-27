from hashlib import sha1
import sys
import os
import codecs
import subprocess
import json

def karsilastirmaBaslat(sozlukYoluEski,sozlukYoluYeni):
	if(sozlukYoluEski != "" and sozlukYoluYeni != ""):
		print("-------------Karşılaştırma İşlemi Başlatılıyor------------------")
		eskiOzetDict = getEskiOzet(sozlukYoluEski)
		yeniOzetDict = getYeniOzet(sozlukYoluYeni)
		for key in list(yeniOzetDict.keys()):
			if key in list(eskiOzetDict.keys()):
				if eskiOzetDict[key] != yeniOzetDict[key]:
					print("Bu dosyanın içeriği değişmiş -->\n"+key)
			else:
				print("Yeni eklenen dosya var -->"+key)
		print("Karsilastirma işlemi bitti.Dosyalarınızda bir değişiklik görünmüyor.\n")
	else:
		print("Dosya özeti oluşturuldu. Eski dosya özetiyle karşılaştırma yapmak için programı yeniden çalıştırın.")
def getEskiOzet(eskiSozlukYolu):
	if os.path.exists(eskiSozlukYolu):
		with open(eskiSozlukYolu, "r") as dosya:
			sozlukString = (dosya.read())
		sozlukStringToDict = json.loads(str(sozlukString))
		return sozlukStringToDict
	return null
def getYeniOzet(yeniSozlukYolu):
	if os.path.exists(yeniSozlukYolu):
		with open(yeniSozlukYolu, "r") as dosya:
			sozlukString = (dosya.read())
		sozlukStringToDict = json.loads(str(sozlukString))
		return sozlukStringToDict
	return null
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
ozetYolu2 = r"/home/neslihan/Masaüstü/sozlukdosyasieski"
baslangicDizinYolu = r"/run/user/1000/gvfs/"
try:
	subDirSha1 = str(getDizinYolu(baslangicDizinYolu))
	dizinYolu = subDirSha1+"/Android/data"
	#print("dizinYolu "+dizinYolu)
except Exception as e:
	print("USB baglantisini kontrol edin !")
	dizinYolu = ""

print("Özet alma basladi, lütfen usb bağlantısını çıkarmayın..")
i=0
try:
	sozlukYoluYeni,sozlukYoluEski = "",""
	if(os.path.isfile(ozetYolu2)) == True:
		sozlukYoluEski = r"/home/neslihan/Masaüstü/sozlukdosyasieski"
		ozetYolu2 = r"/home/neslihan/Masaüstü/sozlukdosyasiyeni"
		sozlukYoluYeni = ozetYolu2
		sozlukdosya = open(ozetYolu2,"w")
		sozlukdosya.write("{")
		sozlukdosya.close()
	else:
		sozlukdosya = open(ozetYolu2,"a")
		sozlukdosya.write("{")
		sozlukdosya.close()
	j = 0
	for root, dirs, files in os.walk(dizinYolu, topdown=False):
		print(i) # Progres bar gerekiyor
		i=i+1
		yazilacak=""
		for name in files:
			yol = os.path.join(root, name)
			try:
				ozet = getSha1(yol)
			except Exception as e:
				ozet = "Okunamayan dosya turu"
			finally:
				kaydedilecekyol = yol[len(dizinYolu):]				
				sozlukdosya = open(ozetYolu2,"a")
				dosyaadi = name
				if (j==0):
					j = j+1
					sozlukyazilacak = "\""+kaydedilecekyol+"\":\""+ozet+"\"\n"
				else:
					sozlukyazilacak = ",\""+kaydedilecekyol+"\":\""+ozet+"\"\n"				
				sozlukdosya.write(sozlukyazilacak)
				sozlukdosya.close()
	

except Exception as e:
	print(e)
finally:
	sozlukdosya = open(ozetYolu2,"a")
	sozlukdosya.write("}")
	sozlukdosya.close()
	print("Ozet Alma İşlemi Bitti..")
	
karsilastirmaBaslat(sozlukYoluEski,sozlukYoluYeni)





