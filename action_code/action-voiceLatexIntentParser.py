#!/usr/bin/env python2
# example: https://github.com/yxdunc/snips-workshop/blob/master/action-times-tables.py
from hermes_python.hermes import Hermes

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

INTENT_INTEGRAL = "integral"
INTENT_DERIVATE = "derivate"
INTENT_CREATE_MATRIX = "create_matrix"
INTENT_DICTATE_MATRIX = "dictate_matrix"


def user_give_integral(hermes, intent_message):

    fun = intent_message.slots.function[0].raw_value
    lower_bound = intent_message.slots.lower_bound.first().value
    upper_bound = intent_message.slots.uppter_bound.first().value

    tts = "Integrate %s from %d to %d" % (fun, lower_bound, upper_bound)

    hermes.publish_end_session(intent_message.session_id, tts)


with Hermes(MQTT_ADDR) as h:
    h.subscribe_intent(INTENT_INTEGRAL, user_give_integral).start()


        # .subscribe_intent(INTENT_DERIVATE, user_does_not_know) \
        # .subscribe_intent(INTENT_CREATE_MATRIX, user_gives_answer) \
        # .subscribe_intent(INTENT_DICTATE_MATRIX, user_gives_answer) \
        # .start()

