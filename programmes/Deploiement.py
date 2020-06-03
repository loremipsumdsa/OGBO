##########################################       parametre de la base      ##############################################################
import mysql.connector
user="paul"
pw="headvoice"
host="localhost"
database="test1"
mydb=mysql.connector.connect(host=host, user=user,password=pw,database=database)
cursor=mydb.cursor()

##########################################       intervention      ##############################################################
cmdAdI="INSERT INTO intervention(designation, praticien, IDN) VALUES (%s, %s, %s)"

cursor.execute("CREATE TABLE IF NOT EXISTS intervention (designation VARCHAR(100), praticien VARCHAR(100), IDN INT)")

interv1=("decoupe du foi","Jeanne Deferlin","3")
interv2=("ablation du cerveau","Jeanne Deferlin)","7")
interv3=("greffe de graisse","Antonio Barabas)","31")
interv4=("rien du tout","Bruno Janiste","43")
interv5=("controle technique","Jeanne Deferlin","45")
interv6=("rien du tout","Bernard Lemalin","68")

cursor.execute(cmdAdI,interv1)
cursor.execute(cmdAdI,interv2)
cursor.execute(cmdAdI,interv3)
cursor.execute(cmdAdI,interv4)
cursor.execute(cmdAdI,interv5)
cursor.execute(cmdAdI,interv6)


##########################################       praticien      ##############################################################
cmdAdP="INSERT INTO praticien(name) VALUES (%s)"

cursor.execute("CREATE TABLE IF NOT EXISTS praticien (name VARCHAR(100))")

praticien1=("Jeanne Deferlin")
praticien2=("Abdel Mirat")
praticien3=("Francis Compet")
praticien4=("Friman Joukansky")
praticien5=("Antonio Barabas")
praticien6=("Philippe Esti Moniron")

cursor.execute(cmdAdI,interv1)
cursor.execute(cmdAdI,interv2)
cursor.execute(cmdAdI,interv3)
cursor.execute(cmdAdI,interv4)
cursor.execute(cmdAdI,interv5)
cursor.execute(cmdAdI,interv6)


##########################################       demande      ##############################################################
cmdAdDem="INSERT INTO demande(patient, NIR, praticien, intervention, INI, NCB, DF, temps) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

cursor.execute("CREATE TABLE IF NOT EXISTS demande (id INT AUTO_INCREMENT PRIMARY KEY, patient VARCHAR(100), NIR VARCHAR(100), praticien VARCHAR(100), intervention VARCHAR(100), INI INT, NCB VARCHAR(100), DF VARCHAR(100),temps INT)")

dem1=("Francois Pedro","1 76 37 67 989 863 36", "Jeanne Deferlin","decoupe du foie","143","intervention urgente","15/10/2018","40")
dem2=("Billy Birman","1 76 37 67 989 863 36","Abdel Mirat","appendicite","13","fin de journée si possible","14/10/2018","50")
dem3=("Erman Dutryk","1 76 37 67 989 863 36","Francis Compet","greffe de moele", "7","","15/10/2018","30")
dem4=("Philippe Motas","1 76 37 67 989 863 36","Friman Joukansky","greffe de graisse","89","les noms d'interventions faites pas gaffe","16/10/2018","40")
dem5=("Louise Label","1 76 37 67 989 863 36","Louane Jermin","rien du tout", "54","penser a changer tout ca si on fait une demo","5/10/2018","40")
dem6=("Francois Pedro","1 76 37 67 989 863 36","Philippe Esti Moniron","controle technique","53","plouf","17/10/2018","70")

cursor.execute(cmdAdDem,dem1)
cursor.execute(cmdAdDem,dem2)
cursor.execute(cmdAdDem,dem3)
cursor.execute(cmdAdDem,dem4)
cursor.execute(cmdAdDem,dem5)
cursor.execute(cmdAdDem,dem6)

mydb.commit()





##########################################       plage      ##############################################################
cmdAdPlag="INSERT INTO plage(praticien, jour, heure, temps, salle) VALUES (%s, %s, %s, %s, %s)"

cursor.execute("CREATE TABLE IF NOT EXISTS plage(id INT AUTO_INCREMENT PRIMARY KEY, praticien VARCHAR(100),jour VARCHAR(100), heure VARCHAR(100), temps INT, salle INT)")

plage1=("Jeanne Deferlin","04/05/2018","08:20","120","1")

cursor.execute(cmdAdPlag,plage1)
mydb.commit()




##########################################       Prevu      ##############################################################
cmdAdPrev="INSERT INTO prevu(patient, NIR, praticien, intervention, INI, NCB, DF, jour, heure, temps, salle) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

cursor.execute("CREATE TABLE IF NOT EXISTS prevu (id INT AUTO_INCREMENT PRIMARY KEY, patient VARCHAR(100), NIR VARCHAR(100), praticien VARCHAR(100), intervention VARCHAR(100), INI INT, NCB VARCHAR(100), DF VARCHAR(100), jour VARCHAR(100), heure VARCHAR(100), temps INT, salle INT)")

prev1=("Francois Pedro","1 76 37 67 989 863 36", "Jeanne Deferlin","decoupe du foie","143","intervention urgente","15/10/2018","5/5/2019","08:20","40","1")
prev2=("Billy Birman","1 76 37 67 989 863 36","Abdel Mirat","appendicite","13","fin de journée si possible","14/10/2018","5/5/2019","09:00","50","1")
prev3=("Erman Dutryk","1 76 37 67 989 863 36","Francis Compet","greffe de moele", "7","","15/10/2018","5/5/2019","10:00","30","1")
prev4=("Philippe Motas","1 76 37 67 989 863 36","Friman Joukansky","greffe de graisse","89","les noms d'interventions faites pas gaffe","16/10/2018","5/5/2019","08:00","40","2")
prev5=("Louise Label","1 76 37 67 989 863 36","Louane Jermin","rien du tout", "54","penser a changer tout ca si on fait une demo","5/10/2018","17/5/2019","11:20","40","2")
prev6=("Francois Pedro","1 76 37 67 989 863 36","Philippe Esti Moniron","controle technique","53","plouf","17/10/2018","5/5/2019","08:10","70","3")
prev7=("Mikael Nasson","1 76 37 67 989 863 36","Philippe Esti Moniron","rendre inteligent","84","tous pour un","15/10/2018","5/5/2019","09:30","40","3")
prev8=("David Blimouri","1 76 37 67 989 863 36","Louane Jermin","decoupe du foie","125","i feel good","15/10/2018","5/5/2019","10:10","30","3")
prev9=("Neter Blema","1 76 37 67 989 863 36","Friman Joukansky","ablation du cerveau","6","piou piou piou","14/10/2018","5/5/2019","10:55","80","3")
prev10=("Jouan Freu","1 76 37 67 989 863 36","Francis Compet","rien du tout","17","mais la musique est top","15/10/2018","5/5/2019","12:20","40","3")
prev11=("Nathan Blermic","1 76 37 67 989 863 36","Jeanne Deferlin","ablation du cerveau","19","super pratique ces commentaires","16/10/2018","5/5/2019","14:00","50","3")
prev12=("Jean Baptiste Tifon","1 76 37 67 989 863 36","Abdel Mirat","rien du tout","43","ok on manque d'idée","15/10/2018","5/5/2019","15:00","40","3")
prev13=("George Nites","1 76 37 67 989 863 36","Louane Jermin","ablation du cerveau","16","voila voila voila...","15/10/2018","5/5/2019","15:50","40","3")

cursor.execute(cmdAdPrev,prev1)
cursor.execute(cmdAdPrev,prev2)
cursor.execute(cmdAdPrev,prev3)
cursor.execute(cmdAdPrev,prev4)
cursor.execute(cmdAdPrev,prev5)
cursor.execute(cmdAdPrev,prev6)
cursor.execute(cmdAdPrev,prev7)
cursor.execute(cmdAdPrev,prev8)
cursor.execute(cmdAdPrev,prev9)
cursor.execute(cmdAdPrev,prev10)
cursor.execute(cmdAdPrev,prev11)
cursor.execute(cmdAdPrev,prev12)
cursor.execute(cmdAdPrev,prev13)

mydb.commit()





##########################################       en cours      ##############################################################
cmdAdPrev="INSERT INTO encours(patient, NIR, praticien, intervention, INI, NCB, DF, jour, heure, temps, salle, statut, raison, estimation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

cursor.execute("CREATE TABLE IF NOT EXISTS encours (id INT AUTO_INCREMENT PRIMARY KEY, patient VARCHAR(100), NIR VARCHAR(100), praticien VARCHAR(100), intervention VARCHAR(100), INI INT, NCB VARCHAR(100), DF VARCHAR(100), jour VARCHAR(100), heure VARCHAR(100), temps INT, salle INT, statut VARCHAR(100), raison VARCHAR(100), estimation VARCHAR(100))")

prev1=("Francois Pedro","1 76 37 67 989 863 36", "Jeanne Deferlin","decoupe du foie","143","poutintouta","15/10/2018","17/4/2019","08:20","40","1","incision","", " " )
prev2=("Billy Birman","1 76 37 67 989 863 36","Abdel Mirat","ablation du cerveau","13","poutintouta","14/10/2018","17/4/2019","09:00","50","2", "fermeture", "", " ")
prev3=("Erman Dutryk","1 76 37 67 989 863 36","Francis Compet","greffe de graisse", "7","je suis ton pere","15/10/2018","17/4/2019","10:00","30","3", "annulee", "risque d'alergie", " ")
prev4=("Philippe Motas","1 76 37 67 989 863 36","Friman Joukansky","ablation du cerveau","89","Shara conor?","16/10/2018","17/4/2019","08:00","40","5", "incision", "", " ")
prev5=("Louise Label","1 76 37 67 989 863 36","Louane Jermin","rien du tout", "54","et tu reconnaitreras le serviteur de l'eternel","15/10/2018","17/04/2019","11:20","40","4", "sortie", "", " ")
prev6=("Francois Pedro","1 76 37 67 989 863 36","Philippe Esti Moniron","controle technique","53","plouf","17/10/2018","17/4/2019","08:10","70","6", "induction", ""," ")
prev7=("Mikael Nasson","1 76 37 67 989 863 36","Philippe Esti Moniron","rendre inteligent","84","tous pour un","15/10/2018","17/4/2019","09:30","40","7", "installation", ""," ")
prev8=("David Blimouri","1 76 37 67 989 863 36","Louane Jermin","decoupe du foie","125","i feel good","15/10/2018","16/04/2019","10:10","30","8", "retard", "On a oublié une spatule","10")
prev9=("Neter Blema","1 76 37 67 989 863 36","Friman Joukansky","ablation du cerveau","6","captain on manque d'idée","14/10/2018","16/4/2019","10:55","80","9", "fermeture", "", " ")

cursor.execute(cmdAdPrev,prev1)
cursor.execute(cmdAdPrev,prev2)
cursor.execute(cmdAdPrev,prev3)
cursor.execute(cmdAdPrev,prev4)
cursor.execute(cmdAdPrev,prev5)
cursor.execute(cmdAdPrev,prev6)
cursor.execute(cmdAdPrev,prev7)
cursor.execute(cmdAdPrev,prev8)
cursor.execute(cmdAdPrev,prev9)

mydb.commit()





##########################################       historique      ##############################################################
cursor.execute("CREATE TABLE IF NOT EXISTS historique (id INT AUTO_INCREMENT PRIMARY KEY, patient VARCHAR(100), NIR VARCHAR(100), praticien VARCHAR(100), intervention VARCHAR(100), INI INT, NCB VARCHAR(100), DF VARCHAR(100), jour VARCHAR(100), salle INT, heureP VARCHAR(100), tempsP INT, heureD VARCHAR(100), heureF VARCHAR(100), imprevu VARCHAR(100), raison VARCHAR(100))")
mydb.commit()
