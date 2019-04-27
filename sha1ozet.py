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
					print("Bu dosyanın içeriği değişmiş -->"+key)
			else:
				print("\nYeni eklenen dosya var -->"+key)
		print("Karsilastirma işlemi bitti.\n")
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
	for subdir in os.listdir(baslangicDizinYolu):
		subDir.append(subdir)
	dondur = (baslangicDizinYolu+"/"+subDir[1]) # ..
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
 
maindir = os.getcwd() 
programKlasoruPath = maindir+r"/SumMyPhone" #ozetlerin tutulacagi konum
if((os.path.isdir(programKlasoruPath))==False): #uygulama ilk defa calistiriliyorsa ya da boyle bir dizin yoksa olustur
	os.mkdir(programKlasoruPath)
	print("SumMyPhone uygulamasına ait dizin oluşturuldu..") 
print(programKlasoruPath)      
ozetYolu = programKlasoruPath+r"/ozetdosyasi"
ozetYolu2 = programKlasoruPath+r"/sozlukdosyasieski"
baslangicDizinYolu = r"/run/user/1000/gvfs/" #Linux tabanli bilgisayarlarda usb baglantilari bu dizin altinda gozukuyor
try:
	subDirSha1 = str(getDizinYolu(baslangicDizinYolu))
	dizinYolu = subDirSha1+"/Android/data" #Baglanan cihazın Android/data klasorundeki dosyalariyla ilgileniliyor
	#print("dizinYolu "+dizinYolu)
except Exception as e:
	print(e)
	print("USB baglantisini kontrol edin !")
	dizinYolu = ""
	exit() #usb baglantisi gerceklesmedigi icin uygulama kapatildi.

print("Özet alma basladi, lütfen usb bağlantısını çıkarmayın..")
i=0 #terminal ekraninda ilerlemenin gozlemlenmesi icin sayac
try:
	sozlukYoluYeni,sozlukYoluEski = "","" #ozetlerin eklenecegi dosyanin yollari
	if(os.path.isfile(ozetYolu2)) == True: #onceden ozet alinmis ise 
		sozlukYoluEski = programKlasoruPath+r"/sozlukdosyasieski"
		ozetYolu2 = programKlasoruPath+r"/sozlukdosyasiyeni" # yeni ozetler bu konuma kaydedilecek
		sozlukYoluYeni = ozetYolu2 #karsilastirmaBaslat fonksiyonuna parametre olarak gidecek
		sozlukdosya = open(ozetYolu2,"w") # yeni ozetleri kaydetmek icin dosya aciliyor
		sozlukdosya.write("{") #dosyaya veriler dictionary yapisinda kaydediliyor.Bu sebeple dictionary takilari ekleniyor
		sozlukdosya.close()
	else:
		sozlukdosya = open(ozetYolu2,"a") #program ilk defa calistiriliyorsa ilk ozet dosyası olusturulacak demektir
		sozlukdosya.write("{") #dictionary yapısı icin gerekli taki
		sozlukdosya.close()
	j = 0 # j degiskeni dictionary takilarinda kontrol icin gerekli
	for root, dirs, files in os.walk(dizinYolu, topdown=False): #ozet almak icin data klasorunun icinde dolasiliyor
		print(i) # Progres bar yapilabilir
		i=i+1
		yazilacak=""
		for name in files:
			yol = os.path.join(root, name) #dosyanin tam yolu alindi
			try:
				ozet = getSha1(yol) #dosyanin tam yolu getSha1() fonksiyonuna gonderilerek ozeti alindi
			except Exception as e: #sha1 kutuphanesinin desteklemedigi turde bir dosya turu var ise exception olusuyor
				print("Bu dosya okunamıyor") #programin durmaması icin kullaniciya bildiriliyor
				ozet = "Okunamayan dosya turu" #okunamayan dosya turu de ozet dosyamiza bu sekilde kaydedilecek
			finally:# ne olursa olsun yapilacak islemler
				kaydedilecekyol = yol[len(dizinYolu):]	#kaydedilecekyol degiskeni dosyanın tam yolunu yazmamak icin kullanilmistir			
				sozlukdosya = open(ozetYolu2,"a") #her bir dosyanin ozeti buraya yazilacaktir
				#dosyaadi = name # gerekli mi ?
				if (j==0):#dictionary yapisi oldugu icin ilk eklemede ',' eklenmemesi lazim. Kontrol yapiliyor
					j = j+1
					sozlukyazilacak = "\""+kaydedilecekyol+"\":\""+ozet+"\"\n"
				else:
					sozlukyazilacak = ",\""+kaydedilecekyol+"\":\""+ozet+"\"\n"	#dictionary yapisinda sozlukyazilacak degiskenine yazildi			
				sozlukdosya.write(sozlukyazilacak)
				sozlukdosya.close()
	

except Exception as e:
	print(e)
finally:#butun yazma islemleri bitince dictionary yapisindan dolayi takilar eklenir
	sozlukdosya = open(ozetYolu2,"a")
	sozlukdosya.write("}")
	sozlukdosya.close()
	print("Ozet Alma İşlemi Bitti..")
	
karsilastirmaBaslat(sozlukYoluEski,sozlukYoluYeni) #karsilastirma islemi baslatilir





