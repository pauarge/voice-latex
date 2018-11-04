#!/usr/bin/env python2
from hermes_python.hermes import Hermes
import requests
import json

IP = "http://10.70.10.146:5000"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

# function intents
INTENT_INTEGRATE = "bezzam:integrate_function"
INTENT_DERIVATE = "bezzam:derivate_function"
INTENT_POLY = "bezzam:write_polynomial"
INTENT_POLY_COEF = "bezzam:polynomial_coefficients"
INTENT_TRIG = "bezzam:write_trig_function"
INTENT_FINISH = "bezzam:finish_function"

# matrix intents
INTENT_CREATE_MATRIX = "bezzam:create_matrix"
INTENT_DICTATE_MATRIX = "bezzam:dictate_matrix"
INTENT_RANDOM_MATRIX = "bezzam:random_matrix"
INTENT_MATRIX_MULT = "bezzam:matrix_mult"
INTENT_MATRIX_FINISH = "bezzam:finish_matrix"
INTENT_MATRIX_INVERSE = "bezzam:matrix_inverse"

STOP_INTENT = "bezzam:stop_intent"

# intent filters for interactive dialogues
INTENT_FILTER_ENTRIES = [INTENT_DICTATE_MATRIX, INTENT_RANDOM_MATRIX, STOP_INTENT]
INTENT_FILTER_MATRIX_OP = [INTENT_MATRIX_MULT, INTENT_MATRIX_INVERSE, INTENT_MATRIX_FINISH, STOP_INTENT]
INTENT_FILTER_POLY = [INTENT_POLY_COEF, STOP_INTENT]
INTENT_FILTER_OPERATION = [INTENT_INTEGRATE, INTENT_DERIVATE, INTENT_FINISH, STOP_INTENT]

entries = dict()
poly = dict()


def user_write_poly(hermes, intent_message):
    session_id = intent_message.session_id
    order = int(intent_message.slots.order.first().value)
    poly[session_id] = {"order": order,
                        "left": order+1,
                        "coef": [],
                        "operation": None,
                        "intent": {"intentName": "user:polynomial"}}
    # tts = "You asked to create a polynomial of order {}. Please tell me {} coefficients.".format(order, order+1)
    tts = "Please tell me {} coefficients.".format(order + 1)
    hermes.publish_continue_session(session_id, tts, INTENT_FILTER_POLY)


def user_poly_coef(hermes, intent_message):
    session_id = intent_message.session_id
    slot_list = intent_message.slots.coef.all()
    n_given_entries = len(slot_list)
    if n_given_entries < poly[session_id]["left"]:

        tts = "I only understood {} entries. Could you please give me {} more?".format(n_given_entries,
                                                                                       poly[session_id]["left"] - n_given_entries)
        # store status in dict
        poly[session_id]["left"] = poly[session_id]["left"] - n_given_entries
        poly[session_id]["coef"] = poly[session_id]["coef"] + [int(slot.value) for slot in slot_list]

        # continue interaction
        hermes.publish_continue_session(session_id, tts, INTENT_FILTER_POLY)

    elif n_given_entries > poly[session_id]["left"]:

        tts = "I understood more coefficients than needed. I will use the first {}.".format(poly[session_id]["order"])

        poly[session_id]["coef"] = poly[session_id]["coef"] + [int(slot.value) for slot in slot_list]
        poly[session_id]["coef"] = poly[session_id]["coef"][:poly[session_id]["order"]+1]

        tts = tts + "I understood the following coefficients: " + ', '.join(str(x) for x in poly[session_id]["coef"])
        tts += ". Would you like to operate on this function?"
        tts = "Would you like to operate on this function?"
        hermes.publish_continue_session(session_id, tts, INTENT_FILTER_OPERATION)

    else:

        poly[session_id]["coef"] = poly[session_id]["coef"] + [int(slot.value) for slot in slot_list]
        tts = "Thank you. I understood the following coefficients: " + ', '.join(str(x) for x in poly[session_id]["coef"])
        tts += ". Would you like to operate on this function?"
        tts = "Would you like to operate on this function?"
        hermes.publish_continue_session(session_id, tts, INTENT_FILTER_OPERATION)


def integrate_function(hermes, intent_message):
    session_id = intent_message.session_id
    poly[session_id]["operation"] = "integral"

    # add lower and upper bound to payload
    # lower_bound = int(intent_message.slots.lower_bound.first().value)
    # upper_bound = int(intent_message.slots.upper_bound.first().value)
    # lower_bound = None if intent_message.slots.lower_bound is None else intent_message.slots.lower_bound.first().value
    # upper_bound = None if intent_message.slots.upper_bound is None else intent_message.slots.upper_bound.first().value
    # poly[session_id]["lower_bound"] = lower_bound
    # poly[session_id]["upper_bound"] = upper_bound

    poly[session_id]["lower_bound"] = None if not intent_message.slots.lower_bound else int(intent_message.slots.lower_bound.first().value)
    poly[session_id]["upper_bound"] = None if not intent_message.slots.upper_bound else int(intent_message.slots.upper_bound.first().value)

    tts = "OK, writing the integral of this function."

    # send to browser
    try:
        r = requests.post(IP, json=poly[session_id])
    except:
        pass
    del poly[session_id]
    hermes.publish_end_session(session_id, tts)


def derivate_function(hermes, intent_message):
    session_id = intent_message.session_id
    poly[session_id]["operation"] = "derivate"

    # add wrt if available
    wrt = 'x' if intent_message.slots.wrt is None else intent_message.slots.wrt.first().value
    poly[session_id]["wrt"] = wrt

    # tts = "OK, writing the derivative of this function with respect to {}.".format(wrt)
    tts = "OK, writing the derivative of this function."

    # send to browser
    try:
        r = requests.post(IP, json=poly[session_id])
    except:
        pass
    del poly[session_id]
    hermes.publish_end_session(session_id, tts)


def create_trig_function(hermes, intent_message):
    session_id = intent_message.session_id

    trigfunc = intent_message.slots.trigfunc.first().value
    var = intent_message.slots.variable.first().value
    auxoper = None if intent_message.slots.auxillaryoperation is None else intent_message.slots.auxillaryoperation.first().value

    poly[session_id] = {"trigfunc": trigfunc,
                        "var": var,
                        "auxoper": auxoper,
                        "operation": None,
                        "intent": {"intentName": "user:trigfunc"}}

    tts = "Would you like to perform an operation on the trig function?"
    hermes.publish_continue_session(session_id, tts, INTENT_FILTER_OPERATION)


def finish_function(hermes, intent_message):
    session_id = intent_message.session_id
    tts = "OK, creating function."

    # send to browser
    try:
        r = requests.post(IP, json=poly[session_id])
    except:
        pass
    del poly[session_id]
    hermes.publish_end_session(session_id, tts)


def user_create_matrix(hermes, intent_message):

    session_id = intent_message.session_id

    first_dim = int(intent_message.slots.first_dim.first().value)
    second_dim = int(intent_message.slots.second_dim.first().value)
    entries[session_id] = {"tot": first_dim * second_dim,
                           "left": first_dim * second_dim,
                           "first_dim": first_dim,
                           "second_dim": second_dim,
                           "operation": None,
                           "vals": [],
                           "intent": {"intentName": "user:matrix"}}

    # tts = "You asked to create a {} by {} matrix. Please tell me the entries.".format(first_dim, second_dim)
    tts = "Please tell me the entries.".format(first_dim, second_dim)
    hermes.publish_continue_session(session_id, tts, INTENT_FILTER_ENTRIES)


def user_random_matrix(hermes, intent_message):
    session_id = intent_message.session_id

    entries[session_id]["intent"]["intentName"] = "user:random-matrix"
    tts = "Creating a random {} by {} matrix.".format(entries[session_id]["first_dim"],
                                                      entries[session_id]["second_dim"])

    tts += " Would you like to operate on this matrix?"
    hermes.publish_continue_session(session_id, tts, INTENT_FILTER_MATRIX_OP)

    # # send to browser
    # r = requests.post(IP, json=entries[session_id])
    # del entries[session_id]
    # hermes.publish_end_session(session_id, tts)


def user_dictate_matrix(hermes, intent_message):

    session_id = intent_message.session_id

    slot_list = intent_message.slots.entry.all()
    n_given_entries = len(slot_list)

    if n_given_entries < entries[session_id]["left"]:
        tts = "I only understood {} entries. Could you please give me {} more?".format(n_given_entries,
                                                                                   entries[session_id]["left"]-n_given_entries)
        # store status in dicts
        entries[session_id]["left"] = entries[session_id]["left"] - n_given_entries
        entries[session_id]["vals"] = entries[session_id]["vals"] + [int(slot.value) for slot in slot_list]

        # continue interaction
        hermes.publish_continue_session(session_id, tts, INTENT_FILTER_ENTRIES)

    elif n_given_entries > entries[session_id]["left"]:
        tts = "I understood more entries than needed. I will use the first {}.".format(entries[session_id]["tot"])

        entries[session_id]["vals"] = entries[session_id]["vals"] + [int(slot.value) for slot in slot_list]
        entries[session_id]["vals"] = entries[session_id]["vals"][:entries[session_id]["tot"]]

        tts += " Would you like to operate on this matrix?"
        hermes.publish_continue_session(session_id, tts, INTENT_FILTER_MATRIX_OP)


        # tts = tts + "I understood the following entries: " + ', '.join(str(x) for x in entries[session_id]["vals"])
        #
        # # send to browser
        # r = requests.post(IP, json=entries[session_id])
        # del entries[session_id]
        # hermes.publish_end_session(session_id, tts)

    else:

        entries[session_id]["vals"] = entries[session_id]["vals"] + [int(slot.value) for slot in slot_list]

        tts = "Thank you. Would you like to operate on this matrix?"
        hermes.publish_continue_session(session_id, tts, INTENT_FILTER_MATRIX_OP)

        # tts = "Thank you. I understood the following entries: " + ', '.join(str(x) for x in entries[session_id]["vals"])
        #
        # # send to browser
        # r = requests.post(IP, json=entries[session_id])
        # del entries[session_id]
        # hermes.publish_end_session(session_id, tts)


def matrix_mult(hermes, intent_message):
    session_id = intent_message.session_id
    third_dim = int(intent_message.slots.second_dim.first().value)

    entries[session_id]["operation"] = "matrix_mult"
    entries[session_id]["third_dim"] = third_dim

    tts = "Writing matrix multiplication."

    # send to browser
    r = requests.post(IP, json=entries[session_id])
    del entries[session_id]
    hermes.publish_end_session(session_id, tts)


def matrix_inverse(hermes, intent_message):
    session_id = intent_message.session_id
    entries[session_id]["operation"] = "matrix_inverse"
    tts = "Writing matrix inverse."

    # send to browser
    r = requests.post(IP, json=entries[session_id])
    del entries[session_id]
    hermes.publish_end_session(session_id, tts)


def matrix_finish(hermes, intent_message):
    session_id = intent_message.session_id
    tts = "Writing matrix."

    # send to browser
    r = requests.post(IP, json=entries[session_id])
    del entries[session_id]
    hermes.publish_end_session(session_id, tts)


def user_stop(hermes, intent_message):
    session_id = intent_message.session_id

    try:
        del entries[session_id]
    except:
        pass

    try:
        del poly[session_id]
    except:
        pass

    hermes.publish_end_session(session_id, "Ending session.")


# if __name__ == "__main__":
with Hermes(MQTT_ADDR) as h:
    h.subscribe_intent(INTENT_CREATE_MATRIX, user_create_matrix) \
     .subscribe_intent(INTENT_RANDOM_MATRIX, user_random_matrix) \
     .subscribe_intent(INTENT_POLY, user_write_poly) \
     .subscribe_intent(INTENT_POLY_COEF, user_poly_coef) \
     .subscribe_intent(INTENT_INTEGRATE, integrate_function) \
     .subscribe_intent(INTENT_DERIVATE, derivate_function) \
     .subscribe_intent(INTENT_FINISH, finish_function) \
     .subscribe_intent(INTENT_TRIG, create_trig_function) \
     .subscribe_intent(INTENT_MATRIX_MULT, matrix_mult) \
     .subscribe_intent(INTENT_MATRIX_FINISH, matrix_finish) \
     .subscribe_intent(INTENT_MATRIX_INVERSE, matrix_inverse) \
     .subscribe_intent(STOP_INTENT, user_stop) \
     .subscribe_intent(INTENT_DICTATE_MATRIX, user_dictate_matrix).start()
