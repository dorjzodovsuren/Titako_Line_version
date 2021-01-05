import os
import aiml
import time
session_id = 1

# Create the kernel and learn AIML files
kernel = aiml.Kernel()
sessionData = kernel.getSessionData(session_id)

kernel.setPredicate("name", "Dorjzodovsuren", session_id)
clients_dogs_name = kernel.getPredicate("name", session_id)

kernel.setBotPredicate("name", "Titako")
bot_hometown = kernel.getBotPredicate("name")

kernel.bootstrap(brainFile = "./model/rule_based/bot_brain.brn")

def get_rulebased_answer(question_en):
    answer_en = kernel.respond(question_en, session_id)
    return answer_en