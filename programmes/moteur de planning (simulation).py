class Demande:
    def __init__(self,i,p,df,dp):
        self.i=i
        self.p=p
        self.df=df
        self.dp=dp

class Rdv:
    def __init__(self,s,p,j,h,d):
        self.s=s
        self.p=p
        self.j=j
        self.h=h
        self.d=d

class Plage:
    def __init__(self,s,p,j,h,d):
        self.s=s
        self.p=p
        self.j=j
        self.h=h
        self.d=d


def creerPlanning():
    inter=False
    place=False
    dfM=100000
    global rdvs
    global demandes
    global plages
    global bl
    demandesS=[]
    
    #Considerer la demande la plus ancienne
    
    for demande in demandes:
        if demande.df<dfM and not(demande.i in bl):
            del demandesS[:]
            demandesS.append(demande)
            dfM=demande.df
        elif demande.df==dfM:
            demandesS.append(demande)
            
    for demande in demandesS:
        #parcourir les plages attribuées au même praticien et dont la durée est plus longue que la durée prévue
        for plage in plages:
            inter=False
            if plage.p==demande.p:
                print("plage trouvée")
                #Si il existe une intervention sur cette plage
                for rdv in rdvs:
                    if rdv.j==plage.j and rdv.s==plage.s:
                        if (rdv.h>=plage.h and rdv.h<=plage.h+plage.d) or (rdv.h+rdv.d>=plage.h and rdv.h+rdv.d<=plage.h+plage.d) or (plage.h>=rdv.h and plage.h+plage.d<=rdv.h+rdv.d):
                            print("interference rdv")
                            inter=True
                            #Si la fin de cette intervention est prevue avant la fin de la plage
                            if rdv.h+rdv.d<plage.h+plage.d:
                                print("plage partiellement libre")
                                #Si le delai entre la fin de l’intervention et la fin de la plage est plus grand que la durée demandée
                                if demande.dp<=plage.d-rdv.d:
                                    #Prévoir une nouvelle intervention avec le praticien, la salle, l’heure de fin de l’intervention et la durée demandée
                                    print("plage suffisante: insertion d'un nouveau rendez vous")
                                    rdvs.append(Rdv(plage.s,demande.p,plage.j,rdv.h+rdv.d,demande.dp))
                                    place=True
                                    #Supprimer la demande

                                    print("Suppression de la demande")
                                    print("\n \n \n")
                                    for a in range (len(demandes)):
                                        if demande.i==demandes[a].i:
                                            del demandes[a]
                                            return

        
                #Sinon
                if inter==False:
                    print("aucune interference")
                    if demande.dp<=plage.d:
                        #Prévoir une nouvelle intervention avec le praticien, la salle, l’heure de début de la plage et la durée demandée
                        print("plage suffisante: insertion d'un nouveau rendez vous")
                        rdvs.append(Rdv(plage.s,demande.p,plage.j,plage.h,demande.dp))
                        place=True
                        #Supprimer la demande
            
                        print("Suppression de la demande")
                        print("\n \n \n")
                        t=demande.i
                        for a in range (len(demandes)):
                            if t==demandes[a].i:
                                del demandes[a]
                                return

        if place==False :
            print("Aucune plage adaptée trouvée")
            print("\n \n \n")
            bl.append(demande.i)
    print("fin de traitement")
    return 1

demandes=[]
demandes.append(Demande(0,"a",2,30))
demandes.append(Demande(1,"a",2,30))
demandes.append(Demande(2,"b",3,61))
demandes.append(Demande(3,"c",1,19))
demandes.append(Demande(4,"c",5,40))

plages=[]
plages.append(Plage(1,"a",3,10,60))
plages.append(Plage(2,"b",4,10,61))
plages.append(Plage(2,"b",4,100,60))
plages.append(Plage(3,"a",4,10,60))
plages.append(Plage(3,"c",5,10,60))


rdvs=[]
rdvs.append(Rdv(1,"b",3,10,31))

bl=[]
for i in range(len(demandes)+20):
    creerPlanning()
