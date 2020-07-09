from random import uniform,choice
import matplotlib.pyplot as plot
from threading import Thread,RLock
from time import sleep 

SIMULATION0={'POPULATION':500,'PTRANSMISSION':0.3,'PMORT':0.05,'TMALADIE':15,'DUREESIMULATION':300}
SIMULATION1={'POPULATION':1500,'PTRANSMISSION':0.1,'PMORT':0.05,'TMALADIE':15,'DUREESIMULATION':300}
etats={0:'contaminable',1:'contamine',2:'immunise',3:'mort'}
TABLEAUNOIR=None
statistic=None
verru=RLock()
tcontamine=1
contamine=0
JOURS=0
cpt=0

def probabilite(p):
    return uniform(0, 1)<p

def init(SIMULATION):
    global TABLEAUNOIR
    global cpt
    TABLEAUNOIR=[[etats[0],0]for i in range(SIMULATION['POPULATION'])]
    cpt=SIMULATION['POPULATION'] 
    choice(TABLEAUNOIR)[0]=etats[1]  
    for individu in range(len(TABLEAUNOIR)):
        Thread(target=agent,args=(individu,SIMULATION)).start()    
    univers(SIMULATION)   

def univers(SIMULATION):
    global JOURS
    global cpt
    global statistic
    global tcontamine
    global contamine
    print('SIMULATION...\n')
    statistic=[]
    contamines=[]
    while JOURS<SIMULATION['DUREESIMULATION']:
        while True:
            sleep(0.05)
            if(cpt==SIMULATION['POPULATION']):
                break      
        immunise=0
        mort=0
        for i in range(SIMULATION['POPULATION']):
             if(TABLEAUNOIR[i][0]==etats[2]):
                immunise+=1    
             if(TABLEAUNOIR[i][0]==etats[3]):
                mort+=1
        statistic.append([tcontamine,immunise,mort])
        contamines.append(contamine)
        contamine=0
        JOURS+=1
        cpt=0
    print('\nFIN SIMULATION.\n')    
    plot.subplot(121)
    plot.title('statistic de cumulatifs journaliers')
    plot.xlabel('jours')
    plot.ylabel('individu')
    plot.plot(statistic)
    plot.legend([etats[1],etats[2],etats[3]])
    plot.subplot(122)
    plot.title('statistic de nouveau cas')
    plot.xlabel('jours')
    plot.ylabel('individu')
    plot.plot(contamines)
    plot.legend([etats[1]])
    plot.show()
    
def agent(i,SIMULATION):
    global cpt
    global tcontamine
    global contamine
    while True:
        sleep(0.05)
        if JOURS>0:
            break
    while JOURS<SIMULATION['DUREESIMULATION']:
        JOUR=JOURS
        if(TABLEAUNOIR[i][0]==etats[1]):
            if(TABLEAUNOIR[i][1]==SIMULATION['TMALADIE']):
               if(probabilite(SIMULATION['PMORT'])):
                   TABLEAUNOIR[i][0]=etats[3]
               else:
                   TABLEAUNOIR[i][0]=etats[2]
            else:
               if(probabilite(SIMULATION['PTRANSMISSION'])):
                   c=choice(TABLEAUNOIR)
                   if(c[0]==etats[0]):
                       c[0]=etats[1]
                       tcontamine+=1
                       contamine+=1
               TABLEAUNOIR[i][1]+=1       
        with verru:       
            print('je suis individu ',i,' je suis ',TABLEAUNOIR[i][0],' LE JOUR ',JOURS)
            cpt+=1
        while True:
            sleep(0.05)
            if(JOURS!=JOUR):
                break
                                        
init(SIMULATION0)    
    
    
