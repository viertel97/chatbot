from rasa_core.actions import Action
from rasa_core.events import SlotSet

from rasa_core.events import AllSlotsReset
import re


class preisBerechnen(Action):
   def name(self):
       return "preisBerechnen"

   def run(self, dispatcher, tracker, domain):

       numberpassengers = int(tracker.get_slot("numberPassengers"))
       rueckreise = tracker.get_slot("rueckreise")
       result = 0
       if rueckreise == "true":
           result = 1500 * numberpassengers * 2
       else:
           result = 1500 * numberpassengers
       result = str(result) + "€"
       return [SlotSet("preis", result if result is not None else [])]

class emailInSlot(Action):
    def name(self):
        return 'emailInSlot'

    def run(self, dispatcher, tracker, domain):
        email = next(tracker.get_latest_entity_values("email"), None)
        if email is None:
            email = next(tracker.get_latest_entity_values("ORG"), None)

        return [SlotSet("emailAdresse", email if email is not None else [])]


class yesno(Action):

    def name(self):
        return 'yesno'

    def run(self, dispatcher, tracker, domain):

        result = tracker.latest_message.intent["name"]
        if(tracker.get_slot("rueckreise") is None):
            if result == "affirm":
                dispatcher.utter_template('utter_frageRueckreiseDatum')
                return [SlotSet("rueckreise", "true")]

            elif result == "deny":
                dispatcher.utter_template('utter_fragePaymentType')
                return [SlotSet("rueckreise", "false")]
        else:
            if result == "affirm":
                dispatcher.utter_template('utter_reiseBestaetigt', emailAdresse=tracker.get_slot("emailAdresse"))

                return [SlotSet("buchungBestaetigt", "true")]

            elif result == "deny":
                dispatcher.utter_template('utter_reiseNichtBestaetigt')
                return [SlotSet("buchungBestaetigt", "false")]



class paymentInSlot(Action):
    def name(self):
        return 'paymentInSlot'

    def run(self, dispatcher, tracker, domain):
        if tracker.latest_message.intent["name"] == "zahlungstypen":
            dispatcher.utter_template('utter_frageEmailadresse')
            result = next(tracker.get_latest_entity_values("city"))
            if(next(tracker.get_latest_entity_values("city")) is None):
                result = next(tracker.get_latest_entity_values("paymentTypes"))
            return [SlotSet("paymentTypes", result)]

class ergebnisAusgeben(Action):
    def name(self):
        return 'ergebnisAusgeben'

    def run(self, dispatcher, tracker, domain):
        if tracker.get_slot("rueckreise") == "true":
            dispatcher.utter_template('utter_frageBuchungBestaetigtMitRueckreise', cityFrom=tracker.get_slot('cityFrom'), cityTo=tracker.get_slot('cityTo'),numberPassengers=tracker.get_slot('numberPassengers'),reiseDatumHinreise=tracker.get_slot('reiseDatumHinreise'),reiseUhrzeitHinreise=tracker.get_slot('reiseUhrzeitHinreise'),reiseDatumRueckreise=tracker.get_slot('reiseDatumRueckreise'),reiseUhrzeitRueckreise=tracker.get_slot('reiseUhrzeitRueckreise'), paymentTypes=tracker.get_slot('paymentTypes'), preis=tracker.get_slot('preis'), emailAdresse=tracker.get_slot('emailAdresse'))
        elif tracker.get_slot("rueckreise") == "false":
            dispatcher.utter_template('utter_frageBuchungBestaetigtOhneRueckreise', cityFrom=tracker.get_slot('cityFrom'), cityTo=tracker.get_slot('cityTo'),numberPassengers=tracker.get_slot('numberPassengers'),reiseDatumHinreise=tracker.get_slot('reiseDatumHinreise'),reiseUhrzeitHinreise=tracker.get_slot('reiseUhrzeitHinreise'), paymentTypes=tracker.get_slot('paymentTypes'), preis=tracker.get_slot('preis'), emailAdresse=tracker.get_slot('emailAdresse'))

class TicketsInSlot(Action):
    def name(self):
        return 'TicketsInSlot'

    def run(self, dispatcher, tracker, domain):

        numberpassengers = (tracker.get_slot("numberPassengers"))
        if (numberpassengers is None):
            numberpassengers = next(tracker.get_latest_entity_values("number"))

        if(not (type(numberpassengers) == int)):
            numberpassengers = [int(s) for s in numberpassengers.split() if s.isdigit()]
            numberpassengers = numberpassengers[0]

        if numberpassengers > 15:
            dispatcher.utter_message(
                "Die eingegebene Anzahl von " + str(numberpassengers) + " Tickets ist zu groß. Sie wurde auf 15 reduziert.")
            numberpassengers = 15
        elif numberpassengers < 0:
            dispatcher.utter_message(
                "Die eingegebene Anzahl von " + str(numberpassengers) + " Tickets ist zu niedrig. Sie wurde auf 1 erhöht.")
            numberpassengers = 1
        dispatcher.utter_template("utter_frageReiseDatum")
        return [SlotSet("numberPassengers", numberpassengers if numberpassengers is not None else [])]


class zeitInSlot(Action):
    def name(self):
        return 'zeitInSlot'

    def run(self, dispatcher, tracker, domain):
        result = next(tracker.get_latest_entity_values("time"), None)
        result = result.split("T")
        result = result[1]
        result = result.split("-")
        result = result[0]
        if tracker.get_slot("reiseUhrzeitHinreise") is None:
            dispatcher.utter_template("utter_frageObRueckreise")
            return [SlotSet("reiseUhrzeitHinreise", result)]
        elif tracker.get_slot("reiseUhrzeitRueckreise") is None and tracker.get_slot("reiseUhrzeitHinreise") is not None and tracker.get_slot("rueckreise") == "true":
            dispatcher.utter_template('utter_fragePaymentType')
            return [SlotSet("reiseUhrzeitRueckreise", result)]


class datumInSlot(Action):
    def name(self):
        return "datumInSlot"

    def run(self, dispatcher, tracker, domain):
        reiseDatumHinreise = tracker.get_slot("reiseDatumHinreise")
        reiseDatumRueckreise = tracker.get_slot("reiseDatumRueckreise")

        result = next(tracker.get_latest_entity_values("time"), None)
        result = result.split("T")
        result = result[0]


        if result is not None and reiseDatumHinreise is None:
            dispatcher.utter_template('utter_frageZeitSlot', reiseDatumHinreise=result)
            return [SlotSet("reiseDatumHinreise", result if result is not None else [])]

        elif result is not None and reiseDatumRueckreise is None and reiseDatumHinreise is not None:
            dispatcher.utter_template('utter_frageZeitSlotRueckreise', reiseDatumRueckreise=result)
            return [SlotSet("reiseDatumRueckreise", result if result is not None else [])]


class GPEoderCityInSlot(Action):
    def name(self):
        return "GPEoderCityInSlot"

    def run(self, dispatcher, tracker, domain):
        preposition = []
        prepositionStart = []
        city = []
        cityStart = []
        cityTo = None
        cityFrom = None
        time = []
        timeStart = []
        print(tracker.latest_message.entities)
        for x in tracker.latest_message.entities:
            if(x["entity"] == "preposition"):
                preposition.append(x["value"].strip())
                prepositionStart.append(x["start"])
            elif(x["entity"] == "city"):
                city.append(x["value"].strip())
                cityStart.append(x["start"])
            elif(x["entity"]=="time"):
                time.append(x["value"])
        print(time)

        if preposition[0] is not None and city[0] is not None:
            if preposition[0] == "von" or "aus" == preposition[1] and prepositionStart[0]<cityStart[0]:
                cityFrom = city[0]

            elif(preposition[0] == "nach" or "zu" and prepositionStart[0]<cityStart[0]):
                cityTo = city[0]

        if preposition[1] is not None and city[1] is not None:
            if preposition[1] == "von" or "aus" == preposition[1] and prepositionStart[1] < cityStart[1]:
                cityFrom = city[1]
            elif (preposition[1] == "nach" or "zu" and prepositionStart[1] < cityStart[1]):
                cityTo = city[1]
        try:
            cityFrom = cityFrom.title()
            cityTo = cityTo.title()
        except:
            print("blub")
        if cityTo is not None and cityFrom is not None:
            dispatcher.utter_message("Wie viele Tickets benötigst du von " + cityFrom + " nach " + cityTo+ "? (Zwischen 1 und 15)")
            ausgabe = [SlotSet("cityFrom", cityFrom), SlotSet("cityTo", cityTo)]
        elif(cityTo is None and cityFrom is not None):
            dispatcher.utter_template('utter_frageNachWo', cityFrom=cityFrom)
            ausgabe = [SlotSet("cityFrom", cityFrom)]
        elif(cityTo is not None and cityFrom is None):
            dispatcher.utter_template('utter_frageVonWo', cityTo=cityTo)
            ausgabe = [SlotSet("cityTo", cityTo)]

        if(time is not None):
            time = time[0].split("T")
            time = time[1]
            time = time.split("-")
            time = time[0]
            temp = time.split(":")
            temp = int(temp[0])
            print(time)
            ausgabe.append(SlotSet("reiseDatumHinreise"),time)

        return ausgabe