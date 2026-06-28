#CONTROLLER-STAMPA NODI COMP CONNESSE CON DIM MAGGIORE DI 1 E SUA DIM
componenti_connesse = self._model.get_connesse()
        self._view.txt_result.controls.append(ft.Text(f"\nLe componenti connesse sono:"))
        for connessa in componenti_connesse:
            if len(connessa) > 1:
                stringa = ""   #MODO PER FARE STRINGA UNICA ANCHE SE LE COSE LE "CALCOLI" SU LIVELLI DIVERSI
                for nodo in connessa:
                    stringa += f"{nodo.GeneID}, "
                stringa += f" | dimensione componente = {len(connessa)}"
                self._view.txt_result.controls.append(ft.Text(stringa))  #COMPONI E POI STAMPI TUTTO INSIEME
        self._view.update_page()

MODEL:
#CONNECTED_COMPONENTS RESTITUISCE UNA LISTA DI COMP CONNESSE CHE A LORO VOLTA SONO UNA LISTA DI NODI
return sorted(nx.connected_components(self._graph), key=lambda connessa: len(connessa), reverse=True)
#---------------------------------------------------------------------------------------
#DROPDOWN
#----NUMERI INTERI----------------------------------------------------------------
def fillDDYears(self):  # questo metodo lo chiamo nella view subito dopo aver creato i dd, perchè si devono riempire appena la pagina viene caricata
    years = self._model.getAllYears()
    for y in years:
        # sono numeri interi quindi ci conviene riempirli direttamente così
        self._view._ddAnno1.options.append(ft.dropdown.Option(y))
        self._view._ddAnno2.options.append(ft.dropdown.Option(y))
    self._view.update_page()

#----OGGETTI---------------------------------------------------------------------------------------------------------------------------------------------------------
#NB. NON DEVI FARE NULLA NELLA VIEW
 self._view._ddSquadra.options.append(
                ft.dropdown.Option(data = t,
                                   text = t.name,
                                   on_click = self.readDDTeams)
            )

        self._view.update_page()


    def readDDTeams(self, e):
        if e.control.data is None:
            self._choiceTeam = None   #da inizializzare nel costruttore del controller
        else:
            self._choiceTeam = e.control.data
        print(f"Selezionato il team {self._choiceTeam}")

#--------------------CONTROLLER-SE DEVI RECUPERARE IL DATO DA UN DD CON MEMORIZZATO IL DATA E IL TEXT------------------------
 # 1. Recuperiamo il TESTO selezionato nel dropdown
        scelta_testo = self._view._ddcategory.value

        # 2. Troviamo l'opzione corrispondente per estrarre l'oggetto Category nascosto nel .data
        categoria = None
        if scelta_testo is not None:
            for option in self._view._ddcategory.options:
                if option.text == scelta_testo:
                    categoria = option.data
                    break
#---------------------------------------------------------
#NB RICORDATI DI ABILITARE (disabled = False) NEL CONTROLLER I BOTTONI O I DD CHE SONO DISABILITATI INIZIALMENTE NELLA VIEW
#-------------------------------------------------------------------------------------------------
#DUE DROPDOWN A CASCATA, LA SELEZIONE DEL PRIMO DEVE ATTIVARE L'ALTRO
    def fillDDYears(self):
        years = self._model.getAllYears()
        for y in years:
            self._view.ddyear.options.append(ft.dropdown.Option(y))
        self._view.ddyear.on_change = self.fillDDStatesByYear #NO PARAMETRI
        self._view.update_page()

    #NEL SECONDO DD SERVE IL PARAMETRO EVENTO
    def fillDDStatesByYear(self, e=None):   #DEVO METTERLO PERCHE VIENE SCATENATO DA ON CHANGE
        a = self._view.ddyear.value
        if a is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("Selezionare un anno per procedere"))
            self._view.update_page()
            return
        try:
          anno = int(a)
        except:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text("anno non numerico"))
            self._view.update_page()

        stati = self._model.getStatesByYear(anno)
        for s in stati:
            self._view.ddstate.options.append(ft.dropdown.Option(key=s.id, text = s.name, data = s))
        self._view.update_page()
#----------------------------------------------------------------------------------------------------
#NB SE TI DA ERRORE DI TXTRESULT CHE NON ESISTE E PERCHE VIENE CREATO DOPO CHE CHIAMO FILLDD NELLA VIEW
#QUINDI SPOSTA FILLDD PIU IN BASSO DEL TXTRESULT CHE TI DA ERRORE
#---------------------------------------------------------------------------------------------------
#                      CREATE ALERT E CONTROLLI SUI TXTIN IN INPUT DELL'UTENTE PRIMA DI FARE IL GRAFO --> LI FAI CON TRY-EXCEPT
 def handle_graph(self, e):
        # read latitude
        try:
            latitude = float(self._view.txt_latitude.value)
        except:
            self._view.create_alert(
                f"La latitudine deve essere un valore numerico compreso tra {self._min_lat} e {self._max_lat}")
            return
        if latitude < self._min_lat or latitude > self._max_lat:
            self._view.create_alert(
                f"La latitudine deve essere un valore numerico compreso tra {self._min_lat} e {self._max_lat}")
            return

        # read longitude
        try:
            longitude = float(self._view.txt_longitude.value)
        except:
            self._view.create_alert(
                f"La longitudine deve essere un valore numerico compreso tra {self._min_lng} e {self._max_lng}")
            return
        if longitude < self._min_lng or longitude > self._max_lng:
            self._view.create_alert(
                f"La longitudine deve essere un valore numerico compreso tra {self._min_lng} e {self._max_lng}")
            return

        # read shape
        if self._view.ddshape.value is None or self._view.ddshape.value == "":
            self._view.create_alert("Selezionare una shape!")
            return
        shape = self._view.ddshape.value

        self._model.buildGraph(latitude, longitude, shape)
        n,a = self._model.getGraphDetails()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Grafo correttamente creato con {n} nodi e {a} archi"))
        nodi, archi = self._model.getDettagli()
        self._view.txt_result1.controls.append(ft.Text(f"nodi con grado maggiore:"))
        for n, g in nodi:
            self._view.txt_result1.controls.append(ft.Text(f"{n} grado {g}"))
        self._view.txt_result1.controls.append(ft.Text(f"archi con peso maggiore:"))
        for e in archi:
            self._view.txt_result1.controls.append(ft.Text(f"{e[0]}--{e[1]} peso {e[2]["weight"]}"))

        self._view.update_page()
