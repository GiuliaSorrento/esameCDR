#RICORSIONE

#QUANDO CONOSCI GIA IL NODO SOURCE NON PARTIRE CON PARZIALE LISTA VUOTA MA CON PARZIALE CON NODO SOURCE GIA DENTRO

#for n in self._graph.successors(parziale[-1]):  #SCORRO I SUCCESSORI DEL NODO DOPO, LO FAI QUANDO NEL CAMMINO I NODI DEVONO SEGUIRE IL VERSO DEGLI ARCHI

# NB I GRAFI DIRETTI HANNO I SUCCESSORS, I GRAFI NON ORIENTATI HANNO I NEIGHBORS E BASTA

#CAMMINO SEMPLICE --> IL NODO NON DEVE ESSERE MAI VISITATO PIU DI UNA VOLTA (DEVE COMPARIRE IN PARZIALE UNA SOLA VOLTA)

#SE LA CONDIZIONE E' CHE IL CAMMINO DEVE PROCEDERE IN SENSO STRETTAMENTE DECRESCENTE DI PESO, TI CONVIENE CHIAMARE LA RICORSIONE
#CON PARAMETRI PARZIALE E PESO PRECEDENTE (CHE ALLA PRIMA CHIAMATA VERRA IMPOSTATO A NONE)
#POI if peso_precedente is None or peso_precedente > pesoSuccessivo: faccio parziale.append, chiamo ricorsione con PESO SUCCESSIVO e parziale.pop

#Trovare un CAMMINO SEMPLICE LUNGHEZZA MASSIMA tale che (condizione)-->(LAB SIMULAZIONE 11 e 12)-----------------------------------------
        def getSolOttima(self):
            self._optPath = []
            self._optScore = 0
            # DEVI PROVARE A FAR PARTIRE IL CAMMINO DA OGNI NODO DEL GRAFO : PERCHE NON TI VIENE DATO UN NODO SOURCE
            for nodo_partenza in self._grafo.nodes():
                parziale = [nodo_partenza]
                self._ricorsione(parziale)
            return self._optPath, self._optScore

        def _ricorsione(self, parziale):
            # Condizione di aggiornamento: ogni volta che arriviamo qui,
            # controlliamo se il cammino attuale è il più lungo trovato finora.
            if len(parziale) > self._optScore:
                self._optScore = len(parziale)
                self._optPath = copy.deepcopy(parziale)

            # Esplorazione dei vicini (neighbors)
            nodo_corrente = parziale[-1]    #E PIU UTILE RICAVARSI IL NODO CORRENTE PIUTTOSTO CHE USARE UN INDICE

            for vicino in self._grafo.neighbors(nodo_corrente): #ESPLORO VICINI SE GRAFO NON ORIENTATO E SUCCESSORS SE GRAFO ORIENTATO
                # Vincolo 1: Cammino SEMPLICE (il nodo non deve essere già stato visitato)
                if vicino not in parziale:
                    # Vincolo 2: Età strettamente decrescente
                    # NOTA: Se vicino.eta < nodo_corrente.eta (oppure controlla le date di nascita)
                    if vicino.date_of_birth > nodo_corrente.date_of_birth:
                        # Svolta (Backtracking)
                        parziale.append(vicino)

                        # Ricorsione: non serve l'indice 'i', andiamo avanti finché troviamo vicini validi
                        self._ricorsione(parziale)

                        # Contro-svolta
                        parziale.pop()
#-----------------------------------------------------------------------------------------------------------------------
#--------------------------RICORSIONI CON MIN DIFF ETA E NODI TUTTI IN DIVERSE COMP CONNESSE  E K ELEMENTI NEL CAMMINO ----------------------------------------------------
def getListaPilotiOttima(self, k):
    self._optListpiloti = []
    self._minDistGiorni = 100 * 365  # voglio minimizzare la differenza di eta tra più giovane e più vecchio dei piloti (parto da un dato alto in termini di gg)

    components = list(nx.connected_components(self._graph))

    if len(components) < k:
        # allora non ho abbastanza componenti connesse da cui pescare e non posso trovare una soluzione
        return None, 0

    parziale = []
    self._ricorsione(components, k, parziale, 0)

    return self._optListpiloti, self._minDistGiorni


def _ricorsione(self, components, k, parziale,
                indexComponente):  # indice di quale componente sto in questo momento decidendo se inserire nella mia lista di piloti oppure no
    # condizione di ottimalità
    if len(parziale) == k:
        # ho una soluzione accettabile
        dateDiNascita = [p.dob for p in parziale]
        diffEtaPiloti = (max(dateDiNascita) - min(dateDiNascita)).days  # data.days
        if diffEtaPiloti < self._minDistGiorni:
            self._optListpiloti = copy.deepcopy(parziale)
            self._minDistGiorni = diffEtaPiloti
        return

    # condizione di terminazione
    # esco se l'indice che indica quale comp connessa sto considerando a questa iterazione è diventato maggiore o uguale al
    # numero di componenti connesse totali, perchè vuol dire che non ho altre componenti da cui pescare
    # altro motivo, se non ho abbastanza componenti rimanenti per arrivare a k piloti in parziale

    if (indexComponente >= len(components)) or (len(components) - indexComponente < (k - len(parziale))):
        return

    # se non sono uscito , allora posso aggiungere ancora piloti. Per questa componente di indice indexComponente
    # provo a ingaggiare un pilota oppure a non ingaggiare nessuno

    # caso 1, inserisco un pilota appartenente a questa compo conessa. In questo branch provo tutti i piloti che fanno parte
    # della componente connessa in esame
    componente = components[indexComponente]
    for pilota in componente:
        parziale.append(pilota)
        self._ricorsione(components, k, parziale, indexComponente + 1)
        parziale.pop()

    # caso 2, mi tengo un branch di esplorazione in cui io non ho preso proprio nessuno da questa componente.
    self._ricorsione(components, k, parziale, indexComponente + 1)  # scorro alla componente successiva

    #----------------------PER IMPORRE CHE OGNI NODO DEL PERCORSO OTTIMO APPARTENGA A UNA COMPONENTE CONNESSA DISTINTA--------
    # COMPORTAMENTO 1: Provo ad AGGIUNGERE il nodo corrente (se valido)
    valido = True
    for inserito in parziale:
        # Se c'è un cammino, appartengono alla stessa componente connessa -> NON VALIDO
        if nx.has_path(self._graph, nodo_corrente, inserito):
            valido = False
            break
#--------------------------------------------------------------------------------------------------------------------

#MODO PER CALCOLARE SOMMA DEI PESI DI PARZIALE SEGUENDO ORDINE DEGLI ARCHI/NODI (GRAFO DIRETTO):
        #QUANDO DEVI MASSIMIZZARE/MINIMIZZARE IL PESO DI PARZIALE
        def _score(self, parziale):
            if len(parziale) < 2:
                return 0
            peso = 0
            # DEVI PER FORZA SCORRERE COSI PERCHE SENNO NON RISPETTI ORDINE DEI NODI IN PARZIALE
            for i in range(len(parziale) - 1):
                u = parziale[i]
                v = parziale[i + 1]
                peso += self._graph[u][v]["weight"]
            return peso
#--------------------------------------------------------------------------



#---------------------------------RICORSIONE CON RIMANENTI E ALTRE COSE PARTICOLARI:-----------------------------------------------------------------------------------------
        def get_list_nodes(self):
            self._bestListNodes = []
            self._bestScore = len(self._graph.nodes)
            self._bestLen = 0  #STO CERCANDO LISTA DI NODI DI LUNGHEZZA MASSIMA

            allNodes = list(self._graph.nodes)   #.NODES NON MI DA SUBITO UNA LISTA QUINDI DEVO TRASFORMARLA PER POTERCI LAVORARE
            allNodes.sort(key=lambda x: x.GeneID)  #LA LISTA FINALE DI LUNGHEZZA MAX DEVE ESSERE ORDINATA, ORDINO GIA ALL'INIZIO TUTTI I NODI COSI LI PRENDO UNO ALLA VOLTA GIA ORDINATI

            for root in allNodes:   #LA REGOLA "O TUTTI ESSENTIALS O TUTTI NON ESSENTIALS" VIENE DETTATA DA ROOT, VISTO CHE NON E SPECIFICATA DEVO PROVARE TUTTE LE ROOT
                rimanenti = copy.deepcopy(allNodes)   #USO RIMANENTE
                rimanenti.remove(root)
                rimanenti = [x for x in rimanenti if x.Essential == root.Essential]  #HA MEMORIZZATO NEI NODI ANCHE IL CAMPO ESSENTIAL PER ESSERE PIU COMODI

                self._ricorsione([root], list(rimanenti))  #CHIAMI RICORSIONE CON PARZIALE[ROOT] E RIMANENTI

            print(self._bestLen, self._bestScore)
            return self._bestListNodes, self._bestLen, self._bestScore

        def _ricorsione(self, parziale, rimanenti):
            if len(parziale) > self._bestLen:   #LISTA LUNGHEZZA MASSIMA
                self._bestLen = len(parziale)
                self._bestScore = self._getScore(parziale)
                self._bestListNodes = copy.deepcopy(parziale)
                if len(parziale) == self._bestLen:  #ALTRA CONDIZIONE PROBLEMA
                    if self._getScore(parziale) < self._bestScore:
                        self._bestScore = self._getScore(parziale)
                        self._bestListNodes = copy.deepcopy(parziale)

            if len(rimanenti) == 0:
                return

            for n in rimanenti:
                if n.GeneID > parziale[-1].GeneID:  #DEVO SEGUIRE ORDINE
                    parziale.append(n)
                    rimanenti.remove(n)   #RIMUOVERE DA RIMANENTI
                    self._ricorsione(parziale, rimanenti)
                    parziale.remove(n)
                    rimanenti.append(n)  #AGGIUNGERE A RIMANENTI

        def _getScore(self, parziale):
            return nx.number_connected_components(self._graph.subgraph(parziale))  #NUM COMP CONNESSE DATO UN SOTTOGRAF0O


#-------------------RICORSIONE CON VINCOLI, PUNTEGGI E SUCCESSORS ------------------------------------------------------
    def getSolOttima(self):
        self._camminoOttimo = []
        self._maxPunteggio = float('-inf')  #SE VUOI PUNTEGGIO MAX MA PUO ESSERE ANCHE NEGATIVO PARTI DA -INF

        #non conosciamo source:
        for nodo_partenza in self._graph.nodes():
            parziale = [nodo_partenza]
            self._ricorsione(parziale)
        return self._camminoOttimo, self._maxPunteggio

    def _ricorsione(self, parziale):
          if self.getScore(parziale) > self._maxPunteggio:
              self._maxPunteggio = (self.getScore(parziale))
              self._camminoOttimo = copy.deepcopy(parziale)


          nodo_corrente = parziale[-1]
          for vicino in self._graph.successors(nodo_corrente):  #scorro seguendo direzione archi
              if self.isAdmissible(parziale, vicino):
                  parziale.append(vicino)
                  self._ricorsione(parziale)
                  parziale.pop()

    def getScore(self, parziale):
        #+100 per ogni avvistamento nel cammino
        #+200 se avvistamento nello stesso mese del precedente
        #non applicabile al primo avvistamento
        if not parziale:
            return 0

        score_partenza = len(parziale) * 100
        for i in range(1,len(parziale)): #escludo il primo
            corrente = parziale[i]
            precedente = parziale[i-1]
            if corrente.datetime.month == precedente.datetime.month:
                score_partenza += 200

        return score_partenza


    def isAdmissible(self, parziale, n):
        #durata strettamente crescente
       #non piu di 2 avvistamenti nello stesso mese
       #segui direzione archi
       conteggio_mesi = {}
       for p in parziale:
           m = p.datetime.month
           conteggio_mesi[m] = conteggio_mesi.get(m, 0) + 1

       mese = n.datetime.month
       if conteggio_mesi.get(mese, 0) >= 3:   #METTI VALORE DI DEFAULT PERCHE NON SAI SE QUEL MESE E GIA PRESENTE NEL DIZ O NO
           return False

       precedente = parziale[-1]
       if precedente.duration >= n.duration:
           return False

       if n in parziale:  #non puo gia essere presente
           return False

       return True
#---------------------------------------------------------------------------------------
#           RICORSIONE CON NODO SOURCE E NODO DEST GIA DEFINITI IN PARTENZA
    def getSolOttima(self,source,end,lun):
        self._optPath=[]
        self._optScore=0
        parziale = [source]  #QUANDO CONOSCI GIA ORIGINE PUOI DIRETTAMENTE METTERLA IN PARZIALE
        self._ricorsione(parziale,end,lun)
        return self._optPath, self._optScore

    def _ricorsione(self, parziale,end,lun):
        #condizione di terminazione
        if len(parziale)==lun:
                if parziale[-1]==end and self.getScore(parziale)>=self._optScore:
                    self._optPath= copy.deepcopy(parziale)
                    self._optScore = self.getScore(parziale)
                return
        #condizione di non terminazione
        for n in self._graph.successors(parziale[-1]):  #SCORRO I SUCCESSORI DEL NODO DOPO, LO FAI QUANDO NEL CAMMINO I NODI DEVONO SEGUIRE IL VERSO DEGLI ARCHI
                if n not in parziale:
                    parziale.append(n)
                    self._ricorsione(parziale,end, lun)
                    parziale.pop()

    def getScore(self,parziale):
        peso = 0
        for i in range(0, len(parziale)-1):
                peso+=self._graph[parziale[i]][parziale[i+1]]['weight']
        return peso