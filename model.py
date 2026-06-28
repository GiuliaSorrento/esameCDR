#MODEL
#1) 5 ARCHI DI PESO MAGGIORE------------------------------------------------------------------
    # 5 archi di pesi maggiore
    edges = sorted(self._grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)
#--------------------------------------------------------------------------------------------------
#2) 5 NODI CON IL MAGGIOR NUMERO DI ARCHI USCENTI E LA SOMMA DEI PESI DI ESSI
    def get_node_max_uscenti(self):
        #ORDINO I NODI PER GRADO USCENTE (GRAFO.OUT_DEGREE(N)) DECR
        sorted_nodes = sorted(self._graph.nodes(), key=lambda n: self._graph.out_degree(n), reverse=True)
        result = []
        for i in range(min(len(sorted_nodes), 5)):
            peso_tot = 0.0
            #SCORRO GLI ARCHI USCENTI DEI PRIMI 5 NODI (GRAFO.OUT_EDGES(N, DATA=TRUE))
            #SENZA DAT=TRUE NON RECUPERI PESO
            for e in self._graph.out_edges(sorted_nodes[i], data=True):
                peso_tot += float(e[2].get("weight"))
            result.append((sorted_nodes[i], self._graph.out_degree(sorted_nodes[i]), peso_tot))
        return result
####--------------------------------------------------------------------------------------------------------------
#3) COMPONENTI CONNESSE:
# - components = list(nx.connected_components(self._graph)) #LISTA COMPONENTI CONNESSE
# n = nx.number_connected_components(self._graph.subgraph(parziale))  # NUM COMP CONNESSE DATO UN SOTTOGRAFO
#ORDINA COMP CONNESSE IN ORDINE DECR DI LUNGHEZZA
#orderedCom = sorted(nx.connected_components(self._graph), key=lambda connessa: len(connessa), reverse=True)
# CONNESSE DEBOLMENTE:  nx.weakly_connected_components(self._graph)

#-----COMP CONN DI DIM MAGGIORE, STAMPARNE I NODI IN SENSO DECRESCENTE DI GRADO-----
components = list(nx.connected_components(self._graph))  # lista di componenti connesse
largest = max(components, key=len)
subgraph = self._graph.subgraph(largest).copy()  # prendi questa componente non come set di nodi ma come sottografo
orderedNodes = sorted(subgraph.nodes(), key=lambda n: self._graph.degree(n), reverse=True)  # ORDINA PER GRADO DECRESC

#---------------TROVA COMPONENTE CONNESSA DI UN NODO SPECIFICO DEL GRAFO--------------
#           #Strategia 1
            dfsTree = nx.dfs_tree(self._graph, source)
            print("size connessa con dfs_tree", len(dfsTree.nodes()))

            #Strategia 2
            dfsPred = nx.dfs_predecessors(self._graph, source)
            print("size connessa con dfs_predecessors", len(dfsPred.values()))

            #Strategia 3
            conn = nx.node_connected_component(self._graph, source)  #COMP CONNESSA A PARTIRE DA UN NODO
            print("size connessa con node_connected_component", len(conn))

#--------------------TROVARE COMPONENTE CONN MAGGIORE E STAMPARE SUOI NODI IN ORDINE DECR DI PESO DEGLI ARCHI INCIDENTI---------------
    # la componente connessa di dimensione maggiore, e stamparne
    # tutti i nodi, ordinati in senso decrescente di peso massimo degli archi incidenti.

    # 1. Trovo la componente connessa di dimensione maggiore
    components = list(nx.connected_components(self._graph))
    if not components:
        return []  # Controllo di sicurezza se il grafo è vuoto

    largest_nodes = max(components, key=len)

    # 2. Estraggo il sottografo corrispondente
    sottografo = self._graph.subgraph(largest_nodes)

    nodi_con_peso_massimo = []

    # 3. Per ogni nodo nella componente, cerco l'arco incidente con peso massimo
    for nodo in sottografo.nodes:
        archi_incidenti = sottografo.edges(nodo, data=True)  # ESTRAE SOLO GLI ARCHI CHE INCIDONO SUL NODO N SPECIFICATO

        if archi_incidenti:
            # Trovo l'arco che ha il valore 'weight' massimo
            arco_massimo = max(archi_incidenti, key=lambda x: x[2]["weight"])
            peso_massimo = arco_massimo[2]["weight"]
        else:
            # Se il nodo è isolato nella componente (può succedere solo se la componente ha 1 solo nodo)
            peso_massimo = 0

        nodi_con_peso_massimo.append((nodo, peso_massimo))

    # 4. Ordino tutti i nodi in senso decrescente in base al peso massimo trovato
    nodi_ordinati = sorted(nodi_con_peso_massimo, key=lambda x: x[1], reverse=True)

    return nodi_ordinati  # Ritorna una lista di tuple (Oggetto_Constructor, peso_massimo)

#---------------------------------------------------------------------------------------------------------------------------------
#    ARTISTA CON INFLUENZA MASSIMA
"""L’influenza di un artista è calcolata come: peso archi uscenti − peso archi entranti. Inoltre, si visualizzino i 5
            archi con peso maggiore, in ordine decrescente."""
        infMax = 0
        nodoInf = None
        for a in self._graph.nodes():
            uscenti = self._graph.out_edges(a, data=True) #data= true per prendere il peso
            entranti = self._graph.in_edges(a, data=True)
            sommaUscenti = sum(dati["weight"] for u,v,dati in uscenti)
            sommaEntranti = sum(dati["weight"] for u,v,dati in entranti)
            influenza=sommaUscenti - sommaEntranti
            if influenza > infMax:
                infMax = influenza
                nodoInf = a

#-----------CAMMINO PIU LUNGO POSSIBILE (SCEGLI SE USA BFS O DFS) DEVI USARE DFS-------------------------------
        def getCammino(self, sourceStr):
            # VISUALIZZARE IL CAMMINO PIU LUNGO PARTENDO DA UN NODO
            # SCEGLERE ALG MIGLIORE TRA DFS E BFS

            source = self._idMap[int(sourceStr)]  # recupera nodo a partire dalla stringa id selezionata dall'utente
            lp = []  # lista che conterra il cammino

            # CAMMINO PIU LUNGO ---> DFS
            tree = nx.dfs_tree(self._graph, source)  # ALBERO CHE CONTIENE TUTTI I NODI RAGGIUNGIBILI DA SOURCE
            nodi = list(tree.nodes())

            for node in nodi:
                tmp = [node]  # lista temporanea che all'inizio contiene solo il nodo finale

                while tmp[0] != source:  # finche non arrivo al nodo di origine
                    pred = nx.predecessor(tree, source, tmp[0])  # recupero il padre del nodo che ho ora
                    tmp.insert(0, pred[0])

                if len(tmp) > len(lp):
                    lp = copy.deepcopy(tmp)

            return lp
#----------------------------------------------------------------------------------------------------------------
#----------GET5PRODOTTI PIU VENDUTI---------------------------------------------------------------------
    def getTop5ProdottiVenduti(self):
        #ovvero i nodi la cui somma dei pesi
        #degli archi uscenti meno la somma dei pesi degli archi entranti è massima.
        listaNodi=[]
        for n in self._graph.nodes:
            uscenti= self._graph.out_edges(n, data=True)  #lista di tuple con archi uscenti DA N e rispettivo peso
            entranti = self._graph.in_edges(n, data=True)
            somma_uscenti = sum(dati['weight'] for u, v, dati in uscenti) #SOMMO IL PESO DEGLI ARCHI USCENTI DA NODO N
            somma_entranti = sum(dati['weight'] for u, v, dati in entranti)
            score_n = somma_uscenti - somma_entranti
            listaNodi.append((n, score_n))   #creo una lista di nodi con tuple che hanno il nodo e il suo punteggio

        listaNodi.sort(key=lambda x: x[1], reverse=True)
        return listaNodi[:5]
#------------------------------------------------------------------------------------------------------------------------
#DIFFERENZA DI DUE CAMPI DATETIME IN GIORNI
# - diffEtaPiloti = (max(dateDiNascita) - min(dateDiNascita)).days

#------------------------------------------------------------------------------------------------------------------------


#-----------DATO UN NODO SOURCE, DAMMI LISTA ARCHI ADIACENTI IN ORDINE DECRESCENTE DI PESO------------
def getVicini(self, source):
    vicini = self._grafo.neighbors(source)  #GRAFO NON DIRETTO: ARCHI ADIACENTI: VICINI
    viciniTuples = []
    for v in vicini:
        viciniTuples.append((v, self._grafo[source][v]["weight"]))  #TUPLA (NODO, PESO) PER ARRIVARE A QUEL NODO DAL NODO SOURCE

    viciniTuples.sort(key=lambda x: x[1], reverse=True)  #ORDINE DECRESCENTE DEL SECONDO ELEMENTO DELLA TUPLA: PESO

    return viciniTuples

--------------------------------------------------------------------------------------------------------------------------------------
# LAZY LOADING: SE LA LOCALIZZAZIONE DI UN GENE E STATA GIA CERCATA
    #IN PASSATO, LA PRENDE DALLA MAPPA IN MEMORIA, ALTRIMENTI FA LA QUERY
    #MIRATA SOLO PER QUEL GENE
    #ELIMINA ERRRI DI SPAZI VUOTI O RECORD MANCANTI
    def get_localization_gene(self, g: Gene):
        if g.GeneID in self._localization_map:
            return self._localization_map[g.GeneID]
        else:
            return DAO.get_localization_gene(g, self._localization_map)

    def build_graph(self, ch_min, ch_max):
        self._graph.clear()
        nodes = DAO.get_nodes(ch_min, ch_max)
        self._graph.add_nodes_from(nodes)

        for i in range(len(nodes)-1):
            for j in range(i+1, len(nodes)):
                if (self.get_localization_gene(nodes[i]) == self.get_localization_gene(nodes[j]) and
                        nodes[i].GeneID != nodes[j].GeneID and
                        (nodes[i].GeneID, nodes[j].GeneID) in self._correlations_map):
                    peso = self._correlations_map[(nodes[i].GeneID, nodes[j].GeneID)]
                    if nodes[i].Chromosome < nodes[j].Chromosome:
                        self._graph.add_edge(nodes[i], nodes[j], weight=peso)
                    elif nodes[i].Chromosome > nodes[j].Chromosome:
                        self._graph.add_edge(nodes[j], nodes[i], weight=peso)
                    else:
                        self._graph.add_edge(nodes[i], nodes[j], weight=peso)
                        self._graph.add_edge(nodes[j], nodes[i], weight=peso)
#------------------------------------------------------------------------------------------------------------------------



