import matplotlib.pyplot as plt
import numpy as np
import random
from Jeu_regles import Deck, Card, Hand, hit, hit_or_stand, show_some, show_all, player_busts, player_wins, dealer_busts, dealer_wins, push
import Agent_Q_learning
from Agent_Q_learning import train_q_learning_agent

# Appeler l'entraînement avec suivi
agent, scores, final_hands = train_q_learning_agent(episodes=1000)

# Tracer les scores moyens
plt.figure()
plt.plot(range(len(scores)), scores, label="Score moyen par épisode", color='blue')
plt.xlabel("Épisodes")
plt.ylabel("Score")
plt.title("Progression des scores pendant l'apprentissage (Q-Learning)")
plt.legend()
plt.grid()
plt.show()

# Tracer les mains finales moyennes
plt.figure()
plt.plot(range(len(final_hands)), final_hands, label="Main moyenne à la fin de l'épisode", color='orange')
plt.axhline(y=21, color='r', linestyle='--', label="Score optimal (21)")
plt.xlabel("Épisodes")
plt.ylabel("Main finale moyenne")
plt.title("Progression des mains finales pendant l'apprentissage (Q-Learning)")
plt.legend()
plt.grid()
plt.show()

