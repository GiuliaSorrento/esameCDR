#RIASSUNTI LABORATORI (VAI A VEDERLI SU GITHUB SE TI SERVE)

#LAB1--> random.shuffle(lista), read.splitlines, lista[i+2:i+6]  (inizio escluso, fine inclusa)
#LAB2 --> .strip.split(), .get per recuperare da un dizionario, elem not in lista/stringa, input.isdigit (true o false)
#LAB3 --> @property def parola(self): return self._parola (GET), @parola.setter def parola(self,valore): self._parola = valore
#LAB4 --> VIEW , ft.Switch (tema)
#LAB5 --> alertDialog (vai a vedere come funziona)

#LAB 6 --> YEAR, DAY, MONTH che puoi usare nelle query DOVE I CAMPI SONO DATETIME PER RECUPERARTI SOLO QUEI NUMERI (ex. ti serve solo l'anno)
#       -->e.control.data, e.control.value per raccogliere oggetto o valore(chiave/text) di un dato nel dd
#       --> def __post__init  per calcolare un valore che diventa proprieta di quel nodo nella dataclass, dopo che c'è stata l'inizializzazione
#       --> COALESCE che puoi usare nelle query: PRENDE IL PRIMO VALORE NON NULL DENTRO COALESCE  -->lo usi quando non è detto che ci sia quel valore (ex. non è detto che l'utente applicherà quel FILTRO)

#LAB7 E 8 (RICORSIONE) --> getSolOttima, _ricorsione, getScore, isAdmissible(dove vanno tutti i vincoli, se ci sono)
#                      --> alla fine della condizione di terminazione metti sempre il return
#                      --> USA EVENTO CORRENTE = PARZIALE[-1] così non devi scorrere con un for nella condizione di non terminazione
#                      --> fuori dalla condizione di non terminazione (CASO DI CORRENTE NON AMMISSIBILE IN PARZIALE) devi comunque chiamare ricorsione ma con aumento di posizione sennò non vai avanti
#                      --> diff(data1-data2).total_seconds()/3600  #differenza tempo in ore

#LAB9                  -->LEAST (A,B), GREATEST(A,B) , AVG(CAMPONUMERICO) nelle query (vedi bene)  (least e greates è perchè il grafo non è orientato devo considerare entrambe le direzioni)
#                      --> vedi bene query archi
#                      --> SE CONVERTI UN CAMPO DELLA VIEW IN INT DEVI FARE TRY-EXCEPT

#LAB10          -->query con IN e UNION (QUANDO HAI UNA TABELLA CHE TI DA GIA LE COPPIE ("CONFINE") FAI UNION TRA QUESTA TABELLA E SE STESSA E OTTIENI UN GRANDE ELENCO CON TUTTI I NODI PRESENTI IN ENTRAMBE LE COLONNE ALMENO UNA VOLTA
#----------------QUERY DEI NODI COMPLICATA
#                --> allG = list(self._grafo.degree(allNodi))  lista di tuple (nodo, grado)