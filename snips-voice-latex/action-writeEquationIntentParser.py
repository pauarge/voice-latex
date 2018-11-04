#!/usr/bin/env python2
from hermes_python.hermes import Hermes

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

INTENT_INTEGRAL = "bezzam:integral"
INTENT_CREATE_MATRIX = "bezzam:create_matrix"


def user_give_integral(hermes, intent_message):
    sentence = "Hello, you asked for an integral."
    hermes.publish_end_session(intent_message.session_id, sentence)


def user_create_matrix(hermes, intent_message):

    first_dim = intent_message.slots.first_dim.first().value.value
    second_dim = intent_message.slots.second_dim.first().value.value

    tts = "Hello you asked to create a {} by {} matrix.".format(first_dim, second_dim)

    hermes.publish_end_session(intent_message.session_id, tts)


def intent_received(hermes, intent_message):
    sentence = "Hello "

    if intent_message.intent.intent_name == INTENT_INTEGRAL:
        sentence += 'you asked for an integral'
    elif intent_message.intent.intent_name == INTENT_CREATE_MATRIX:
        sentence += 'you asked to create a matrix'

    hermes.publish_end_session(intent_message.session_id, sentence)

# if __name__ == "__main__":
with Hermes(MQTT_ADDR) as h:
    # h.subscribe_intents(intent_received).start()
    # h.subscribe_intent(INTENT_INTEGRAL, user_give_integral).start()
    h.subscribe_intent(INTENT_CREATE_MATRIX, user_create_matrix).start()
