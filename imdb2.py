#1)Esiste un arco tra due attori se hanno recitato almeno in uno stesso film. Il peso è pari alla somma degli incassi dei film
#  in comune.
#NB LA QUERY DEGLI ARCHI DEVE SEMPRE CONTENERE ANCHE LE CONDIZIONI DEI NODI PERCHE SENNO CREI ARCHI ANCHE TRA NODI CHE NON ESISTONO
@staticmethod
def getAllEdgesPesati(voto1, voto2, idMapAttori):
    conn = DBConnect.get_connection()

    results = []

    cursor = conn.cursor(dictionary=True)
    query = """select rm1.name_id as a1, rm2.name_id as a2,
                sum( cast(replace(replace(m.worlwide_gross_income, '$', ''),',', '') as unsigned)) as peso        
                   from role_mapping rm1, role_mapping rm2, movie m, ratings r, names as n1, names as n2
                   where m.id = rm1.movie_id
                   and m.id = rm2.movie_id
                   and m.id = r.movie_id
                   and rm1.name_id = n1.id
                   and rm2.name_id = n2.id
                   and n1.date_of_birth IS NOT NULL
                   and n2.date_of_birth IS NOT NULL
                   and rm1.name_id < rm2.name_id
                   and r.avg_rating >= %s
                   and r.avg_rating <= %s
                   and m.worlwide_gross_income is not null
                   and m.worlwide_gross_income like '$%'
                   group by rm1.name_id, rm2.name_id 
                   """

    cursor.execute(query, (voto1, voto2,))

    for row in cursor:
        id1 = row["a1"]
        id2 = row["a2"]
        #SE TI DA PROBLEMI DI KEYERROR, FAI COSI
        #SUCCEDE SE PER FARE GLI ARCHI DEVI INSERIRE ULTERIORI CONDIZIONI OLTRE A QUELLE DEI NODI
        #COME IN QUESTO CASO DELL'INCOME
        # Crea l'arco solo se entrambi gli attori sono stati effettivamente caricati come nodi
        if id1 in idMapAttori and id2 in idMapAttori:
            results.append(Arco(idMapAttori[id1], idMapAttori[id2], row["peso"]))
    cursor.close()
    conn.close()
    return results