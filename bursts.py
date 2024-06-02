import numpy as np

# Ορισμός των καταστάσεων και των ρυθμών τους (λ)
states = [0.5, 1.0, 1.5]
transition_cost = 1  # Κόστος μετάβασης σε κατάσταση υψηλότερης δραστηριότητας
time_stamps = [1, 2.5, 4, 6]

# Συνάρτηση κόστους για εκθετική κατανομή
def exponential_cost(lambda_i, x):
    return -np.log(lambda_i * np.exp(-lambda_i * x))

# Δυναμικός προγραμματισμός για εύρεση της ακολουθίας καταστάσεων με το ελάχιστο κόστος
def find_optimal_sequence(states, time_stamps, transition_cost):
    n_states = len(states)
    n_times = len(time_stamps)
    
    # Πίνακας κόστους
    cost_matrix = np.zeros((n_states, n_times))
    # Πίνακας προηγούμενων καταστάσεων για ανακατασκευή της βέλτιστης ακολουθίας
    prev_state = np.zeros((n_states, n_times), dtype=int)
    
    # Υπολογισμός αρχικών κόστους για την πρώτη χρονική στιγμή
    for i in range(n_states):
        cost_matrix[i, 0] = exponential_cost(states[i], time_stamps[0])
    
    # Υπολογισμός κόστους για τις υπόλοιπες χρονικές στιγμές
    for t in range(1, n_times):
        for i in range(n_states):
            min_cost = float('inf')
            for j in range(n_states):
                transition_c = transition_cost if j > i else 0
                total_cost = cost_matrix[j, t-1] + exponential_cost(states[i], time_stamps[t] - time_stamps[t-1]) + transition_c
                if total_cost < min_cost:
                    min_cost = total_cost
                    prev_state[i, t] = j
            cost_matrix[i, t] = min_cost
    
    # Εύρεση της κατάστασης με το ελάχιστο κόστος στην τελευταία χρονική στιγμή
    min_final_cost = float('inf')
    final_state = 0
    for i in range(n_states):
        if cost_matrix[i, -1] < min_final_cost:
            min_final_cost = cost_matrix[i, -1]
            final_state = i
    
    # Ανακατασκευή της βέλτιστης ακολουθίας καταστάσεων
    optimal_sequence = [final_state]
    for t in range(n_times-1, 0, -1):
        optimal_sequence.insert(0, prev_state[optimal_sequence[0], t])
    
    return optimal_sequence, min_final_cost

# Εκτέλεση του προγράμματος
optimal_sequence, min_final_cost = find_optimal_sequence(states, time_stamps, transition_cost)
print("Βέλτιστη ακολουθία καταστάσεων:", optimal_sequence)
print("Ελάχιστο συνολικό κόστος:", min_final_cost)
s