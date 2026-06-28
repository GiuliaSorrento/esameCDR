#QUERY:

#NB. QUANDO FAI QUERY DEGLI ARCHI DEVI SEMPRE ANCHE INSERIRE LE CONDIZIONI CHE SERVONO PER LA QUERY DEI NODI, SENNO TI CREI
#DEGLI ARCHI CHE SONO TRA NODI CHE MAGARI NON ESISTONO: QUERY ARCHI = CONDIZIONI ARCHI + CONDIZIONI NODI
# - BETWEEN valore1 and valore2 nelle condizioni-->INCLUDE ESTREMI
# - IS NOT NULL nelle condizioni
# - se hai due tabelle che non sono collegate sfrutta la tabella che ti sarà più utile nelle condizioni come tabella di collegamento tra le due
# - per trovare gli archi molte volte devi unire due tabelle uguali e selezionare due nodi che corrispondono a tutte le singole coppie

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#3 MODI PER TROVARE ARCHI:
# 1) QUERY ID1, ID2 E PESO FROM DUE TABELLE IDENTICHE CREATE DA ME

#Due nodi sono connessi da un arco se e solo se entrambi i prodotti sono stati venduti almeno una volta nel
#range selezionato (estremi inclusi). L’arco è uscente dal nodo con numero di vendite maggiore ed entrante
#nel nodo con numero di vendite minore. In caso di parità di numero di vendite, si inseriscano entrambi gli
#archi. Suggerimento: per confrontare date in un range in SQL, è possibile usare l’operatore “BETWEEN”. Nel
#caso in cui un nodo non sia stato venduto nel range selezionato, quel nodo deve rimanere isolato. Il peso
#dell’arco è pari alla somma delle vendite dei prodotti nel range considerato (numero di vendite distinte, non
#si considerino eventuali vendite di più di un pezzo).
            """select t1.product_id as id1, t2.product_id as id2, t1.n as nt1, t2.n as nt2, t1.n+t2.n as peso   #PRENDO ENTRAMBI I PRODOTTI, ENTRAMBE LE VENDITE E IL PESO DELL'ARCO COME LORO SOMMA
                                from (SELECT p.product_id, count(*) as n            #FACCIO LA FROM TRA DUE TABELLE IDENTICHE CHE INSERISCONO TUTTE LE CONDIZIONI E RECUPERANO ID DEL PRODOTTO E NUMVENDITE
                                FROM  products p, order_items oi, orders o
                                WHERE o.order_id = oi.order_id
                                and oi.product_id = p.product_id
                                and o.order_date between %s and %s
                                and p.category_id = %s
                                group by(p.product_id )
                                ) t1,
                                (SELECT p.product_id, count(*) as n
                                FROM  products p, order_items oi, orders o
                                WHERE o.order_id = oi.order_id
                                and oi.product_id = p.product_id
                                and o.order_date between %s and %s
                                and p.category_id = %s
                                group by(p.product_id )
                                ) t2
                                where t1.product_id <> t2.product_id         #PRENDO SOLO COPPIE DI PRODOTTI DISTINTI (PERCHE GRAFO ORDINATO)
                                and t1.n >= t2.n                             #>= MI PERMETTE DI IDENTIFICARE IL VERSO DA MAGGIORE A MINORE VENDITE SENZA DOVERLO FARE NEL MODEL
                                order by peso desc"""
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 2) QUERY DOVE PRENDI DUE TABELLE GIA ESISTENTI UGUALI E LE USI INSIEME AD ALTRE ULTERIORI PER FARE JOIN E TROVARE ID1, ID2 E PESO
"""select r1.driverId as d1, r2.driverId  as d2 , count(*) as peso
                from  results r1, results r2, races r
                where r.raceId = r1.raceId and r.raceId	=r2.raceId 
                and r1.constructorId = r2.constructorId  
                and r1.driverId >r2.driverId    
                and r1.`position`  is not null
                and r2.`position` is not null 
                and r.`year` between %s and %s     #INCLUDI SEMPRE ANCHE LE CONDIZIONI DEI NODI
                group by r1.driverId , r2.driverId 
                order by peso desc"""
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#3 RECUPERO DATI CHE METTO IN UNA LISTA/MAPPA O MEMORIZZO NELLA DATACLASS E POI CALCOLO ARCHI E PESO NEL MODEL
@staticmethod
            def getSalariesTeam(year, idMapTeams):
                conn = DBConnect.get_connection()

                result = []

                cursor = conn.cursor(dictionary=True)
                #ESATTAMENTE STESSO PROCEDIMENTO CHE FACCIO NEL DB CHINOOK SIMULAZIONE LAB 11 (NON USO QUERY PER TROVARE ARCHI O PESO MA SOLO IL PESO SINGOLO DEI NODI, POI ARCHI E PESO TOT LO FACCIO NEL MODEL)
                query = """select t.ID, t.teamCode, sum(s.salary) as totSalary
                               from salaries s, teams t, appearances a 
                               where s.`year` = t.`year` and t.`year` = a.`year` and a.`year` = %s
                               and t.ID = a.teamID and a.playerID = s.playerID 
                               group by t.ID , t.teamCode """

                cursor.execute(query, (year,))

                mapSalary = {}
                for row in cursor:
                    mapSalary[idMapTeams[row["ID"]]] = row["totSalary"]

                cursor.close()
                conn.close()
                return mapSalary
#QUANDO GLI ARCHI SI CONNETTONO CON NULLA DI NUOVO E LA NOVITA E SOLO NEL CALCOLO DEL PESO CHE E SINGOLO PER OGNI NODO E POI VA SOMMATO PER L'ARCO
#FAI SOLO LA QUERY DEL PESO E TE LA ACCOPPI A OGNI NODO E POI CREI NEL MODEL
#E POI NEL MODEL:
# - se ti dice che gli ARCHI SONO TUTTE LE COPPIE DI NODI DISTINTE, non devi fare la query
#   fai solo la query per recuperarti il "PESO SINGOLO DI OGNI NODO" CHE METTI IN UNA MAPPA CON CHIAVE I NODI
#   poi nel model USI ITERTOOLS PER TROVARE TUTTE LE COPPIE DISTINTE
myedges = list(itertools.combinations(self._nodi, 2))  #ACCOPPIO OGNI NODO DI DUE IN DUE
        self._grafo.add_edges_from(myedges)

        mapSalary = DAO.getSalariesTeam(year, self._idMapTeams)  #LA QUERY DEL PESO MI
# RESTITUISCE UNA MAPPA CHE COLLEGA OGNI NODO AL SUO "PESO SINGOLO" (UN PO COME SE SALARIO FOSSE POPOLARITA)
        for e in self._grafo.edges:
            sal1 = mapSalary[e[0]]
            sal2 = mapSalary[e[1]]
            peso = sal1+sal2   #POI NEL MODEL DI CALCOLI IL VERO PESO DELL'ARCO
            self._grafo[e[0]][e[1]]["weight"] = sal1+sal2    #il peso lo posso anche aggiungere dopo che ho creato gli archi
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#QUERY GRAFO ORIENTATO---------------------------------------------
SELECT
    c1.constructorId AS da_scuderia,  -- <--- NODO PARTENZA (A)
    c2.constructorId AS a_scuderia,   -- <--- NODO ARRIVO (B)
    (c1.conteggio - c2.conteggio) AS peso
FROM
    ( ... Sotto-query 1 ... ) c1,
    ( ... Sotto-query 2 ... ) c2
WHERE
    c1.constructorId != c2.constructorId
    AND c1.conteggio > c2.conteggio; -- <--- LA DIREZIONE VIENE DECISA QUI

#-------------------------------------------------------------------------
"PER RECUPERARE DATA PIU VECCHIA IN SQL USA MIN(CAMPO DATA)"

#GESTISCI DIFFERENZA DI DATA IN SQL (PUOI ANCHE CIRCONDARLO DA ABS)
#AND o1.data < o2.data
#AND DATEDIFF(o2.data, o1.data) <= %s
#DATEDIFF(DATA+GRANDE, DATA+PICCOLA) COSI SEI SICURA CHE NON E NEGATIVA

#nb. QUANDO ORDINI UN PRODOTTO POSSONO ESSERCI PIU QUANTITA DI QUEL PRODOTTO, DEVI FARE SUM DI QUANTITY NON COUNT DELL'ID PRODOTTO

#COALESCE+NULLIF: Prova a dividere la somma degli oggetti per i giorni di differenza.
        # Se i giorni sono 0 (che farebbe crashare il sistema), fai finta che non sia successo nulla e prendi semplicemente la somma totale
        # degli oggetti come peso dell'arco.
        #BASTA IMPORRE CHE LA DATEDIFF SIA MAGGIORE DI 0 NELLE CONDIZIONI


#--------------------------------------------------------------------------------------------------------------------------------------
#ESERCIZIO IN CUI PER OGNI NODO (CONSTRUCTOR) MI FACEVA MEMORIZZARE UNA DIZIONARIO{ANNO:LISTA OGGETTI RISULTATI}
#IL FATTO CHE MI FACESSE FARE TUTTO QUESTO MI DOVEVA FAR CAPIRE CHE IO DOVEVO FARE GLI ARCHI DIRETTAMENTE NEL MODEL UTILIZZANDO QUESTA LISTA DI RISULTATI
#CHE AVEVO PER OGNI NODO
def _calcolaPesoArco(self, n1, n2):
    # il peso dell'arco è definito come il numero totale di piloti
    # che hanno raggiunto il traguardo. Se ci sono 4 piloti
    # che non hanno finito la gara (il campo position è null) allora il
    # valore da considerare per quell'anno è nTotPiloti - 4
    # L'arco non esiste se uno dei due team non ha mai partecipato nel range selezionato
    # (ovvero, il nodo deve rimanere isolato)
    peso = 0

    if len(n1.results.values()) == 0 or len(n2.results.values()) == 0:  #SE I RISULTATI SONO LUNGHI 0 NON HANNO PARTECIPATO IN QUEGLI ANNI
        return peso

    for r in n1.results.values():  # per ogni anno
        for p in r:  # per ogni pilota e per ogni gara
            if p.position is not None:
                peso += 1     #PESO=SOMMA DEI PILOTI CHE HANNO GAREGGIATO IN QUEGLI ANNI PER QUEL TEAM N1

    for r in n2.results.values():  # per ogni anno
        for p in r:  # per ogni pilota e per ogni gara     #STESSA COSA PER TEAM N2
            if p.position is not None:
                peso += 1    #IL PESO SOMMA I VALORI DI ENTRAMBI I TEAM PERCHE SONO CONNESSI DA ARCO

    return peso

# Aggiunta archi non richiede una query perchè abbiamo già importato i risultati
        for i in self._nodes:
            for j in self._nodes:
                if i.constructorId < j.constructorId and self._calcolaPesoArco(i, j) > 0:
                        peso = self._calcolaPesoArco(i, j)
                        self._graph.add_edge(i, j, weight=self._calcolaPesoArco(i, j))
#-------------------------------------------------------------------------------------------------------------


#QUERY FLIGHT DELAYS---------------------------------
#COALESCE: PRENDI IL PRIMO VALORE NON NULL DENTRO COALESCE, COSì NON DEVI SCRIVERE DUE QUERY, 0 E IL VALORE DI DEFAUL SE T1.N E NULL
            """select t1.ORIGIN_AIRPORT_ID , t1.DESTINATION_AIRPORT_ID , coalesce(t1.n,0) + coalesce(t1.n,0) as peso
                                FROM (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
                                from flights f
                                group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                                order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) t1
                                left Join (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
                                from flights f
                                group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                                order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) t2
                                on t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID 
                                and t1.DESTINATION_AIRPORT_ID = t2.ORIGIN_AIRPORT_ID 
                                where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID or t2.ORIGIN_AIRPORT_ID is Null
                               """
    #SE HAI COSE TIPO ANDATA E RITORNO TI CONVIENE GUARDARE QUESTO:
    #LEFT JOIN: PRENDE TUTTE RIGHE DELLA PRIMA TABELLA (T1) E POI SE C'E CORRISPONDENZA UNISCE LE COLONNE T1 CON QUELLE DI T2
              #SE NON CE CORRISPONDENZA MANTIENE RIGA DI T1 E LE COLONNE DI T2 LE RIEMPE CON NULL, PER QUESTO CHE POI USA COALESCE
              #NELL'ON SI METTE LA CONDIZONE INCROCIATA PER CERCARE ANDATA E RITORNO
              #NEL WHERE CONDIZIONE DI < PER EVITARE DUPLICATI
              #IS NULL SERVE PER ASSICURARSI DI METTERE LE RIGHE ANCHE SE NON ESISTE RITORNO
#------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#ESTRAZIONE DATI DAO DOPO QUERY:
# - for row in cursor:
#      results.append(Arco(idMapDriver[row["d1"]], idMapDriver[row["d2"]], row["peso"]))
# - for row in cursor:
#       results.append(Driver(**row))     UNPACK(solo quando fai select esattamente di tutti gli attributi con stesso identico nome e ordine (ex. select *))


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
