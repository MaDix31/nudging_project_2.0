from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        # im Folgenden wird der zufällige Snack ausgewählt
        if self.round_number == 1:

            # Zufalls-Stufe, von der ausgewählt wird
            self.participant.vars['step'] = random.choice([1,2,3,4])

            if self.participant.vars['step'] in [1, 4]:
                # zufälliger Snack, der am Ende ausbezahlt werden könnte
                self.participant.vars['random_snack'] = random.choice(Constants.list_snacks)
                self.participant.vars['random_snack2'] = random.choice(Constants.list_snacks)
                self.participant.vars['random_snack3'] = random.choice(Constants.list_snacks)
                self.participant.vars['random_snack4'] = random.choice(Constants.list_snacks)
                self.participant.vars['random_snack5'] = random.choice(Constants.list_snacks)

            if self.participant.vars['step'] == 2:
                # zufälliger Snack, der am Ende ausbezahlt wird
                self.participant.vars['random_snack'] = random.choice(self.participant.vars['step2_decisions'])
                self.participant.vars['random_snack2'] = random.choice(self.participant.vars['step2_decisions'])
                self.participant.vars['random_snack3'] = random.choice(self.participant.vars['step2_decisions'])
                self.participant.vars['random_snack4'] = random.choice(self.participant.vars['step2_decisions'])
                self.participant.vars['random_snack5'] = random.choice(self.participant.vars['step2_decisions'])

            if self.participant.vars['step'] == 3:
                # zufälliger Snack, der am Ende ausbezahlt wird
                self.participant.vars['random_snack'] = random.choice(self.participant.vars['step3_decisions'])
                self.participant.vars['random_snack2'] = random.choice(self.participant.vars['step3_decisions'])
                self.participant.vars['random_snack3'] = random.choice(self.participant.vars['step3_decisions'])
                self.participant.vars['random_snack4'] = random.choice(self.participant.vars['step3_decisions'])
                self.participant.vars['random_snack5'] = random.choice(self.participant.vars['step3_decisions'])

            # Preis für den zufälligen Snack
            self.participant.vars['random_price'] = random.randrange(0, 50)/10


class BDM2(Page):
    def vars_for_template(self):
        return {
            'image_path': 'img_snacks/' + str(Constants.list_snacks[self.participant.vars['num_snacks_Step4'][0]]) + '.JPG',
            'snack'     : str(Constants.list_snacks[self.participant.vars['num_snacks_Step4'][0]]),
            'left'      : len(Constants.list_snacks)-len(self.participant.vars['num_snacks_Step4'])
        }

    def before_next_page(self):
        self.player.fill_BDM_dict()
        self.player.unfill_snack_list()

    form_model = 'player'
    form_fields = ['slider_value', 'rated_snack']


class Lastpage(Page):
    def is_displayed(self):
        # zeige End-Seite nur nach der letzten Runde an
        return self.round_number == Constants.num_rounds


    def vars_for_template(self):
        # PAYOFF LOGIK
        # bestimme Stufe, die für den Payoff genommen wird
        step_payoff = self.participant.vars['step']
        minimumwage = 10
        random_snack = self.participant.vars['random_snack']
        random_snack2 = self.participant.vars['random_snack2']
        random_snack3 = self.participant.vars['random_snack3']
        random_snack4 = self.participant.vars['random_snack4']
        random_snack5 = self.participant.vars['random_snack5']

        if step_payoff == 1 or step_payoff == 4:
            payoff_with_snack = minimumwage + 5 - float(self.participant.vars['random_price'])
            payoff_without_snack = minimumwage + 5
            if step_payoff == 1:
                # this is to avoid a non-repeatable key error that occured in a pilot session
                try:
                    participant_WTP = float(self.participant.vars['BDM'][self.participant.vars['random_snack']])
                except KeyError:
                    print("########### A KeyError has occured for snack1 Step 1!")
                    participant_WTP = 0
                try:
                    participant_WTP2 = float(self.participant.vars['BDM'][self.participant.vars['random_snack2']])
                except KeyError:
                    print("########### A KeyError has occured for snack2 Step 1!")
                    participant_WTP2 = 0
                try:
                    participant_WTP3 = float(self.participant.vars['BDM'][self.participant.vars['random_snack3']])
                except KeyError:
                    print("########### A KeyError has occured for snack3 Step 1!")
                    participant_WTP3 = 0
                try:
                    participant_WTP4 = float(self.participant.vars['BDM'][self.participant.vars['random_snack4']])
                except KeyError:
                    print("########### A KeyError has occured for snack4 Step 1!")
                    participant_WTP4 = 0
                try:
                    participant_WTP5 = float(self.participant.vars['BDM'][self.participant.vars['random_snack5']])
                except KeyError:
                    print("########### A KeyError has occured for snack5 Step 1!")
                    participant_WTP5 = 0
            if step_payoff == 4:
                # this is to avoid a non-repeatable key error in a pilot session
                try:
                    participant_WTP = float(self.participant.vars['WTPs_step_4'][self.participant.vars['random_snack']])
                except KeyError:
                    print("########### A KeyError has occured for snack1 Step 4!")
                    participant_WTP = 0
                try:
                    participant_WTP2 = float(self.participant.vars['WTPs_step_4'][self.participant.vars['random_snack2']])
                except KeyError:
                    print("########### A KeyError has occured for snack2 Step 4!")
                    participant_WTP2 = 0
                try:
                    participant_WTP3 = float(self.participant.vars['WTPs_step_4'][self.participant.vars['random_snack3']])
                except KeyError:
                    print("########### A KeyError has occured for snack3 Step 4!")
                    participant_WTP3 = 0
                try:
                    participant_WTP4 = float(self.participant.vars['WTPs_step_4'][self.participant.vars['random_snack4']])
                except KeyError:
                    print("########### A KeyError has occured for snack4 Step 4!")
                    participant_WTP4 = 0
                try:
                    participant_WTP5 = float(self.participant.vars['WTPs_step_4'][self.participant.vars['random_snack5']])
                except KeyError:
                    print("########### A KeyError has occured for snack5 Step 4!")
                    participant_WTP5 = 0


        if step_payoff == 2 or step_payoff == 3:
            payoff_with_snack = minimumwage
            payoff_without_snack = minimumwage
            participant_WTP = "-"
            participant_WTP2 = "-"
            participant_WTP3 = "-"
            participant_WTP4 = "-"
            participant_WTP5 = "-"


        return {
            'p_label'           : self.participant.label,
            'step'              : step_payoff,
            'random_snack'      : random_snack,
            'random_snack2'     : random_snack2,
            'random_snack3'     : random_snack3,
            'random_snack4'     : random_snack4,
            'random_snack5'     : random_snack5,
            'random_price'      : float(self.participant.vars['random_price']),
            'participant_WTP'   : participant_WTP,
            'participant_WTP2'  : participant_WTP2,
            'participant_WTP3'  : participant_WTP3,
            'participant_WTP4'  : participant_WTP4,
            'participant_WTP5'  : participant_WTP5,
            'payoff_with_snack' : payoff_with_snack,
            'payoff_without_snack': payoff_without_snack
        }

    form_model = 'player'
    form_fields = [ 'rand_snack', 'rand_price', 'p_label', 'payout1', 'payout2', 'payout3',
                    'payout4', 'payout5', 'payout6', 'payout7', 'payout8', 'payout9', 'payout10']



page_sequence = [
    Instructions,
    BDM2,
    Lastpage
]
