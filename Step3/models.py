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
lets participant again choose between 2 images the snack he/she prefers (without default)
"""


class Constants(BaseConstants):
    name_in_url = 'Step3'
    players_per_group = None
    # TO DO: Ändern in tatsächliche Anzahl an Vergleichsrunden
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

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def save_decision(self):
        self.participant.vars['step3_decisions'].append(self.decision)

    def delete_two_snacks(self):
        if len(self.participant.vars["snacks_to_show_step3"]) >= 2:
            self.participant.vars["snacks_to_show_step3"].pop(0)
            self.participant.vars["snacks_to_show_step3"].pop(0)

    def count_decisions(self):
        self.participant.vars['decision_count'] += 1


    #### DATA-fields
    # die zwei Snacks, zwischen denen sich der Teilnehmer entscheiden muss
    offer_1 = models.StringField(widget=widgets.HiddenInput(), verbose_name='')
    offer_2 = models.StringField(widget=widgets.HiddenInput(), verbose_name='')
    # der Snack, für den sich der Teilnehmer entscheidet
    decision = models.StringField()
    # Treatment-Gruppe des Teilnehmers
    treatment = models.StringField()
