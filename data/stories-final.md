##Main
* conversation_start
  - utter_greet
  - utter_frageVonWo
* buchung
  - GPEoderCityInSlot
  - utter_frageNachWo
* buchung
  - GPEoderCityInSlot
  - utter_frageWieVieleTickets
* anzahldertickets
  - utter_frageReiseDatum
* buchung
  - datumHinreiseInSlot
  - utter_frageZeitSlot
* _uhrzeit
  - zeitInSlot
> check_rueckReiseGesetzt
> backToMain
  - utter_fragePaymentType
* zahlungstypen
  - utter_frageEmailadresse
* emailadressen
> check_buchungBestaetigtGesetzt

> check_rueckReiseGesetzt
  - utter_frageObRueckreise
* affirm
  - utter_frageRueckreiseDatum
* buchung
  - datumRueckreiseInSlot
  - utter_frageZeitSlotRueckreise
* uhrzeit
  - zeitInSlot
> backToMain

> check_rueckReiseGesetzt
  - utter_frageObRueckreise
* deny
> backToMain

> check_buchungBestaetigtGesetzt{"rueckreise": false}
  - utter_frageBuchungBestaetigtOhneRueckreise
> checkBuchungBestaetigt  

> check_buchungBestaetigtGesetzt{"rueckreise": true}
  - utter_frageBuchungBestaetigtMitRueckreise
> checkBuchungBestaetigt    
  
> checkBuchungBestaetigt
* affirm
  - utter_reiseBestaetigt

> checkBuchungBestaetigt
* deny
  - utter_reiseNichtBestaetigt
  
> beenden
* cancel
  - clearSlots
  
  
  
  