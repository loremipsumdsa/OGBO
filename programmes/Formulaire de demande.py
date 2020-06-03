
from tkinter import *

def envoi():
 c=intervPratC.curselection()
 print(intervPratC.get(c[0]))

 d=intervINC.curselection()
 print(intervINC.get(d[0]))


    

def formulaire():
    # Creation fenetre + Frames de base + Bouton validation
    formulaire=Tk()
    formulaire.title("Formulaire")
    patientF=Frame(formulaire, borderwidth=2,relief=GROOVE)
    intervF=Frame(formulaire, borderwidth=2, relief=GROOVE)
    ok=Button(formulaire, text="Valider", command=envoi)
    annuler =Button(formulaire, text= "Annuler")
    
    #Creation Frames Patient
    patientNF=Frame(patientF)
    patientIDF=Frame(patientF)

    #Creation Frames intervention
    intervPratF=Frame(intervF)
    intervDF=Frame(intervF)
    intervComF=Frame(intervF)

    #Creation Labels Patient
    patientNL=Label(patientNF, text="Nom du patient            ")
    patientIDL=Label(patientIDF, text="ID du patient                  ")

    #Creation Labels intervention
    intervPratL=Label(intervPratF, text="Nom du Praticien       ")
    intervDL=Label(intervDF, text="Intervention à pratiquer    ")
    intervComL=Label(intervComF, text="Note au cadre de bloc")

    
    #Creation champs Patient
    global patientNC
    global patientIDC
    patientNC=Entry(patientNF)
    patientIDC=Entry(patientIDF)

    #Creation champs intervention
    global intervPratC
    global intervDC
    global intervComC
    intervPratC=Listbox(intervPratF, width=20, height=3,exportselection=0)
    intervPratC.insert(0,"Jeanne Deferlin")


    intervDC=Listbox(intervDF, width=20, height=3, exportselection=0)
    intervDC.insert(0,"1")
    
    
    intervComC=Entry(intervComF)


    #Placement Champs et labels patient
    patientNC.pack(side=RIGHT)
    patientNL.pack(side=LEFT)

    patientIDC.pack(side=RIGHT)
    patientIDL.pack(side=LEFT)



    #Placement Champs et labels intervention
    intervPratC.pack(side=RIGHT)
    intervPratL.pack(side=LEFT)

    intervDC.pack(side=RIGHT)
    intervDL.pack(side=LEFT)

    intervComC.pack(side=RIGHT)
    intervComL.pack(side=LEFT)


    #Placement Frames patient
    patientNF.pack();
    patientIDF.pack();


    #Placement Frames patient
    intervPratF.pack();
    intervDF.pack();
    intervComF.pack();

    #placement Frames de base + bouton validation et annulation ouverture fenetre
    patientF.pack(side=TOP)
    ok.pack(side=BOTTOM, padx = 10, pady = 10)
    annuler.pack(side= BOTTOM, padx= 10, pady=10)
    intervF.pack(side=BOTTOM)
    formulaire.mainloop()

accueil=Tk()
accueil.title("Interface practicien")
accueil.geometry('250x250')
listF=Frame(accueil, borderwidth=2, relief=GROOVE)
info=Label(listF, text="affichage des listes")
nouveau=Button(accueil, text="nouveau",command=formulaire,padx=5, pady=5)

info.pack()
listF.pack(side=BOTTOM)
nouveau.pack( padx =10, pady = 10)
accueil.mainloop()
