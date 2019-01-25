from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Intro(Page):
    def is_displayed(self):
        # zeige Instruktionen nur zu  Beginn an
        return self.round_number == 1


class BDM_instructions(Page):
    def vars_for_template(self):
        # instructions_path: Pfad zur Instructions Page, der auf dieser Seite angezeit wird
        return {
            'instructions_path': 'Instructions/Slide' + str(self.round_number) + '.JPG'
        }

page_sequence = [
    Intro,
    BDM_instructions
]
