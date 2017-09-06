import random as rnd
import time
import os
import tkinter as tk
import subprocess as sp
import platform as plt

#Kullanılacak yazı tipleri için  makro tanımlar.
TIP = ("Verdana", 12)
TIP_1 = ("Helvetica", 24)
K_TIP_1 = ("Helvetica", 12)
YOL = ".{}SoruDosyaları".format(os.sep)

class CarePython(tk.Tk):
    "Mayınlardan python ile kurtulun."
    def __init__(self, *args, **kwargs):
        """Kontrol sınıfının yapılandırıcı fonksiyonudur.
Kontrol sınıfımızın üst sınıfının yapılandırıcı fonksiyonunun
özelliklerini super fonksiyonuyla alır.Ayrıca
oyunun diğer sayfalarını içerisinde barındıracak taşıyıcı sayfayı
tanımlar.Oyundaki tüm sayfalarının sınıfları örnekleyerek bir
sözlük içine koyar ve yeri geldiğinde bu sayfaların gösterilmesini
sağlar"""
        super().__init__(*args, **kwargs)
        #Oyunun pencere başlığı
        tk.Tk.wm_title(self, "Mayın Tarlası")
        #Sayfa boyutu sabitlenir ve boyutlandırılır.
        self.resizable(width=False, height=False)
        self.geometry('{}x{}'.format(372, 400))
        
        #Tüm sayfaları barındıracak ana sayfa.
        self.tasiyici = tk.Frame(self)
        self.tasiyici.pack()
        
        #programın kullanacağı ek dosya ve klasörleri denetler.
        #yoksa oluşturur, varsa işleme devam eder.
        Islemler.kaynak_denetimi()
        
        #Oyundaki tüm sayfaların örneklerinin bulunduğu sözlük.
        #Bu sözlükte tüm sayfaların sınıfları örneklenmiştir ve
        #kullanılmaya hazırdır.cerceve_goster fonksiyonu ile
        #gereken zamanda sayfalar gösterilir.
        self.cerceveler = {}
        for sayfa in ["AnaSayfa", "Oyun", "YuksekSkorlar", "Ogretici"]:
            sınıf_adı = eval(sayfa)
            self.cerceveler[sayfa] = sınıf_adı(self.tasiyici, self)
            self.cerceveler[sayfa].grid(row=0, column=0, sticky="nsew")
        #başlangıçta anasayfayı gösterir.
        self.cerceve_goster("AnaSayfa")
    
    def cerceve_goster(self, sayfa_adı):
        """sayfa adlarını parametle olarak alır.Bu sayfa adını
kullanarak, sayfalarının örneklerinin bulunduğu sözlükten sayfayı
bulur.Daha sonra tk.raise metodu ile bu sayfayı ekranda gösterir."""
        self.cerceve = self.cerceveler[sayfa_adı]
        self.cerceve.tkraise()
    
    def sayfa_yenile(self, sayfa_listesi):
        """yenilecek sayfaların adını bir liste içinde alır
        ve bu sayfaları yeniden oluşturulur.Böylece sayfa içinde olan
        değişiklikler ekrana yansır."""
        for sayfa in sayfa_listesi:
            sınıf_adı = eval(sayfa)
            self.cerceveler[sayfa] = sınıf_adı(self.tasiyici, self)
            self.cerceveler[sayfa].grid(row=0, column=0, sticky="nsew")
        
        
        
        
class AnaSayfa(tk.Frame):
    def __init__(self, tasiyici, kontrolcu):
        """Anasayfa sınıfıdır.Programın sayfalarına
erişmek için gerekli butonları içerir."""
        #Frame sınıfının niteliklerini super fonksiyonu ile alır.
        #tasiyici bu çerçeveyi taşıyan kök penceredir.
        super().__init__(tasiyici)
        #Oyun başlığıdır.
        self.baslik_etiketi = tk.Label(self, text="Mayın Tarlası",
                                  relief=tk.GROOVE, borderwidth=5,
                                  width=20, fg="black", bg="gray",
                                  font=TIP_1)
        self.baslik_etiketi.grid(row=0, column=0, columnspan=3)
        #Oyun penceresine geçiş butonudur.
        self.buton = tk.Button(self, text="Oyun", relief=tk.RAISED,
                            borderwidth=2, width=20, font=K_TIP_1,
                            command=
                            lambda: kontrolcu.cerceve_goster("Oyun"))
        self.buton.grid(row=1, column=1)
        #Öğretici penceresine geçiş butonudur.
        self.buton1 = tk.Button(self, text="Öğretici", relief=tk.RAISED,
                            borderwidth=2, width=20, font=K_TIP_1,
                            command=
                            lambda: kontrolcu.cerceve_goster("Ogretici"))
        self.buton1.grid(row=2, column=1)
        #Yüksek skorlar penceresine geçiş butonudur.
        self.buton2 = tk.Button(self, text="Yüksek Skorlar",
                            relief=tk.RAISED, borderwidth=2,
                            width=20, font=K_TIP_1, command=lambda:
                            kontrolcu.cerceve_goster("YuksekSkorlar"))
        self.buton2.grid(row=3, column=1)
        
        
class Oyun(tk.Frame):
    """Oyunun yaratıldığı sınıftır."""
    def __init__(self, tasiyici, kontrolcu):
        super().__init__(tasiyici)
        self.harita = Islemler.son_haritayi_bul()
        self.buton_sayisi = 64

        self.puan_etiketi = tk.Label(self, text= "0", font=TIP_1)
        self.puan_etiketi.grid(row=0, column=0, columnspan=3)
        
        self.tarla_tasiyici = tk.Frame(self, padx=10, pady=10)
        self.tarla_tasiyici.grid(row=1, column=0, columnspan=3)
        
        for r  in range(8):
            for c in range(8):
                if self.harita[r][c] == 'x':
                    bos_buton = tk.Button(self.tarla_tasiyici, 
                                   relief=tk.RAISED, width=2,
                                   borderwidth=2)
                    bos_buton["command"] = (lambda buton=bos_buton : 
                                            self.bos_butonlar(buton))
                    bos_buton.grid(row=r, column=c)
                elif self.harita[r][c] == '?':
                    soru_buton = tk.Button(self.tarla_tasiyici, 
                                    relief=tk.RAISED, width=2,
                                    borderwidth=2)
                    soru_buton["command"] = (lambda buton=soru_buton :
                                             self.soru_butonu(buton))
                                            
                    soru_buton.grid(row=r, column=c)
                elif self.harita[r][c] == 'b':
                    bonus_buton = tk.Button(self.tarla_tasiyici,
                                    relief=tk.RAISED, width=2,
                                    borderwidth=2)
                    bonus_buton["command"] = (lambda buton=bonus_buton :
                                              self.bonus_butonu(buton))
                    bonus_buton.grid(row=r, column=c)
        
        self.donus_butonu = tk.Button(self, text='Ana Sayfa',
                                relief=tk.RAISED, width=10,
                                borderwidth=2,
                                command=lambda: 
                                kontrolcu.cerceve_goster('AnaSayfa'))
        self.donus_butonu.grid(row=2, column= 0)
        
        self.yenile_butonu = tk.Button(self, text="Oyunu Yenile", 
                                relief=tk.RAISED, width=10, 
                                borderwidth=2, 
                                command=lambda: 
                                kontrolcu.sayfa_yenile(['Oyun']))
        self.yenile_butonu.grid(row=2, column=2)
        
        
    
    def soru_butonu(self, buton):
        buton['state'] = tk.DISABLED
        buton['text'] = '?'
        sayfa = tk.Toplevel(self)
        sayfa.wm_title("?")
        sayfa.resizable(width=False, height=False)
        
        kro = Kronometre(sayfa, 60)
        kro.grid(row=4, column=0)
        
        soru_dosyasi = Islemler.dosya_sec()
        soru, betik = Islemler.dosya_formatlayici(soru_dosyasi)
        yrm = Islemler.yorumlayici_bul()
        
        soru_etiketi = tk.Label(sayfa, text=soru,justify=tk.LEFT)
        soru_etiketi.grid(row=1, column=0)
        
        kod_girisi = tk.Text(sayfa,background="black",
                             foreground="yellow")
        kod_girisi.grid(row=2, column=0)
        kod_girisi.insert(tk.END, betik)
        
        def tab(arg):
            print("tab pressed")
            kod_girisi.insert(tk.INSERT, " " * 4)
            return 'break'
        kod_girisi.bind("<Tab>", tab)

        
        def islem():
            kullanıcı_kodu = kod_girisi.get("1.0", tk.END)
            Islemler.cevap_dosyasi(kullanıcı_kodu)
            kullanici_dosyasi = os.path.join(YOL, "cevap.py")
            cozum_cıktısı = Islemler.betik_islet([yrm, soru_dosyasi])
            k_cıktısı = Islemler.betik_islet([yrm, kullanici_dosyasi])
            if cozum_cıktısı[0] == k_cıktısı[0]:
                sonuc_etiketi = tk.Label(sayfa, font=K_TIP_1)
                sonuc_etiketi["text"] = "DOĞRU"
                sonuc_etiketi.grid(row=0, column=0)
                self.puan_etiketi["text"] = str(eval(
                                        self.puan_etiketi["text"]) + 40)
                
            else:
                sonuc_etiketi = tk.Label(sayfa, font=K_TIP_1)
                sonuc_etiketi["text"] = "YANLIŞ"
                sonuc_etiketi.grid(row=0, column=0)
                
                
            
        islem_butonu = tk.Button(sayfa, text="Derle",
                                 relief=tk.RAISED, command=islem)
        islem_butonu.grid(row=3, column=0)
        self.buton_sayisi -= 1

    
    def bonus_butonu(self, buton):
        buton['state'] = tk.DISABLED
        buton['text'] = 'B'
        self.buton_sayisi -= 1
    
    def bos_butonlar(self, buton):
        buton['state'] = tk.DISABLED
        buton['text'] = 'X'
        self.puan_etiketi["text"] = str(eval(
                                        self.puan_etiketi["text"]) + 1)
        
        self.buton_sayisi -= 1

class Ogretici(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
class YuksekSkorlar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

class Islemler:
    """Oyunun altyapıyı ilgilendiren arayüzle bağlantılı,
olmayan işlerini yapan fonksiyonları bulunduran sınıftır."""
    def __init__(self):
        """boş başlatıcı fonksiyon.Sınıfımızdaki metodları örneklemeden
kullanabiliyoruz.Bu yüzden başlatıcı fonksiyonumuz boş."""
        pass
        
    @classmethod
    def harita_yarat(cls, boyutlar=(8,8), esya_listesi=['x', 'b', '?']):
        """Verilen boyutlarda, item listesindeki elemanlar ile
2 boyutlu harita oluşturur.Elemanların bulunma sıklığı, esya
listesindeki elemanların sırasına göre azalır."""
        eksen_x, eksen_y = boyutlar#eksen boyutları değişkene atanır.
        harita = []
        for satir in range(eksen_x):
            bir_satir = []
            for sutun in range(eksen_y):
                random_sayi = rnd.randint(0, 100)#random sayı tutulur.
                if random_sayi == 0 or random_sayi == 100:
                    #random sayı 0 veya 100 ise
                    bir_satir.append(esya_listesi[-1])
                elif random_sayi > 10 and random_sayi < 90:
                    #random sayı 10 ile 80 arasında ise
                    bir_satir.append(esya_listesi[0])
                else:
                    try:
                        #esya listesi 2 elemanlı olarak verilirse
                        #oluşacak hata önlenir.
                        bir_satir.append(rnd.choice(esya_listesi[1:-1]))
                    except IndexError:
                        bir_satir.append(esya_listesi[-1])
            harita.append(bir_satir)
        
        return harita
        
    @classmethod
    def harita_kontrolu(cls, harita, esya_listesi=['x', 'b', '?']):
        """Parametre olarak verilen harita ve esya_listesi ile
bir harita skoru oluşturur.Böylece daha fazla çeşitte eşya
içeren harita daha yüksek skora sahip olur."""
        skor = 0
        for satir in harita:
            for sutun in satir:
                if sutun == esya_listesi[0]:
                    skor += 1
                elif sutun in esya_listesi[1:-1]:
                    skor += 4
                elif sutun == esya_listesi[-1]:
                    skor += 40
        return skor
        
    @classmethod
    def son_haritayi_bul(cls, sayac = 5):
        """Parametre olarak verilen kere harita_olustur
fonksiyonuyla harita oluşturur ve skorunu bulur.En yüksek skora sahip
haritayı son harita olarak döndürür."""
        son_skor = 0
        son_harita = None
        for i in range(sayac):
            harita = cls.harita_yarat()
            ara_skor = cls.harita_kontrolu(harita)
            if ara_skor > son_skor:
                son_skor = ara_skor
                son_harita = harita
            
        return son_harita
        
    @classmethod
    def betik_islet(cls, komut_listesi):
        """komut listesindeki komutlar ile Popen nesnesi
        oluşturur.Komut listesinin çıktılarını ve hatalarını, Popen
        nesnesinin communicate komutuyla yakalar ve çıktı değeri
        olarak döndürür.Bu fonksiyon kullanıcının yazdığı kodları
        bir python dosyasına kaydetmek ve bunu yürüterek
        çıktısını bulmak içindir."""
        surec = sp.Popen(komut_listesi, stdout=sp.PIPE, stderr=sp.PIPE)
        try:
            #popen nesnesi ile bağlantı kurulur ve
            #girilen komutun çıktısı ile verdiği hata
            #bir değişkende tutulur.
            cikti, hata  = surec.communicate(timeout=15)
        except TimeoutExpired:
            surec.kill()
            cikti, hata = surec.communicate()
        #popen nesnesi çıktılar ve hataları byte olarak döndürür.
        #byte'ları utf-8 karakter kodlama sistemine çevirerek
        #anlaşılır çıktılar elde ederiz.
        return cikti.decode("utf-8"), hata.decode("utf-8")
        
    @classmethod
    def yorumlayici_bul(cls):
        """sistem adı platform kütüphanesi system fonksiyonu ile
bulunur.Eğer sistem adı linux ise python 3x yorumlayıcısı nasıl
adlandırılmış o bulunur.bu yorumlayıcı adı olarak ilerde
betik çalıştırmak için tutulur.Eğer sistem windows ise
python yorumlayıcısı python.exe olarak tutulur."""
        sistem_adi = plt.system()#sistem adı bul.
        yorumlayici = None
        if sistem_adi == "Linux":
            cikti, hata = cls.betik_islet(["python3", "-V"])
            if hata == '':#python3 komutu hata yaratmıyorsa
                yorumlayici = "python3"
            else:
                #python3 komutu hata yaratıyorsa python3
                #python komutu ile çağrılıyordur.
                yorumlayici = "python"
        elif sistem_adi == "Windows":
            yorumlayici = "python.exe"
        
        return yorumlayici
        
    @classmethod
    def kaynak_denetimi(cls):
        """programın kullanacağı dosya ve klasörleri
denetler.Eğer varlarsa, işleme devam eder.Yoksa gerekli klasörleri
ve dosyaları oluşturur."""
        if os.path.exists(YOL):
            pass
        else:
            os.mkdir(YOL)
        
        dosya_listesi = ["soru0.py", "soru1.py", "soru2.py", "soru3.py",
                         "soru4.py", "soru5.py", "soru6.py", "soru7.py",
                         "soru8.py", "soru9.py"]
        
        soru0 = """
#Üç kenarı a,b,c değişkenleriyle
#5,6,7 olarak verilmiş bir üçgenin
#alanını hesaplayan aşağıdaki programı tamamlayınız.
a = 5
b = 6
c = 7
s = (a + b + c) / 2
area = (s*(s-a)*(s-b)*(s-c)) ** 0.5
print("Üçgenin alanı {}.".format(area))"""
        
        soru1 = """
#a ve b şeklinde  6 ve 19 olarak belirlenmiş
#değişkenlerin tek mi çift mi olduğunu bulan
#ve yazdıran aşağıdaki programı tamamlayınız.
def tek_cift(sayi):
    if sayi % 2 == 0:
        return "çift"
    else:
        return "tek"
a = 6
b = 19
print("{} sayısı {}tir.".format(a, tek_cift(a)))
print("{} sayısı {}tir.".format(b, tek_cift(b)))"""

        soru2 = """
#1'den 10'a kadar tamsayıların toplamını bulan
# ve yazdıran aşağıdaki programı tamamlayınız.
sonuc = 0
for sayi in range(1, 11):
    sonuc += sayi
print(sonuc)"""

        soru3 = """
#Bir yılın artık yıl olup olmadığını bulan ve
#2017 ile 2000 yıllarının artık olup olmadığını
#yazdıran aşağıdaki programı tamamlayınız.
def artik_yil(yil):
    if (yil % 4) == 0:
        if (yil % 100) == 0:
            if (yil % 400) == 0:
                print("{} artık yıldır.".format(yil))
            else:
                print("{} artık yıl değildir".format(yil))
        else:
            print("{} artık yıldır".format(yil))
    else:
        print("{} artık yıl değildir.".format(yil))
artik_yil(2017)
artik_yil(2000)"""

        soru4 = """
#liste halinde verilmiş 5,8,4,96,2
#sayılarının en büyüğünü bulan ve yazdıran
#aşağıdaki programı tamamlayınız.
sayi_listesi = [5, 8, 4, 96, 2]
sonuc = sayi_listesi[0]
for sayi in sayi_listesi[1:]:
    if sayi > sonuc:
        sonuc = sayi
    else:
        continue
print("{} en büyük sayıdır.".format(sonuc))"""
        
        soru5 = """
#5 ve 7 sayısının faktöriyel değerini
#bulan ve yazdıran aşağıdaki programı tamamlayınız.
def faktoriyel_bul(sayi):
    if sayi == 0:
        return 1
    else:
        return sayi * faktoriyel_bul(sayi - 1)
print("{} in faktöriyeli {}".format(5, faktoriyel_bul(5)))
print("{} in faktöriyeli {}".format(7, faktoriyel_bul(7)))"""

        soru6 = """
#1'den 5'e kadar olan sayıların karesini ve küpünü
#içeren 2 boyutlu bir liste üreten aşağıdaki fonksiyonu
#tamamlayınız.(bir satır 'sayı, karesi, küpü' şeklindedir.)
iki_boyut_liste = []
for i in range(1, 6):
    satir = [i, i**2, i**3]
    iki_boyut_liste.append(satir)
print(iki_boyut_liste)"""

        soru7 = """
#çekoslovakyalılaştıramadıklarımızdanmısınız
#harf dizisinde her harften kaç tane olduğunu
#bulan ve '... harfinden ... tane vardır.'
#şeklinde yazdıran aşağıdaki programı tamamlayınız.
def harf_sayici(kelime):
    veri_sozlugu = {}
    for harf in kelime:
        if harf in veri_sozlugu.keys():
            veri_sozlugu[harf] += 1
        else:
            veri_sozlugu[harf] = 1
    for sozcuk, sayisi in veri_sozlugu.items():
        print("{} harfinden {} tane vardır.".format(sozcuk, sayisi))
harf_sayici("çekoslovakyalılaştıramadıklarımızdanmısınız")"""

        soru8 = """
#[[12, 15, 27]
# [20, 22, 45]
# [8, 10, 97]] 2 boyutlu listesinden 5'e
#tam bölünebilen sayıları bulup yazdıran aşağıdaki
#programı tamamlayınız.
liste = [[12, 15, 27]
         [20, 22, 45]
         [8, 10, 97]]
for satir in liste:
    for sayi in satir:
        if sayi % 5 == 0:
            print("{} sayisi 5 ile bölünür.".format(sayi))"""
        
        soru9 = """
#6. ve 10. sıradaki fibonacci sayılarını bulan
#ve bu sayıları yazdıran aşağıdaki programı tamamlayınız.
def fibonacci_bul(sayi_sirasi):
    if sayi_sirasi < 2:
        return 1
    return fibonacci_bul(sayi_sirasi-1) + fibonacci_bul(sayi_sirasi-2)
print("{}. sıradaki fibonacci sayısı {}.".format(6, fibonacci_bul(6)))
print("{}. sıradaki fibonacci sayısı {}.".format(10, fibonacci_bul(10)))
"""
        
        for dosya in dosya_listesi:
            if os.path.exists(YOL + os.sep + dosya):
                pass
            else:
                yeni_dosya = open(YOL + os.sep + dosya, 'w')
                yeni_dosya.write(eval(dosya[0:5]))
                yeni_dosya.close()
        
                
    @classmethod
    def dosya_formatlayici(cls, dosya_adi):
        """Python betik dosyalarını, programda
kullanılabilecek şekilde formatlar.Başı # işareti ile
başlayan soru satırlarını soru metni, kod satırlarını
kod metni olarak döndürür."""
        soru_metni = """""" 
        betik = """"""
        dosya_nesnesi = open(dosya_adi, 'r')
        
        for satir in dosya_nesnesi.readlines():
            if satir[0] == '#':
                yeni_satir = satir.replace('#', '')
                soru_metni += yeni_satir
            elif satir == os.linesep:
                pass
            else:
                if rnd.randint(0,10) % 2 == 0:
                    betik += satir
                else:
                    betik += "<-------->" + os.linesep
        dosya_nesnesi.close()
                
        return soru_metni, betik
    
    @classmethod
    def dosya_sec(cls):
        """soru dosyaları arasından rastgele bir
dosyayı seçer ve okunmak için döndürür."""
        dosya_listesi = os.listdir(YOL)
        rastgele_dosya = rnd.choice(dosya_listesi)
        
        return os.path.join(YOL, rastgele_dosya)
        
    @classmethod    
    def cevap_dosyasi(cls, metin):
        dosya = open(os.path.join(YOL, "cevap.py"), 'w')
        dosya.write(metin)
        dosya.close()
        
class Kronometre(tk.Label):
    def __init__(self, tasiyici, sure, eylem="destroy"):
        super().__init__(tasiyici)
        self.tasiyici = tasiyici
        self.sure = sure
        self.eylem = eylem
        self["text"] = self.sure
        self["font"] = TIP_1
        self.islem()
    
    def islem(self):
        if self.sure <= 0:
            if self.eylem == "destroy":
                self.tasiyici.destroy()
            else:
                pass
        else:
            self.configure(text="{}".format(self.sure))
            self.sure -= 1
            self.tasiyici.after(1000, self.islem)
            
            
        
        
if __name__ == "__main__":
    app = CarePython()
    app.mainloop()