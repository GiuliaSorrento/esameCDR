"""1)Esiste un arco tra l’artista A e l’artista B se almeno un cliente ha acquistato brani di
entrambi gli artisti, con verso da A verso B se la popolarità di A è maggiore della popolarità di B. In caso i
nodi A e B abbiano la stessa popolarità, aggiungere due archi in entrambi i versi. Si calcoli la popolarità di un
artista come la somma di tutti i brani acquistati di quell’artista. Usare le tabelle invoceline e invoce per
determinare gli acquisti dei clienti. Il peso dell’arco tra l’artista A e l’artista B è la somma delle rispettive
popolarità."""

#SE LE QUERY DA FARE PER CALCOLARE ANCHE IL PESO SONO TROPPO COMPLICATE
#E SE POI NEL MODEL TI VIENE RICHIESTO ANCHE LA POPOLARITA COME DATO SINGOLO
#DEL NODO, L'APPROCCIO MIGLIORE E FARE QUERY SEMPLICI CHE NON CALCOLANO
#EFFETTIVAMENTE LA POPOLARITA E NEANCHE GLI ARCHI
#E FARE POI IL PROCESSO PIU COMPLICATO NEL MODEL
#IN QUESTO CASO VEDI BENE GITHUB DEL PROF SIMULAZIONE LAB 11 --> SE HAI PROBLEMI SU QUESTO DB VEDI BENE LA PROVA ESAME


#nb se devi fare collegamento tra customer ed employee --> c.supportRepId = e.EmployeeId