from tkinter import *
import tkinter as tk
from tkinter.font import Font
from tkinter.messagebox import *
import mysql.connector
import time

#parametre de la base de données
user="paul"
pw="headvoice"
host="localhost"
database="test1"
mydb=mysql.connector.connect(host=host, user=user,password=pw,database=database)
cursor=mydb.cursor()
codeCouleur={"installation":"blue","induction":"green","incision":"yellow","fermeture":"brown","sortie":"black","retard":"orange","annulee":"red","libre":"white","transition":"white"}

#Creation de la fenetre principale
Mafenetre = Tk()
Mafenetre.rowconfigure(0,weight=1)
Mafenetre.columnconfigure(0,weight=1)

# Création d'un widget Canvas ( zone graphique )
largeur = 1200
hauteur = 1200
Canevas = Canvas(Mafenetre, width = largeur, height =hauteur, bg ='white')
Canevas.pack(padx =5, pady = 5)



def extraction(numero):
    #fonction de lecture de la base de donné intervention en cours
    mydb=mysql.connector.connect(host=host, user=user,password=pw,database=database)
    cursor=mydb.cursor()
    ordre="SELECT * FROM encours WHERE salle ='"+str(numero)+"+'"
    cursor.execute(ordre)
    r=cursor.fetchall()
    cursor.close
    mydb.close()
    if r==[]:
        return [0,"--","--","--","--","--","--","--","--","--","--","--","libre","--","--","--"]
    elif r[0][12]==" ":
        return [0,"--","--","--","--","--","--","--","--","--","--","--","transition","--","--","--"]
    else:
        return r[0]



# Création de la fenêtre principale
Mafenetre.title("STATUTS DES SALLES D'OPERATION")
Mafenetre.geometry('1280x1024')





# On définit les variables qui nous servirons plus tard
marge = hauteur/20
longueurCarre = (largeur/6)-2*marge
ajCoordXSalle = 2/3*longueurCarre
ajCoordYSalle= 2/3*longueurCarre
hauteurListe= hauteur/25



# Ajustement du Canvas à la taille de l'écran
Canevas.grid(sticky=NSEW)

#Création de la police des numéros et de la liste
myFont = Font(family="Helvetica", size=40)

myFont2 = Font(family="Helvetica", size=16)





class Salle:
    #Classe qui associe une salle avec un numéro
    #Création des carrés pour les salles, on donne la coordonnée d'un point du carré et de la longueur de ce carre (en fonction de la largeur et de la hauteur de l'écran)

    def __init__(self,numero):
        
        #Attribut de base
        self.numero = numero

        #recuperation de l'enemble des informations
        self.extrait=extraction(self.numero)

        #Extraction primaires des informations 
        self.nompract = self.extrait[3]
        self.nompat = self.extrait[1]
        self.intervention = self.extrait[4]
        self.etat = self.extrait[12]
        self.jour=self.extrait[8]
        self.heure=self.extrait[9]
        self.raison=self.extrait[13]
        self.estimation=self.extrait[14]

        #Interpretation
        self.color = codeCouleur[self.etat]

        self.coordXL = largeur/3
        self.coordYL = 1/6*hauteur+(self.numero-1)*largeur/20

        
        self.texteL = str(self.numero)+" - "+self.nompract+ " - "+self.nompat+ " - "+self.intervention
        if self.etat=="retard":
            self.texteL+=" - retard estimé à :"+self.estimation+" minutes"
        else:
            self.texteL+=" - "+self.etat
        if (self.raison!=" " and self.raison!="--") :
            self.texteL+=" - Commentaire de l'infirmier: "+self.raison
            print(self.raison+"a")

            
        if self.numero <= 5 :
            self.coordX = marge
            self.coordY = self.numero*marge+(self.numero-1)*longueurCarre
        else :
            self.coordX = 2*marge+longueurCarre
            self.coordY = (self.numero-5)*marge+(self.numero-6)*longueurCarre

        
        self.representationC = Canevas.create_rectangle(self.coordX,self.coordY,self.coordX+longueurCarre,self.coordY+longueurCarre,fill='white')
        self.representationN = Canevas.create_text(self.coordX + ajCoordXSalle, self.coordY + ajCoordYSalle, text= numero, font =myFont)
        self.representationR = Canevas.create_rectangle(self.coordX, self.coordY, self.coordX+longueurCarre/6,self.coordY+longueurCarre,fill=self.color)
        self.representationCL = Canevas.create_rectangle(self.coordXL, self.coordYL, self.coordXL+hauteurListe, self.coordYL+hauteurListe,fill=self.color)
        self.representationL = Canevas.create_text(self.coordXL+1.5*hauteurListe, self.coordYL+1/2*hauteurListe, text=self.texteL,anchor="w", font= myFont2)


    def estSelectionné(self, event): #Accesseur d'état
        if event.x>=self.coordX and event.x<=self.coordX+longueurCarre and event.y>=self.coordY and event.y<=self.coordY+longueurCarre :
            return True
        else :return False
        
    
    def afficher(self): #affichage informatif
        text='Praticien: '+self.nompract+ " Date: "+ self.jour + " "+self.heure+" Patient: "+self.nompat+"\n"+'Praticien: '+self.nompract+ " Date: "+ self.jour + " "+self.heure+" Patient: "+self.nompat+"\n"
        showinfo("Interventions à venir salle"+str(self.numero), text)


    def rafraichir(self):
        #Extraction secondaire des informations
        self.extrait=extraction(self.numero)
        self.nompract = self.extrait[3]
        self.nompat = self.extrait[1]
        self.intervention = self.extrait[4]
        self.etat = self.extrait[12]
        self.jour=self.extrait[8]
        self.heure=self.extrait[9]
        self.raison=self.extrait[13]
        self.estimation=self.extrait[14]

        self.texteL = str(self.numero)+" - "+self.nompract+ " - "+self.nompat+ " - "+self.intervention
        if self.etat=="retard":
            self.texteL+=" - retard estimé à :"+self.estimation+" minutes"
        else:
            self.texteL+=" - "+self.etat
        if (self.raison!=" " and self.raison!="--") :
            self.texteL+=" - Commentaire de l'infirmier: "+self.raison

            

        self.color = codeCouleur[self.etat]

        Canevas.delete(self.representationR)
        Canevas.delete(self.representationCL)
        Canevas.delete(self.representationL)


        self.representationR = Canevas.create_rectangle(self.coordX, self.coordY, self.coordX+longueurCarre/6,self.coordY+longueurCarre,fill=self.color)
        self.representationCL = Canevas.create_rectangle(self.coordXL, self.coordYL, self.coordXL+hauteurListe, self.coordYL+hauteurListe,fill=self.color)
        self.representationL = Canevas.create_text(self.coordXL+1.5*hauteurListe, self.coordYL+1/2*hauteurListe, text=self.texteL,anchor="w", font= myFont2)

        
def clicD(event): #fonction de reaction au clic droit: determination du rdv selectionné et demande d'affichage
        print("clicD")
        for salle in listeS:
                if salle.estSelectionné(event):
                        salle.afficher()


    
        
salle1 = Salle(1)
salle2 = Salle(2)
salle3 = Salle(3)
salle4 = Salle(4)
salle5 = Salle(5)
salle6 = Salle(6)
salle7 = Salle(7)
salle8 = Salle(8)
salle9= Salle(9)


listeS=[]
listeS.append(salle1)
listeS.append(salle2)
listeS.append(salle3)
listeS.append(salle4)
listeS.append(salle5)
listeS.append(salle6)
listeS.append(salle7)
listeS.append(salle8)
listeS.append(salle9)

Canevas.bind('<Button-3>',clicD)

while True:
    for salle in listeS:
        salle.rafraichir()
    Mafenetre.update_idletasks()
    Mafenetre.update()

