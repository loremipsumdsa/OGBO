
from tkinter import *
import tkinter.font as tkFont
from tkinter.filedialog import *
from tkinter import ttk
from time import strftime
import mysql.connector

#parametre de la base de données
user="paul"
pw="IDijir2016*!"
host="localhost"
database="test1"
cmdArch="INSERT INTO historique(patient, NIR, praticien, intervention, INI, NCB, DF, jour, salle, heureP, tempsP, heureD, heureF,imprevu, raison) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
cmdAdenC="INSERT INTO encours(patient, NIR, praticien, intervention, INI, NCB, DF, jour, heure, temps, salle, statut, raison, estimation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

infoB=[]
mydb=mysql.connector.connect(host=host, user=user,password=pw,database=database)
cursor=mydb.cursor()
heure=" "

salle=1
etape="no"
imprevu="aucun"
commentaire="non specifié"

def suivant():
    global occupe
    lowerM=[]
    lowerH=[]
    mmin=60
    hmin=24
    jour=strftime("%d/%m/%y")
    jourM=''
    if jour[0]!='0':
        jourM+=jour[0]
    jourM+=jour[1]
    jourM+=jour[2]
    if jour[3]!='0':
        jourM+=jour[3]
    jourM+=jour[4]
    jourM+=jour[5]
    jourM+='2'
    jourM+='0'
    jourM+=jour[6]
    jourM+=jour[7]

    ordre="SELECT * FROM prevu WHERE salle ='"+str(salle)+"' AND jour='"+jourM+"'"
    cursor.execute(ordre)
    p=cursor.fetchall()
    print(p)
    if p==[]:
        occupe=False
    for i in range (len(p)):
        h=int(p[i][9][0]+p[i][9][1])
        if h<hmin:
            lowerH=[]
            lowerH.append(p[i])
            hmin=h
        elif h==hmin:
            lowerH.append(p[i])
            
    for i in range (len(lowerH)):
        m=int(lowerH[i][9][3]+lowerH[i][9][4])
        if m<mmin:
            lowerM=lowerH[i]
            mmin=h
    print(lowerM)
    if lowerM!=[]:
        valeurs=(lowerM[1],lowerM[2],lowerM[3],lowerM[4],str(lowerM[5]),lowerM[6],lowerM[7],lowerM[8],lowerM[9],str(lowerM[10]),str(salle)," ", " ", " ")
        cursor.execute(cmdAdenC,valeurs)
        mydb.commit()
        cursor.execute("DELETE FROM prevu WHERE id = '"+str(lowerM[0])+"'")


def archivage():
    global infoB
    h=strftime("%H:%M")
    valeurs=(infoB[1],infoB[2],infoB[3],infoB[4],infoB[5],infoB[6],infoB[7],infoB[8],salle,infoB[9],infoB[10],heure,h,imprevu, commentaire)
    cursor.execute(cmdArch,valeurs)
    mydb.commit()

    
def nettoyage():
    cursor.execute("DELETE FROM encours WHERE salle = '"+str(salle)+"'")
    mydb.commit()
    
def extraction():
    global infoB
    global occupe
    global etape
    #fonction de lecture de la base de donné intervention en cours
    ordre="SELECT * FROM encours WHERE salle ='"+str(salle)+"'"
    cursor.execute(ordre)
    infoB=cursor.fetchall()
    if infoB!=[]:
        infoB=infoB[0]
        print(infoB[0])
        intitule.configure(text=str(infoB[1])+"  "+str(infoB[4])+"   Prevu pour: "+infoB[9]+"   Avec: "+infoB[3])
        etape="instal"
    else:
        print("liste vide")
        etape="no"
        intitule.configure(text="Aucune autre intervention prevu pour la journée")

def changementOp():
    global etape
    global heure
    global lp
    s=True
    print("changement op")
    print(salle)
    labelInstal.configure(text="Heure d'installation")
    labelInduc.configure(text="Heure d'induction")
    labelInci.configure(text="Heure d'incision")
    labelFerm.configure(text="Heure de fermeture")
    labelSort.configure(text="Heure de sortie")

    if etape=="no":
        suivant()
    if etape!="no":
        archivage()
        nettoyage()
        suivant()
    extraction()
    
    heure=a=strftime("%H:%M")


def annulation():
    global imprevu
    print("annulation")
    cursor.execute("UPDATE encours SET statut='annulee' WHERE salle="+str(salle))
    mydb.commit()
    imprevu="annulee"

def retard():
    global imprevu
    global retardE
    print("retard")
    cursor.execute("UPDATE encours SET statut='retard', estimation='"+retardE.get('1.0','1.3')+"' WHERE salle="+str(salle))
    mydb.commit()
    imprevu="retard"


    
#configuration fenetre racine
fenetre = Tk()
fenetre.title("interface bloc opératoire")
fenetre.configure(bg = "white")


def raison():
    global raisonE
    global commentaire
    print("raison")
    print(raisonE.get("1.0","3.0"))
    commentaire=raisonE.get("1.0","1.35")
    cursor.execute("UPDATE encours SET raison='"+commentaire+"' WHERE salle="+str(salle))
    mydb.commit()
    #cursor.execute("UPDATE encours SET statut='"+raisonE.get()+"' WHERE salle="+str(salle))
    #mydb.commit()    
    
def affichHeure(etapeD):
    global etape
    print(etape)
    if etapeD==etape:
        print("alors")
        if etape=="instal":
            a=strftime("%d/%m/%y %H:%M")
            labelInstal.configure(text=a)
            cursor.execute("UPDATE encours SET statut='installation' WHERE salle="+str(salle))
            mydb.commit()
            etape="induc"
            
        elif etape=="induc":
            a=strftime("%d/%m/%y %H:%M")
            labelInduc.configure(text=a)
            cursor.execute("UPDATE encours SET statut='induction' WHERE salle="+str(salle))
            mydb.commit()
            etape="inci"
            
        elif etape=="inci":
            a=strftime("%d/%m/%y %H:%M")
            labelInci.configure(text=a)
            cursor.execute("UPDATE encours SET statut='incision' WHERE salle="+str(salle))
            mydb.commit()
            etape="ferm"
            
        elif etape=="ferm":
            a=strftime("%d/%m/%y %H:%M")
            labelFerm.configure(text=a)
            cursor.execute("UPDATE encours SET statut='fermeture' WHERE salle="+str(salle))
            mydb.commit()
            etape="sort"

        elif etape=="sort":
            a=strftime("%d/%m/%y %H:%M")
            labelSort.configure(text=a)
            cursor.execute("UPDATE encours SET statut='sortie' WHERE salle="+str(salle))
            mydb.commit()
            etape="fin"



def confSalle():
    global salleE
    global salle
    salle=int(salleE.get())
    print(salle+1)

def popup():
    global salleE
    param = Toplevel()
    param.title("selection salle")
    param.configure(bg = "white")

    quellesalle = Label(param, text="Entrer le numéro de la salle :",font=policelabel,bg = "white")
    quellesalle.pack(side=TOP)
    
    global salle
    salleE = Entry(param,font = policelabel,width=10,bg = "white",text=salle)
    salleE.pack(side=TOP)
    salleE.focus_set()
   

    boutsalle = Button(param, text="Valider",font = policelabel,bg="dark green", width=10, command=confSalle)
    boutsalle.pack(side=TOP)
    
    boutsallequit=Button(param, text='Quitter',font = policelabel, command=param.destroy,bg = "white")
    boutsallequit.pack(side=BOTTOM,padx=10, pady=10)

    
            
#affichage titre, on peut changer le text en fonction de l'opération
policelabel=tkFont.Font(size=15)
intitule = Label(fenetre, text="Nom du patient,type d'intervention", font = policelabel,bg = "white",relief='ridge',width=150)
intitule.pack(side=TOP)

#bouton suivant
Framequit=Frame(fenetre, borderwidth=0, relief=GROOVE,bg = "white")
Framequit.pack(side=BOTTOM)
suivantB=Button(Framequit, text="Intervention suivante",font = policelabel, command=changementOp,bg = "white",width=50,relief='raised',borderwidth=5)
suivantB.pack(side=LEFT,padx=500, pady=20)

#frame de placement
Frameleft = Frame(fenetre, borderwidth=0, relief=GROOVE,bg = "white")
Frameleft.pack(side=LEFT, padx=0, pady=0)
FrameStatut = Frame(Frameleft, borderwidth=0, relief=GROOVE,bg = "white")
FrameStatut.pack(side=BOTTOM, padx=0, pady=0)
FrameBoutonStatut = Frame(FrameStatut, borderwidth=0, relief=GROOVE,bg = "white")
FrameBoutonStatut.pack(side=LEFT, padx=0, pady=0)
FrameLabHeure = Frame(FrameStatut, borderwidth=0, relief=GROOVE,bg = "white")
FrameLabHeure.pack(side=LEFT, padx=5, pady=0)
Frame3 = Frame(fenetre, borderwidth=0, relief=GROOVE,bg = "white")
Frame3. pack(side=RIGHT, padx=5, pady=30)
Frame4 = Frame(Frame3, borderwidth=0, relief=GROOVE,bg = "white")
Frame4.pack(side=TOP, padx=5, pady=30)
Frame5 = Frame(Frame3, borderwidth=0, relief=GROOVE,bg = "white")
Frame5.pack(side=TOP, padx=5, pady=5)
Frame6 = Frame(Frame3, borderwidth=0, relief=GROOVE,bg = "white")
Frame6.pack(side=TOP, padx=5, pady=5)

#trex
#                         _-==o-_
#          ____--====--_-=  _==--
#  ========_____(  )__((_--=
#               | |    \\
#               ||      P
#               [_\


#consigne horloge
labelanu = Label(Frameleft, text="Appuyer sur le bouton correspondant à la phase de l'opération :",font=policelabel,bg = "white",relief='ridge')
labelanu.pack(side=TOP)


#frame heure
FrameInstal = Frame(FrameLabHeure, borderwidth=2, relief=GROOVE,bg = "white")
FrameInstal.pack(side=TOP, padx=5, pady=3)
FrameInduc = Frame(FrameLabHeure, borderwidth=2, relief=GROOVE,bg = "white")
FrameInduc.pack(side=TOP, padx=5, pady=3)
FrameInci = Frame(FrameLabHeure, borderwidth=2, relief=GROOVE,bg = "white")
FrameInci.pack(side=TOP, padx=5, pady=3)
FrameFerm = Frame(FrameLabHeure, borderwidth=2, relief=GROOVE,bg = "white")
FrameFerm.pack(side=TOP, padx=5, pady=3)
FrameSort = Frame(FrameLabHeure, borderwidth=2, relief=GROOVE,bg = "white")
FrameSort.pack(side=TOP, padx=5, pady=3)


#heure/ indication phase d'opération
labelInstal=Label(FrameInstal,height=6, width=40, text="Heure d'installation", borderwidth=2,font = policelabel,bg = "white")
labelInstal.pack(padx=0, pady=5)
labelInduc=Label(FrameInduc,height=6, width=40, text="Heure d'induction",borderwidth=2,font = policelabel,bg = "white")
labelInduc.pack(padx=0, pady=5)
labelInci=Label(FrameInci,height=6, width=40, text="Heure d'incision",borderwidth=2,font = policelabel,bg = "white")
labelInci.pack(padx=0, pady=5)
labelFerm=Label(FrameFerm,height=6, width=40, text="Heure de fermeture",borderwidth=2,font = policelabel,bg = "white")
labelFerm.pack(padx=0, pady=5)
labelSort=Label(FrameSort,height=6, width=40, text="Heure de sortie",borderwidth=2,font = policelabel,bg = "white")
labelSort.pack(padx=0, pady=5)


#tricératops                  
#                           ,,
#                __________ \\___
#               /          ==\\ O\=/\
#              /\/ |     | |==``__\-"
#                | |-----| |
#                |_\     |_\
#

#bouton pour l'heure
bouton=Button(FrameBoutonStatut,height=6, width=40, text="Installation", command=lambda: affichHeure("instal"),font = policelabel,bg = "white",relief='raised',borderwidth=5)
bouton.pack(padx=0, pady=3)

bouton2=Button(FrameBoutonStatut,height=6, width=40, text="Induction", command=lambda: affichHeure("induc"),font = policelabel,bg = "white",relief='raised',borderwidth=5)
bouton2.pack(side=TOP,padx=0, pady=3)

bouton3=Button(FrameBoutonStatut,height=6, width=40, text="Incision", command=lambda: affichHeure("inci"),font = policelabel,bg = "white",relief='raised',borderwidth=5)
bouton3.pack(side=TOP,padx=0, pady=3)

bouton4=Button(FrameBoutonStatut,height=6, width=40, text="Fermeture", command=lambda: affichHeure("ferm"),font = policelabel,bg = "white",relief='raised',borderwidth=5)
bouton4.pack(side=TOP,padx=0, pady=3)

bouton5=Button(FrameBoutonStatut,height=6, width=40, text="Sortie", command=lambda: affichHeure("sort"),font = policelabel,bg = "white",relief='raised',borderwidth=5)
bouton5.pack(side=TOP,padx=0, pady=3)





#bouton annulation
annuler = Button(Frame4,text= "Annulation de l'opération",height=6, width=40,bg="red4",font = policelabel, command=annulation,relief='raised',borderwidth=5) #on pourra créer un fonction pour envoyer un input à la base de données#
annuler.pack(side=BOTTOM, padx=0, pady=0)
labelanu = Label(Frame4, text="Appuyer sur ce bouton si l'opération est annulée :",font=policelabel,bg = "white",relief='ridge')
labelanu.pack(side=TOP)



#spinosaure
#
#                 ___
#                /   \
#               /     \   _-==o-_
#          ____-|====-|_-=  _==--
#  ========_____(  )__((_--=
#               | |    \\
#               ||      P
#               [_\



#durée retard
Frame7 = Frame(Frame5, borderwidth=0, relief=GROOVE,bg = "white")

Frame7.pack(side=RIGHT, padx=5, pady=30)

instretard = Label(Frame7, text="Entrer la durée du retard \n en minutes :",font=policelabel,bg = "white",relief='ridge')
instretard.pack(side=TOP)

labretard = Label(Frame5, text="Retard",height=4, width=20, bg="dark orange2",font=policelabel)
labretard.pack(side=LEFT,padx=50)

retardE = Text(Frame7, width=10, height=3)
retardE.pack(side=LEFT)

boutretard = Button(Frame7, text="Valider",bg="dark green", width=6,font=policelabel, command=retard,relief='raised',borderwidth=5,height=1)
boutretard.pack(side=LEFT)

retardE.focus_set()


#raison retard
raisonL = Label(Frame6, text="Entrer la raison du retard / de l'annulation :",font=policelabel,bg = "white",relief='ridge')
raisonL.pack(side=TOP)

raisonE = Text(Frame6, width=50, height=4)
raisonE.pack(side=LEFT)

raisonE.focus_set()


raisonB = Button(Frame6, text="Valider",bg="dark green", width=10,font=policelabel,relief='raised',borderwidth=5,height=2, command=raison)
raisonB.pack(side=LEFT)





Boutonsalle=Button(Framequit, text='Salle',font = policelabel, command=popup,bg = "white")
Boutonsalle.pack(side=RIGHT,pady=20)


