Masinska vizija. (master predmet)
=================================

Obrada slike je napravljena tako da detektuje diode koje su ukljucene, i to
radi. Poenta je napraviti da radi u svakom slucaju. A to znaci da se pomera
kamera i to pod raznim uslovima osvetljenja.

U trenutnoj postavci postoje slike koje su slikane kada je tastatura ukljucena
skroz i pod razlicitim uslovima osvetljenja. U tim slucajevima koji su dati
radi, samo ponekad sam drzac za kameru pravi probleme algoritmu.

Napraviti setap tako da se lako moze integrisati algoritam sa LIVE kamerom, da
se proveri taj nacin rada.

POTREBNO URADITI:
=====================
* Strukturirati kod i napraviti logicke celine, po mogucstvu funkciju za
  procesing, sa vracenom obradjenom slikom. Ili to nije potrebno?
* Iskomentarisati kod.
* Javiti se Mariji sa trenutnim rezultatima.
* Krenuti sa gledanjem pomeranja kamere u ovom slucaju? Kako postici da se
  odredi sa pokretanjem kamere?
* Pogledati da li isti kod radi i na Windows-u pod Anaconda Navigator-om?

OPIS TRENUTNOG STANJA:
======================
Kalibracija napravljena na nacin kako je opisano, sa 10 uzetih snimaka, i
napravljena tako da posle 10 snimaka ima sigurne diode. Tj da ima pozicije
dioda gde se one sigurno nalaze, nakon cega je moguce preci na procesing.
U odeljku procesinga, napravljena jednostavna obrada slike, kao i u kalibraciji
pre nego se dodje do funkcije za prepoznavanje krugova. Nakon cega, usled
sigurne pozicije dioda, moze se odrediti stanje diode (ukljucena/iskljucena)
iz binarizovane slike (da li se na mestu centra kruga nalazi nula ili 255,
ukoliko je nula = iskljuceno, obrnuto = ukljuceno).
Iscrtavanje centara kruga napravljeno nakon procesinga, kao cist pokazatelj
toga gde se diode nalaze. I gde treba da se odredjuje stanje.

OPIS KALIBRACIJE:
======================
Napraviti setap tako da je kamera fiksna u odnosu na tastaturu. Sto je moguce
ako se iskoristi onaj srdjanov vec postojeci deo.
Kad se fiksira kamera u odnosu na tastaturu, uzeti prvih nekoliko snimaka, kada
je tastatura ukljucena u celosti, i proveriti da li puno odstupa nalazenje
dioda. Kada se nadje svih 18 dioda, i da polozaj pronalazaka ne odstupa
previse, u na primer 10 prvih frejmova, moze da se kaze da je kalibracija
zavrsena. Tad se fiksiraju pozicije. Poslednja na primer 3 frejma, zaokruzene
koordinate centara krugova, i to se smesta u jednu strukturu koja je zakucana i
na koju se posle ugleda sve.

OPIS RADA:
======================
Nakon kalibracije, krece se sa normalnim radom cele strukture. To znaci da se
diode preko CAN interfejsa pale i gase onako kako se zada, a da alogirtam treba
da loguje u svakom trenutku koja je upaljena ili ugasena. I da se to prikazuje
u svakom trenutku na izlazu (kao stanje dioda). Sve dok se ne prekine
izvrsavanje nekim signalom, na primer pritisak Q ili q. Vidi ovo jos.

OPIS LOG PODATAKA:
======================
Drugi izgled log podatka koji ce se prikazivati na izlazu:

        DIDOE   |1a|1b|1c|2a|2b|2c|3a|3b|3c|4a|4b|4c|5a|5b|5c|6a|6b|6c|
        STANJE  |10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|10|

--------------------------------------------------------------------------------

OPIS ALGORITMA:
======================
Ideja realizacije:
- koristiti openCV bibloteku za Python3.(done)
- koristiti fiksnu kameru u pocetku.(done)[koriste se slike koje je Srdjan
  uslikao]
- registrovati kameru kao ulaz, sa nje kupiti slike(done)[napravljeno da live
  strimuje]{ostalo napraviti setap sa tastaturom koja radi}
=> za pocetak uzeti nekoliko snimaka
- izfiltrirati sliku tako da se mane koje unosi kamera odstrane(done)
--> filtriranje:
	koristiti GREY sliku(done)
	odseci delove oko tastature, tako da oni ne uticu u slici (za pocetak)
	(nalepiti izolir traku okolo, tako da sve bude crno, i da se ne vide
        supljine koje je srjan izbusio za solenoide)(NOT DONE)
	(probati) odraditi ekvalizaciju histograma, tako da se dobije jasna slika
	ispeglati nesavrsenosti (na primer neki Gaus, ili mozda cisto filtriranje
        usrednjavanjem)(done)[uradjena ekvalizacija histograma, gausovo
        filtriranje i binarizacija]
	- naci neki algoritam za detekciju obrasca (pattern
          matching)(done)[Hough Circles algoritam iskoriscen, opisati ga]
	- naci neki algoritam za detekciju krugova (posto su diode pravilnog oblika)
	odbaciti sve lose pronalaske (backlight dugmadi, ili detektovati i njih???)
- koristiti jednu sliku koja je dobro uslikana kao referencu gde se nalaze didode
(neka vrsta mape)
	(na ovaj nacin ce se dobiti sigurne pozicije dioda na tastaturi)
        [NOT DONE]
- svaku sledecu sliku uzfiltrirati na isti nacin i naci diode(NOT DONE)
- uporediti sa vec postojecom mapom, i odrediti koja fali(NOT DONE)
- na taj nacin ce se dobiti prepoznavanje koja dioda je ukljucena, koja
  iskljucena(NOT DONE)

--------------------------------------------------------------------------------

U ovom dokumentu ce se nalaziti revizija koda koji je Srdjan napisao za obradu
slike sa kamere. I koji je potrebno ja da unapredim i dokumentujem kako bih ga
predao kao projekat za predmet Masinska vizija.

Cilj projekta je detekcija stanja dioda na tastaturi uz pomoc kamere koja ce se
pokretati. Pokreti kamere su za sada sekundarna stvar, i cilj je pronaci i
detektovati stanje dioda na tastaturi, tako da se dobija veran prikaz stanja na
tastaturi iz programa koji ce se pokretati sa openCV bibliotekom.
Pokreti kamere ce se implementirati tek nakon komunikacije sa asistentkinjom, i
kada staticna kamera bude davala 100% rezultate. Tj kada algoritam obrade slike
bude ispeglan, tako da ce pokreti biti samo dodatak vec postojecem programu.

Srdjan je u sklopu projekta za Liebherr vec uradio obradu slike, i dobijanje
rezultata, po njegovom izvestaju, u 100% slucajeva. U ovom dokumentu ce se
nalaziti revizija tog koda i to u smislu da se sto vise rasclani i uvide
nedostaci, i mesta za poboljsanje.

Ideja realizacije:
- koristiti openCV bibloteku za Python3.
- koristiti fiksnu kameru u pocetku.
- registrovati kameru kao ulaz, sa nje kupiti slike
=> za pocetak uzeti nekoliko snimaka
- izfiltrirati sliku tako da se mane koje unosi kamera odstrane
--> filtriranje:
	koristiti GREY sliku
	odseci delove oko tastature, tako da oni ne uticu u slici (za pocetak)
	(nalepiti izolir traku okolo, tako da sve bude crno, i da se ne vide supljine koje je srjan izbusio za solenoide)
	(probati) odraditi ekvalizaciju histograma, tako da se dobije jasna slika
	ispeglati nesavrsenosti (na primer neki Gaus, ili mozda cisto filtriranje usrednjavanjem)
	- naci neki algoritam za detekciju obrasca (pattern matching)
	- naci neki algoritam za detekciju krugova (posto su diode pravilnog oblika)
	odbaciti sve lose pronalaske (backlight dugmadi, ili detektovati i njih???)
- koristiti jednu sliku koja je dobro uslikana kao referencu gde se nalaze didode (neka vrsta mape)
	( na ovaj nacin ce se dobiti sigurne pozicije dioda na tastaturi)
- svaku sledecu sliku uzfiltrirati na isti nacin i naci diode
- uporediti sa vec postojecom mapom, i odrediti koja fali
- na taj nacin ce se dobiti prepoznavanje koja dioda je ukljucena, koja iskljucena

Primer Mape:
(Tastatura ima 3 reda sa po 2 dugmeta, i iznad svakog dugmeta 3 diode)
	| #1 dugme  | #2 dugme  |
----------------------------------
#1 red	| D | D | D | D | D | D |
----------------------------------
#2 red	| D | D | D | D | D | D |
----------------------------------
#3 red	| D | D | D | D | D | D |
----------------------------------
D = 1/0 u zavisnosti od toga da li je dioda ukljucena ili ne ( 1 = ON; 0 = OFF)

Revizija koda:
- main.py- main fajl u kome se sve inicijalizuje i gde se pokrecu odredjeni testovi koji su napravljeni
	 - najzanimljivije su funkcije unutar Keyboard.py koje se odnose na obradu slike: testLEDs, testBacklight
	 - unutar testLEDs and testBacklight se pozivaju fukncije za postavljanje promenu LED statusa preko CAN-a
	 i promenu Backlight-a
- Keyboard.py   - fajl u kome se nalaze implementirane funkcije za citanje statusa LED-ova i Backlight-a
	        - readLEDStatus(self):
		=> inicijalizuje se kamera za koriscenje, uzima nekoliko frejmova, i poziva findLEDs iz imageProcessing.py
			=> koristi se funkcija getLEDLocation() koja se nalazi u Keyboard.py
			=> kalibrisu se lokacije dugmadi na osnovu pozicije dioda (valjda??)
		- readBacklight(self):
			=> slicno kao i za LEDStatus
			=> poziva se isBacklightON iz imageProcessing.py
