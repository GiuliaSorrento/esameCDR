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

nodo: clienti che avevano fatto una fattura 

select  distinct c.*
from customer c , invoice i
where c.CustomerId = i.CustomerId 

due nodi sono collegati se hanno acquistato
entrambi dallo stesso artista

SELECT 
    c1.CustomerId AS Da_NodoA, 
    c2.CustomerId AS A_NodoB,
    COUNT(c1.ArtistId) AS Peso_Arco
FROM 
    (SELECT DISTINCT c.CustomerId, a.ArtistId 
     FROM invoice i, invoiceline il, track t, album a, customer c
     WHERE i.InvoiceId = il.InvoiceId 
       AND il.TrackId = t.TrackId 
       AND t.AlbumId = a.AlbumId 
       AND c.CustomerId = i.CustomerId) c1,
    (SELECT DISTINCT c.CustomerId, a.ArtistId 
     FROM invoice i, invoiceline il, track t, album a, customer c
     WHERE i.InvoiceId = il.InvoiceId 
       AND il.TrackId = t.TrackId 
       AND t.AlbumId = a.AlbumId 
       AND c.CustomerId = i.CustomerId) c2
       
WHERE c1.ArtistId = c2.ArtistId   
  AND c1.CustomerId <> c2.CustomerId 

GROUP BY c1.CustomerId, c2.CustomerId
