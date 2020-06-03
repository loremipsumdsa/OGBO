
from tkinter import *
from tkinter.messagebox import *
import time
import mysql.connector
from tkinter.font import Font
import calendar
from datetime import datetime

mode="plage"

user="paul"
pw="headvoice"
host="localhost"
database="test1"
mydb=mysql.connector.connect(host=host, user=user,password=pw,database=database)
cursor=mydb.cursor()
#Parametres de base du programme; tout les parametres grahpiques en decoulent
heureD=8
heureF=20
largeur = 1200
hauteur = 1000

#Parametre decoulants des parametres de base du programme
longueurSalle=11/15*largeur
hauteurSalle=1/25*hauteur
coordXSalle=1/12*largeur
coefCoordYSalle=1/20*hauteur

coordYReserve=7/10*hauteur
coordYAxeTemps=3/25*hauteur

ajCoordYSalle=1/10*largeur
ajEtiquetteSalle=2/60*largeur
ajEtiquetteAxeTemps=1/80*largeur


coordXJour=largeur/2
coordYJour=hauteur/15
ajPSY=10
ajPX=-80-hauteurSalle/2
ajSX=100-hauteurSalle/2
codeCouleur={"Jeanne Deferlin":"purple","Francis Compet":"green","Friman Joukansky":"yellow","Louane Jermin":"brown","Philippe Esti Moniron":"orange","Abdel Mirat":"black","Mathieu Gigoudi":"Yellow","Arim Sliman":"gray"}

decalageJ=0
ljour=[]
now=datetime.now()
now.year
for m in range (1,13):
    ms=calendar.monthcalendar(now.year-1,m)
    for s in ms:
        for j in s:
            if j!=0:
                ljour.append(str(j)+"/"+str(m)+"/"+str(now.year-1))
for m in range (1,13):
    ms=calendar.monthcalendar(now.year,m)
    for s in ms:
        for j in s:
            if j!=0:
                ljour.append(str(j)+"/"+str(m)+"/"+str(now.year))
for m in range (1,13):
    ms=calendar.monthcalendar(now.year+1,m)
    for s in ms:
        for j in s:
            if j!=0:
                ljour.append(str(j)+"/"+str(m)+"/"+str(now.year+1))


def nouvellePlage():

    # Creation fenetre + Frame de base + Bouton validation
    formulaire=Tk()
    formulaire.title("Formulaire")
    formulaireF=Frame(formulaire, borderwidth=2,relief=GROOVE)
    ok=Button(formulaire, text="Valider", command=creationPlage)
    
    #Creation Frames formulaire
    praticienF=Frame(formulaireF)
    dureeF=Frame(formulaireF)

    #Creation Labels formulaire
    praticienL=Label(praticienF, text="Nom du praticien            ")
    dureeL=Label(dureeF, text="Durée de la plage (en min)          ")


    #Creation champs formulaire
    global praticienC
    global dureeC
    praticienC=Listbox(praticienF, width=20, height=3,exportselection=0)
    praticienC.insert(0,"Jeanne Deferlin")
    praticienC.insert(1,"Mathieu Gigoudi")
    praticienC.insert(2,"Arim Sliman")
    praticienC.insert(3,"Marc Djic")
    praticienC.insert(4,"Ziva Lechat")
    
    
    dureeC=Entry(dureeF)


    #Placement Champs et labels formulaire
    praticienC.pack(side=RIGHT)
    praticienL.pack(side=LEFT)

    dureeC.pack(side=RIGHT)
    dureeL.pack(side=LEFT)

    praticienF.pack()
    dureeF.pack()


    #placement Frames de base + bouton validation et annulation ouverture fenetre
    formulaireF.pack(side=TOP)
    ok.pack(side=BOTTOM, padx = 10, pady = 10)
    formulaire.mainloop()



def creationPlage():
    print("une plage va etre créé")
    cmdAdPlag="INSERT INTO plage(praticien, jour, heure, temps, salle) VALUES (%s, %s, %s, %s, %s)"
    jour=jourAc()[0]
    plage=(praticienC.get(praticienC.curselection()[0]), jour,"08:00", str(dureeC.get()),'0')
    cursor.execute(cmdAdPlag,plage)
    mydb.commit()
    ajd=jourAc()
    CreerPlanning(ajd[0],"plage")





class Rdv:

    #Class des representant graphique des RDVs
    #Chaque objet correspond a une ligne de la table specifique
    #un RDV est definis par un praticien, un IN, un patient, une salle, une date, une heure, un temps et une note au cadre de bloc
    #La representation grahpique necessite les attributs de coordonnés, de de dimensions et de couleur
        
    def __init__(self,info):

        global planning
        print("creation rdv")
        self.identifiant=info[0]
        self.all=info
        print(self.all)
        
        #Attributs recuperés depuis la table
        self.praticien=self.all[3]
        self.IN=self.all[5]
        self.patient=self.all[1]
        self.salle=self.all[11]
        self.jour=self.all[8]
        self.heure=self.all[9]
        self.temps=self.all[10]
        self.NCB=self.all[6]
        
        #Attributs deduits des valeurs recuperés depuis la table
        self.coordX=minInPx(int(self.heure[0]+self.heure[1])*60+int(self.heure[3]+self.heure[4]))
        for salle in salles:
            if salle.numero==self.salle:
                self.coordY=salle.coordY
                break
        self.long=qMinInPx(int(self.temps))
        self.couleur=codeCouleur[self.praticien]

        #Attributs constants
        self.haut=hauteurSalle

        #Attributs d'état
        self.clic=False

        #Attributs graphiques
        self.representation=planning.create_rectangle(self.coordX,self.coordY,self.coordX+self.long,self.coordY+self.haut,fill=self.couleur)
        

    def clique(self,etat): #Mutateur d'état
        self.clic=etat

    def estclique(self): #Accesseur d'état
            return self.clic

    def estSelectionné(self, event): #Accesseur d'état
        if event.x>=self.coordX and event.x<=self.coordX+self.long and event.y>=self.coordY and event.y<=self.coordY+self.haut :
            return True
        else :return False

    def place(self, event): #placement dynamique
        global planning
        self.coordX=event.x
        self.coordY=event.y
        planning.coords(self.representation,self.coordX,self.coordY,self.coordX+self.long,self.coordY+self.haut)

    def placeD(self,coordX,coordY): #placement direct
        global planning
        planning.coords(self.representation,coordX,self.haut,coordX+self.long,coordY)
        
        
    def placeDans(self,salle,event): #placement assisté
            if event.x+self.long>=coordXSalle+longueurSalle:
                print("la")
                self.coordX=coordXSalle+longueurSalle-self.long
            else:
                self.coordX=event.x
            self.heure=pxInHm(self.coordX)
            self.jour=ljour[ajd[1]+decalageJ]
            self.coordY=salle.coordY
            planning.coords(self.representation,self.coordX,self.coordY,self.coordX+self.long,self.coordY+self.haut)
            self.salle=str(salle.numero)

    def supprimer(self):
        global decalageJ
        cursor.execute("DELETE from prevu WHERE id="+str(self.identifiant))
        mydb.commit()
        ajd=jourAc()
        CreerPlanning(ljour[ajd[1]+decalageJ],"rdv")
        
    def afficher(self): #affichage informatif
            text='Praticien: '+self.praticien+ "\n Date: "+ self.jour + " "+self.heure+ "\n temps estimé: "+ str(self.temps)+" minutes\n Patient: "+self.patient+"\n Salle: "+str(self.salle)+"\n Note au cadre de Blocs: "+self.NCB

            fen = Toplevel()
            fen.title("infos RDV")
            fen.configure(bg = "white")
            infoLab = Label(fen, text=text, bg = "white")
            infoLab.pack(side=TOP)
            supprimer = Button(fen, text="Supprimer",bg="gray", width=10, command=self.supprimer)
            supprimer.pack(side=BOTTOM)

    def estDansSalle(self,salle):
        return str(self.salle)==str(salle)

    def enregistrer(self):
        print("enregistrement rdv")
        cursor.execute("UPDATE prevu SET heure='"+self.heure+"', jour='"+self.jour+"', salle='"+str(self.salle)+"' WHERE id="+str(self.identifiant))
        mydb.commit()


        
    
    
class Plage:

    #Class des representant graphique des RDVs
    #Chaque objet correspond a une ligne de la table specifique
    #un RDV est definis par un praticien, un IN, un patient, une salle, une date, une heure, un temps et une note au cadre de bloc
    #La representation grahpique necessite les attributs de coordonnés, de de dimensions et de couleur
        
    def __init__(self,info):

        global planning
        print("creation plage")
        self.identifiant=info[0]
        self.all=info
        print(self.all)
        
        #Attributs recuperés depuis la table
        self.praticien=self.all[1]
        self.salle=self.all[5]
        self.jour=self.all[2]
        self.heure=self.all[3]
        self.temps=self.all[4]
        
        #Attributs deduits des valeurs recuperés depuis la table
        self.coordX=minInPx(int(self.heure[0]+self.heure[1])*60+int(self.heure[3]+self.heure[4]))
        for salle in salles:
            if salle.numero==self.salle:
                self.coordY=salle.coordY
                break
        self.long=qMinInPx(int(self.temps))
        self.couleur=codeCouleur[self.praticien]

        #Attributs constants
        self.haut=hauteurSalle

        #Attributs d'état
        self.clic=False

        #Attributs graphiques
        self.representation=planning.create_rectangle(self.coordX,self.coordY,self.coordX+self.long,self.coordY+self.haut,fill=self.couleur)
        

    def clique(self,etat): #Mutateur d'état
        self.clic=etat

    def estclique(self): #Accesseur d'état
            return self.clic

    def estSelectionné(self, event): #Accesseur d'état
        if event.x>=self.coordX and event.x<=self.coordX+self.long and event.y>=self.coordY and event.y<=self.coordY+self.haut :
            return True
        else :return False

    def place(self, event): #placement dynamique
        global planning
        self.coordX=event.x
        self.coordY=event.y
        planning.coords(self.representation,self.coordX,self.coordY,self.coordX+self.long,self.coordY+self.haut)

    def placeD(self,coordX,coordY): #placement direct
        global planning
        planning.coords(self.representation,coordX,self.haut,coordX+self.long,coordY)
        
        
    def placeDans(self,salle,event): #placement assisté
            if event.x+self.long>=coordXSalle+longueurSalle:
                print("la")
                self.coordX=coordXSalle+longueurSalle-self.long
            else:
                self.coordX=event.x
            self.heure=pxInHm(self.coordX)
            self.jour=ljour[ajd[1]+decalageJ]
            self.coordY=salle.coordY
            planning.coords(self.representation,self.coordX,self.coordY,self.coordX+self.long,self.coordY+self.haut)
            self.salle=str(salle.numero)


    def supprimer(self):
        global decalageJ
        cursor.execute("DELETE from plage WHERE id="+str(self.identifiant))
        mydb.commit()
        ajd=jourAc()
        CreerPlanning(ljour[ajd[1]+decalageJ],"plage")
        
    def afficher(self): #affichage informatif
            text='Praticien: '+self.praticien+ "\n Date: "+ self.jour + " "+self.heure+ "\n Durée de la plage: "+ str(self.temps)+"\n Salle: "+str(self.salle)

            fen = Toplevel()
            fen.title("info salle")
            fen.configure(bg = "white")
            infoLab = Label(fen, text=text, bg = "white")
            infoLab.pack(side=TOP)
            supprimer = Button(fen, text="Supprimer",bg="gray", width=10, command=self.supprimer)
            supprimer.pack(side=BOTTOM)

    def estDansSalle(self,salle):
        return str(self.salle)==str(salle)

    def enregistrer(self):
        print("enregistrement plage")
        print(self.heure)
        cursor.execute("UPDATE plage SET heure='"+self.heure+"', jour='"+self.jour+"', salle='"+str(self.salle)+"' WHERE id="+str(self.identifiant))
        mydb.commit()

class Salle:

    #Class des representant graphique des RDVs
    #Chaque objet correspond a une salle
    #une salle est definis par un numero et un ensemble de plage
    #La representation grahpique necessite les attributs de coordonnés, de de dimensions et de couleur
        
    def __init__(self,numero):

        global planning
        print("creation Salle")

        #Attributs recuperés
        self.numero=numero
        
        #Attributs constants
        self.coordX=coordXSalle
        self.long=longueurSalle
        self.haut=hauteurSalle
        
        #Attributs deduits des valeurs recuperées
        self.coordY=numero*coefCoordYSalle+ajCoordYSalle
        print(self.coordY)
        if numero==0:
                self.coordY=coordYReserve


        #Attributs graphiques
        self.representation=planning.create_rectangle(self.coordX,self.coordY,self.coordX+self.long,self.coordY+self.haut,fill='white')
        self.etiquette = planning.create_text(self.coordX-ajEtiquetteSalle, self.coordY+self.haut/2, text=self.numero)
        self.bouton=planning.create_rectangle(self.coordX+self.long,self.coordY,self.coordX+self.long+self.haut/2,self.coordY+self.haut,fill='green')


    def estSelectionné(self, event): #Accesseur d'état
        if event.x>=self.coordX and event.x<=self.coordX+self.long and event.y>=self.coordY and event.y<=self.coordY+self.haut :
            return True
        else :return False

    def valide(self,event,mode):
        if event.x>=self.coordX+self.long and event.x<=self.coordX+self.long+self.haut/2 and event.y>=self.coordY and event.y<=self.coordY+self.haut :
            print("salle "+ str(self.numero)+" est validé")

            if mode=="rdv":
                for rdv in rdvs:
                    if rdv.estDansSalle(self.numero):
                        rdv.enregistrer()

            if mode=="plage":
                for plage in plages:
                    if plage.estDansSalle(self.numero):
                        plage.enregistrer()


def minInPx(minute): #fonction d'attribution d'une position en fonction d'un temps
    px=coordXSalle+(minute-heureD*60)*(longueurSalle/((heureF-heureD)*60))
    return px


def qMinInPx(minute): #fonction d'attribution d'une position en fonction d'un temps
    px=minute*(longueurSalle/((heureF-heureD)*60))
    print(px)
    return px

def pxInHm(px): #fonction d'attribution d'une position en fonction d'un temps
    heure=''
    minute=(px-coordXSalle)/(longueurSalle/((heureF-heureD)*60))+heureD*60
    if str(minute//60)[1]=='.':
        heure+='0'
        heure+=str(minute//60)[0]
    else:
        heure+=str(minute//60)[0]
        heure+=str(minute//60)[1]
    heure+=":"
    print(minute%60)
    if str(minute%60)[1]=='.':
        heure+='0'
        heure+=str(minute%60)[0]
    else:
        heure+=str(minute%60)[0]
        heure+=str(minute%60)[1]
    return heure


def CreerPlanning(jour,mode): #fonction de creation du contenant graphique planning
    
    #Parametre du l'axe temps
    axeTempsCoordX=coordXSalle
    axeTempsCoordY=coordYAxeTemps
    axeTempsLong=longueurSalle
    axeTempsHaut=hauteurSalle/2

    planning.delete(ALL)

    planning.create_text(coordXJour, coordYJour, text=jour, font=myFont)
    
    p=planning.create_rectangle(coordXJour+ajPX, coordYJour+ajPSY, coordXJour+ajPX+hauteurSalle/2, coordYJour+ajPSY-hauteurSalle/2, fill="gray79")
    n=planning.create_rectangle(coordXJour+ajSX, coordYJour+ajPSY, coordXJour+ajSX+hauteurSalle/2, coordYJour+ajPSY-hauteurSalle/2, fill="gray79")
    
    modeB=planning.create_rectangle(coordXSalle+longueurSalle/2, coordYReserve+5*hauteurSalle, coordXSalle+hauteurSalle+longueurSalle/2+hauteurSalle/2, coordYReserve+5*hauteurSalle-hauteurSalle, fill="gray79")
    
    axeTemps=planning.create_rectangle(axeTempsCoordX,axeTempsCoordY,axeTempsCoordX+axeTempsLong,axeTempsCoordY+axeTempsHaut,fill='white' )

    global salles
    global rdvs
    global plages
    global reserve
    salles=[]
    salle1=Salle(1)
    salle2=Salle(2)
    salle3=Salle(3)
    salle4=Salle(4)
    salle5=Salle(5)
    salle6=Salle(6)
    salle7=Salle(7)
    salle8=Salle(8)
    salle9=Salle(9)
    reserve=Salle(0)

    salles.append(salle1)
    salles.append(salle2)
    salles.append(salle3)
    salles.append(salle4)
    salles.append(salle5)
    salles.append(salle6)
    salles.append(salle7)
    salles.append(salle8)
    salles.append(salle9)
    salles.append(reserve)

    if mode=="plage":
        print("creation planning mode plages")
        cursor.execute("SELECT * FROM plage WHERE jour= '"+jour +"'")
        n=cursor.fetchall()
        plages=[]

        for r in n:
            plages.append(Plage(r))

        nouveau=planning.create_rectangle(coordXSalle, coordYReserve, coordXSalle+hauteurSalle/2, coordYReserve+hauteurSalle, fill="red")

    elif mode=="rdv":
        cursor.execute("SELECT * FROM prevu WHERE jour= '"+jour +"' OR salle='0'")
        n=cursor.fetchall()
        rdvs=[]

        for r in n:
            rdvs.append(Rdv(r)) 

            
    print("planning")
    for h in range(heureD,heureF):
        planning.create_text(minInPx(h*60)+ajEtiquetteAxeTemps,axeTempsCoordY+axeTempsHaut/2, text=str(h))
    return planning

def Clic(event): #fonction de recation au clic gauche: designation du rdv cliqué
        global decalageJ
        global mode
        if event.x>=coordXSalle+longueurSalle/2 and event.x<=coordXSalle+hauteurSalle+longueurSalle/2+hauteurSalle/2 and event.y<=coordYReserve+5*hauteurSalle and event.y>=coordYReserve+5*hauteurSalle-hauteurSalle:
            if mode=="rdv":
                mode="plage"
            else:
                mode="rdv"
            ajd=jourAc()
            CreerPlanning(ljour[ajd[1]+decalageJ],mode)
        if mode=="rdv":
            for rdv in rdvs:
                if rdv.estSelectionné(event):
                        print("un rdv est selectionné")
                        rdv.clique(True)
                        break
            for salle in salles:
                if salle.valide(event,mode):
                    print("une salle a été validé")
                    break

                
        elif mode=="plage":
            print("clic mode plage")
            if event.x>=coordXSalle and event.x<=coordXSalle+hauteurSalle/2 and event.y<=coordYReserve+hauteurSalle and event.y>=coordYReserve :
                print("nouvelle plage")
                nouvellePlage()
            
            for plage in plages:
                if plage.estSelectionné(event):
                        print("une plage est selectionné")
                        plage.clique(True)
                        break
            for salle in salles:
                if salle.valide(event,mode):
                    print("une salle a été validé")
                    break
            
        ajd=jourAc()    
        if event.x>=coordXJour+ajPX and event.x<=coordXJour+ajPX+hauteurSalle/2 and event.y<=coordYJour+ajPSY and event.y>=coordYJour+ajPSY-hauteurSalle/2 :
            print("precedent")
            decalageJ=decalageJ+-1
            CreerPlanning(ljour[ajd[1]+decalageJ],mode)
            print(ljour[ajd[1]+decalageJ])
            
        elif event.x>=coordXJour+ajSX and event.x<=coordXJour+ajSX+hauteurSalle/2 and event.y<=coordYJour+ajPSY and event.y>=coordYJour+ajPSY-hauteurSalle/2 :
            print("suivant")

            decalageJ=decalageJ+1
            CreerPlanning(ljour[ajd[1]+decalageJ],mode)  
            
def Declic(event): #fonction de reaction au relachement: demande de placement du rdv deposé
        global rdv
        global salles
        global reserve
        print("declic")
        p=0
        if mode=="rdv":
            for rdv in rdvs:
                if rdv.estclique():
                        for salle in salles:
                                if salle.estSelectionné(event):
                                        rdv.placeDans(salle,event)
                                        print("declic bon")
                                        p=1
                        if p==0:
                                rdv.placeDans(reserve,event)
                                print("declic hors salle")
                        rdv.clique(False)
        elif mode=="plage":
            global plages
            p=0
            print("declic mode plage")
            for plage in plages:
                if plage.estclique():
                    for salle in salles:
                            if salle.estSelectionné(event):
                                    plage.placeDans(salle,event)
                                    print("declic bon")
                                    p=1
                    if p==0:
                            plage.placeDans(reserve,event)
                            print("declic hors salle")
                    plage.clique(False)            

def clicD(event): #fonction de reaction au clic droit: determination du rdv selectionné et demande d'affichage
        print("clicD")
        if mode=="rdv":
            for rdv in rdvs:
                if rdv.estSelectionné(event):
                        rdv.afficher()
        if mode=="plage":
            for plage in plages:
                if plage.estSelectionné(event):
                        plage.afficher()            

def Bouge(event): #fonction de reaction au mouvement de la souris: demande de mise en mouvement du rdv selectionné
        if mode=="rdv":
            for rdv in rdvs:
                if rdv.estclique():
                        rdv.place(event)
        elif mode=="plage":
            for plage in plages:
                if plage.estclique():
                        plage.place(event)            

def jourAc():
    acd=str(now.day)+"/"+str(now.month)+"/"+str(now.year)
    print(acd)
    for i in range (len(ljour)):
        if ljour[i]==acd:
            break
    return acd, i



# Création de la fenêtre principale
Mafenetre = Tk()
Mafenetre.title("Planning journalier")
myFont = Font(family="Helvetica", size=20)

planning = Canvas(Mafenetre,width=largeur,height=hauteur,bg ='white')
ajd=jourAc()
CreerPlanning(ajd[0],"plage")  # Création d'un widget planning

# Création des objets graphiques (temporaire




#reglages du widget planning
planning.focus_set()
planning.pack(padx=10,pady=10)

#reglages des evenements
planning.bind('<Button-1>',Clic)
planning.bind('<ButtonRelease>',Declic)
planning.bind('<B1-Motion>',Bouge)
planning.bind('<Button-3>',clicD)

Mafenetre.mainloop()

