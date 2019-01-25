from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import os

author = 'Marius Dietsch'

doc = """
This app is for displaying all BDM instruction PDFs"""


class Constants(BaseConstants):
    name_in_url = 'Intro'
    players_per_group = None
    num_instructions =  len(os.listdir('_static//Instructions'))
    num_rounds = num_instructions

class Subsession(BaseSubsession):
    def creating_session(self):
        print('in creating_session', self.round_number)
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
