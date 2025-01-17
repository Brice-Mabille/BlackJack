import random
import Jeu_regles
from Jeu_regles import Deck, Card, Hand, hit, hit_or_stand, show_some, show_all, player_busts, player_wins, dealer_busts, dealer_wins, push

class SarsaAgent:
    ALPHA = 0.1 
    GAMMA = 0.9
    EPSILON = 1.0
    EPSILON_DECAY = 0.995
    EPSILON_MIN = 0.1
    
    ACTIONS = ['h', 's']  # 'h' : Hit, 's' : Stand
    def __init__(self):
        # Q-table : Dictionnaire de valeurs Q pour chaque état-action
        self.q_table = {}

    def get_state(self, hand_value, has_ace, dealer_card):
        """
        Représente l'état comme un tuple : (somme des cartes, as utilisable, carte visible du dealer)
        """
        return (hand_value, has_ace, dealer_card)

    def sarsa_choose_action(self, state):
        """Choisit une action (hit ou stand) en utilisant une stratégie epsilon-greedy."""
        if state not in self.q_table:
            self.q_table[state] = {'h': 0.0, 's': 0.0}  # Initialise les valeurs Q pour ce nouvel état

        if random.random() < SarsaAgent.EPSILON :
            return random.choice(['h', 's'])  # Exploration
        else:
            return max(self.q_table[state], key=self.q_table[state].get)  # Exploitation

    def update(self, state, action, reward, next_state, next_action):
        """
        Met à jour la valeur Q en utilisant la formule de Q-Learning
        """
        if next_state is None or next_action is None:  # Cas terminal
            next_q = 0  # Aucune récompense future à considérer
        else:        
            if next_state not in self.q_table:
                self.q_table[next_state] = {'h': 0.0, 's': 0.0}  # Initialiser les valeurs Q pour l'état suivant inconnu
            next_q = self.q_table[next_state][next_action]

        #action_idx = SarsaAgent.ACTIONS.index(action)
        #next_action_idx = SarsaAgent.ACTIONS.index(next_action)
        
        current_q = self.q_table[state][action]
        

        # Mise à jour de la valeur Q
        self.q_table[state][action] = current_q + SarsaAgent.ALPHA * (reward + SarsaAgent.GAMMA * next_q - current_q)

def train_sarsa_agent(episodes=10000):
    agent = SarsaAgent()

    for episode in range(episodes):
        deck = Deck()
        deck.shuffle()

        # Initialisation de la main du joueur et du dealer
        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Initialiser l'état et choisir la première action
        state = agent.get_state(player_hand.value, player_hand.aces > 0, Card.values[dealer_hand.cards[0].rank])
        action = agent.sarsa_choose_action(state)

        while True:
            # Effectuer l'action
            if action == 'h':  # Hit
                hit(deck, player_hand)
                if player_hand.value > 21:  # Busted
                    reward = -1
                    next_state = None
                    next_action = None
                else:
                    next_state = agent.get_state(player_hand.value, player_hand.aces > 0, Card.values[dealer_hand.cards[0].rank])
                    next_action = agent.sarsa_choose_action(next_state)
                    reward = 0
            else:  # Stand
                while dealer_hand.value < 17:
                    hit(deck, dealer_hand)

                # Résultat du jeu
                if dealer_hand.value > 21 or player_hand.value > dealer_hand.value:
                    reward = 1
                elif player_hand.value < dealer_hand.value:
                    reward = -1
                else:
                    reward = 0

                next_state = None
                next_action = None

            # Mettre à jour les valeurs Q
            agent.update(state, action, reward, next_state, next_action)

            # Passer à l'état suivant
            state = next_state
            action = next_action

            if state is None:  # Fin de l'épisode
                break

        # Réduction de l'exploration
        SarsaAgent.EPSILON = max(SarsaAgent.EPSILON * SarsaAgent.EPSILON_DECAY, SarsaAgent.EPSILON_MIN)
        print(f"Episode {episode + 1}/{episodes} completed. Récompense : {reward}")

    return agent

