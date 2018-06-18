from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
import os
import operator
import itertools


author = 'Jörn Wieber'

doc = """
lets participant choose between 2 images the snack he/she prefers
"""


class Constants(BaseConstants):
    name_in_url = 'Step2'
    players_per_group = None
    num_rounds = 100
    list_snacks = []
    for snack in os.listdir('_static//img_snacks'):
        if snack.endswith('.JPG'):
            snack = snack[:-4]
            list_snacks.append(snack)
        else:
            continue
    # Bug-Fix, Erklärung siehe BDM-App:
    list_snacks.sort()

    default_ranking = open('_static//default_ranking.txt', 'r')
    healthy_list = []
    for line in default_ranking:
        healthy_list.append(line.rstrip('\n'))

    default_ranking.close()

class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            if 'decision_count' not in p.participant.vars:
                p.participant.vars['decision_count'] = 1


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def save_decision(self):
        self.participant.vars['step2_decisions'].append(self.decision)

    def delete_two_snacks(self):
        if len(self.participant.vars["snacks_to_show"]) >= 2:
            self.participant.vars["snacks_to_show"].pop(0)
            self.participant.vars["snacks_to_show"].pop(0)

    def count_decisions(self):
        self.participant.vars['decision_count'] += 1

    def reset_decision_count(self):
        self.participant.vars['decision_count'] = 1


    def set_healthier_as_default(self, snack1, snack2):
        # TO DO: exception falls snack nicht in Liste ist (sollte eigentlich nicht passieren)
        if Constants.healthy_list.index(snack1) < Constants.healthy_list.index(snack2):
            return 'checked="checked"'
        else:
            return ''



    #### DATA-fields
    # Kontrollfragen - dem Experimentator wird mit "HILFE" eine falsche Antwort signalisiert
    #control_4 = models.StringField(verbose_name="Kotrollfrage 4:", choices=[['ok', 'Ja'], ['HILFE', 'Nein']], widget=widgets.RadioSelect())
    #control_5 = models.StringField(verbose_name="Kotrollfrage 5:", choices=[['ok', 'Ja'], ['HILFE', 'Nein']], widget=widgets.RadioSelect())
    #control_6 = models.StringField(verbose_name="Kotrollfrage 6:", choices=[['ok', 'Ja'], ['HILFE', 'Nein']], widget=widgets.RadioSelect())
    # die zwei Snacks, zwischen denen sich der Teilnehmer entscheiden muss
    offer_1 = models.StringField(widget=widgets.HiddenInput(), verbose_name='')
    offer_2 = models.StringField(widget=widgets.HiddenInput(), verbose_name='')
    # der Snack, der als default gesetzt wurde
    default = models.StringField(widget=widgets.HiddenInput(), verbose_name='')
    # der Snack, für den sich der Teilnehmer entscheidet
    decision = models.StringField()
    # Treatment-Gruppe des Teilnehmers
    treatment = models.StringField(widget=widgets.HiddenInput(), verbose_name='')
