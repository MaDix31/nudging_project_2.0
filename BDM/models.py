from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import os
from operator import itemgetter
import itertools


author = 'Jörn Wieber'

doc = """
shows participants pictures of snacks and asks for their willingness-to-pay
"""


class Constants(BaseConstants):
    name_in_url = 'Step1'
    players_per_group = None

    # Anzahl unterschiedlicher Snack-Bilder, basierend auf Dateien im Snackbilder-Ordner
    num_snacks = len(os.listdir('_static//img_snacks'))

    # Liste der Snacks, basierend auf .jpg-Dateien im Snackbilder-Ordner
    list_snacks = []
    for snack in os.listdir('_static//img_snacks'):
        if snack.endswith('.JPG'):
            snack = snack[:-4]
            list_snacks.append(snack)
        else:
            continue
    # Bug-Fix 'in Live-Session werden nicht alle Snacks angezeigt':
    # da os.listdir u.U. "arbitrary" ordnet und Constants u.U. neu berechnet wird,
    # ist nicht gegeben, dass list_snacks immer gleich geordnet ist, daher:
    list_snacks.sort()

    # Anzahl an Entscheidungen, die in Step 1 gefällt werden sollen = Anzahl Snacks gesamt
    num_rounds = len(os.listdir('_static//img_snacks'))




class Subsession(BaseSubsession):
    def creating_session(self):


        if self.round_number == 1:          # damit Schleifen nur 1x durchlaufen werden

            # initialisiere Index-Liste
            # erstelle für jeden Teilnehmer eine Liste mit Indizes für die Snack-Liste
            # diese Liste wird zufällig geordnet -> individuelle Reihenfolge für jeden Teilnehmer
            for p in self.get_players():
                if 'num_snacks' not in p.participant.vars:
                    # Liste für Step 1
                    p.participant.vars['num_snacks'] = (list(range(Constants.num_snacks)))
                    random.shuffle(p.participant.vars['num_snacks'])
                if 'num_snacks_Step4' not in p.participant.vars:
                    # Liste für Step 4
                    p.participant.vars['num_snacks_Step4'] = (list(range(Constants.num_snacks)))
                    random.shuffle(p.participant.vars['num_snacks_Step4'])

                # für Auszahlung:
                if 'step2_decisions' not in p.participant.vars:
                    p.participant.vars['step2_decisions'] = []
                    p.participant.vars['step3_decisions'] = []


            # initialisiere BDM-Dictionary
            # erstellt ein zunächst leeres Dictionary, in das nach jeder Bewertung
            # über Player.fill_BDM_dict() ein key-value-Paar eingetragen wird
            # key: Snack
            # value: willingness-to-pay
            for p in self.get_players():
                if 'BDM' not in p.participant.vars:
                    p.participant.vars['BDM'] = {}
                if 'WTPs_step_4' not in p.participant.vars:
                    p.participant.vars['WTPs_step_4'] = {}

        # Weise einmalig Teilnehmer abwechselnd einem bestimmten Treatment zu
        if self.round_number == 1:
            treatments = itertools.cycle(['control', 'treatment_1', 'treatment_2'])
            for p in self.get_players():
                p.participant.vars['treatment'] = next(treatments)

        # Fülle in Datenfeld, welchem Treatment der Teilnehmer zugeordnet ist
        for p in self.get_players():
            p.treatment = p.participant.vars['treatment']


class Group(BaseGroup):
    pass



class Player(BasePlayer):
    def unfill_snack_list(self):
        ''' entferne erste Index-Zahl aus Teilnehmer-Snack-Liste
        '''
        self.participant.vars['num_snacks'].pop(0)


    def fill_BDM_dict(self):
        rated_snack = self.slider_value
        # key: abgefragter Snack
        # value: willingness-to-pay
        if self.slider_value == "":
            self.participant.vars['BDM'][Constants.list_snacks[self.participant.vars['num_snacks'][0]]] = '0'
        else:
            self.participant.vars['BDM'][Constants.list_snacks[self.participant.vars['num_snacks'][0]]] = self.slider_value


    def sort_WTPs(self):
        '''Differenzen der WTPs minimal halten
        '''
        # konvertiere BDM-dictionary in Liste von Tupel-Paaren: [(snack, WTP), (snack, WTP),...]
        sorted_BDM_tuples = sorted(self.participant.vars['BDM'].items(), key=itemgetter(1))
        # drehe Liste um, damit absteigend nach WTPs geordnet ist
        sorted_BDM_tuples.reverse()
        BDM_length = len(sorted_BDM_tuples)


        # initialisiere Liste mit den geringsten WTP-Differenzen (wird in nachfolgender Schleife gefüllt)
        closest_WTPs = []


        for index, element in enumerate(sorted_BDM_tuples):
        # ermittelt Differenz zwischen höchster WTP und allen anderen WTPs,
        # geht dann weiter zur zweit-höchsten WTP und ermittelt deren Differenz zu allen niedrigeren WTPs
        # usw.
            if index != BDM_length-1:       # wenn nicht letztes Element der Liste
                i = index + 1
                while i < BDM_length:
                    WTP_difference = round(float(element[1])-float(sorted_BDM_tuples[i][1]), 1)
                    # wenn closest_WTP-Liste noch nicht voll ODER die gerade ermittelte WTP-Differenz niedriger als das Maximum der bereits vorhandenen WTP-Differenzen
                    if len(closest_WTPs) < 400 or max(closest_WTPs, key=itemgetter(2))[2] > WTP_difference:
                        next_element = sorted_BDM_tuples[i][0]
                        i += 1
                        # füge Triple (Snack1, Snack2, WTP-Differenz zwischen Snack1 und Snack2) zu closest_WTP-Liste hinzu
                        closest_WTPs.append((element[0], next_element, WTP_difference))

                        # wenn closest_WTP-Liste voll: entferne größte WTP-Differenz
                        if len(closest_WTPs) > 400:
                            closest_WTPs.remove(max(closest_WTPs, key=itemgetter(2)))
                    else:
                        break


        # speichere closest_WTP-Liste global in Teilnehmer-Variablen
        self.participant.vars['closest_WTPs'] = closest_WTPs

        # Liste mit Snacks aus closest WTPs, um später davon die Pfade zu den Bildern zu bestimmen
        snacks_to_show = []
        # zufällige Reihenfolge, um dem überproportionalen Erscheinen eines bestimmten Guts entgegenzuwirken
        random.shuffle(closest_WTPs)
        for i in closest_WTPs:
            snacks_to_show.append(i[0])
            snacks_to_show.append(i[1])

        self.participant.vars["snacks_to_show"] = snacks_to_show


        # ordne Snacks neu (zufällig) für Step 3:
        snacks_to_show_3 = list(set(snacks_to_show))
        random.shuffle(snacks_to_show_3)
        while len(snacks_to_show_3) < len(snacks_to_show):
            random_snack = random.choice(snacks_to_show_3)
            if random_snack != snacks_to_show_3[-1]:
                snacks_to_show_3.append(random_snack)

        self.participant.vars["snacks_to_show_step3"] = snacks_to_show_3



    #### DATA-fields:
    # Kontrollfragen - dem Experimentator wird mit "HILFE" eine falsche Antwort signalisiert
    ''' auskommentiert: Kontrollfragen werden stattdessen händisch gemacht
    control_1 = models.StringField(verbose_name="Welche Ihrer Entscheidungen sind für Ihre Auszahlung relevant?",
    choices=[   ['HILFE', 'Jede Entscheidung zählt.'],
                ['HILFE', 'Eine der Entscheidungen in Stufe 1 wird zufällig zur Auszahlung ausgewählt.'],
                ['ok', 'Eine der Entscheidungen aus einer der vier Stufen des Experiments wird zufällig zur Auszahlung ausgewählt.']],
    widget=widgets.RadioSelect())
    control_2 = models.StringField(verbose_name="Wenn ich immer eine Zahlungsbereitschaft von 0 Euro angebe und Stufe 1 oder 4 zur Auszahlung ausgewählt wird, erhalte ich eine garantierte Auszahlung von 5 Euro.", choices=[['ok', 'korrekt'], ['HILFE', 'nicht korrekt']], widget=widgets.RadioSelect())
    control_3 = models.StringField(verbose_name="Wenn eine der Stufen 2 oder 3 zur Auszahlung ausgewählt wird, erhalte ich dennoch die garantierte Auszahlung von 5 Euro aus Stufe 1 oder 4.", choices=[['HILFE', 'korrekt'], ['ok', 'nicht korrekt']], widget=widgets.RadioSelect())
    control_4 = models.StringField(verbose_name="Ich erwerbe maximal ein Gut.", choices=[['ok', 'korrekt'], ['HILFE', 'nicht korrekt']], widget=widgets.RadioSelect())
    control_5 = models.StringField(verbose_name="Indem ich eine niedrigere Zahlungsbereitschaft angebe, kann ich einen niedrigeren Preis erhalten, als wenn ich meine wahre Zahlungsbereitschaft angeben würde.", choices=[['HILFE', 'korrekt'], ['ok', 'nicht korrekt']], widget=widgets.RadioSelect())
    control_6 = models.StringField(verbose_name="Indem ich eine niedrigere Zahlungsbereitschaft angebe, kann ich nicht beeinflussen, welchen Preis ich zahle wenn ich das Gut kaufe, da der Preis zufällig bestimmt wird. Ich zahle diesen zufällig gezogenen Preis nur, falls er nicht höher als meine Zahlungsbereitschaft ist.", choices=[['ok', 'korrekt'], ['HILFE', 'nicht korrekt']], widget=widgets.RadioSelect())
    control_7 = models.StringField(verbose_name="Indem ich eine niedrigere Zahlungsbereitschaft angebe, kann es passieren, dass der zufällig gezogene Preis oberhalb dieser angegebenen, aber unterhalb meiner tatsächlichen Zahlungsbereitschaft liegt. Ich würde dann das Gut nicht bekommen, obwohl ich es zu einem Preis hätte kaufen können, der unter meiner tatsächlichen Zahlungsbereitschaft liegt.", choices=[['ok', 'korrekt'], ['HILFE', 'nicht korrekt']], widget=widgets.RadioSelect())
    '''
    # Label des PCs
    p_label = models.StringField(widget=widgets.HiddenInput(), verbose_name='')
    # was der Teilnehmer mit dem Schieberegler wählt
    slider_value = models.StringField(widget=widgets.Slider())
    # welchen Snack der Teilnehmer gerade bewertet
    rated_snack = models.StringField(widget=widgets.HiddenInput(), verbose_name='')
