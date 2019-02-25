##Debug
* _conversation_start
  - utter_greet
  - utter_frageReiseDatum
* _buchung
  - datumHinreiseInSlot
  - utter_frageRueckreiseDatum
  - utter_default

##* _buchung
##  - datumRueckreiseInSlot
##  - utter_default
  
  
##  - utter_frageZeitSlot
##* _uhrzeit
##  - zeitInSlot
##  - utter_frageZeitSlotRueckreise
##* _uhrzeit
##  - zeitInSlot
##  - utter_frageVonWo
##* _buchung[GPE=von Berlin]
##  - verteilungGPEaufcityFrom
##  - utter_frageNachWo
##* _buchung[GPE=New York]
##  - verteilungGPEaufcityTo
##  - utter_VonWoNachWo
##  - utter_frageWieVieleTickets
##* _anzahlDerTickets[numberPassengers=20]
##  - preisBerechnen
##  - utter_frageReiseDatum
##* _buchung[reiseDatumHinreise=morgen]
##  - utter_frageZeitSlot
##* _uhrzeit[reiseUhrzeitHinreise=10:00]
