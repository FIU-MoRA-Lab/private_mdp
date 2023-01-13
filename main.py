import math
import random
import statistics

from scipy.special import rel_entr, kl_div
from scipy.stats import entropy
from tabulate import tabulate

import Forward_Backward_Algiorithm_wikipedia as fb
import Viterbi_Algorithm_wikipedia as vt
import dijkstras as dk
import helpers as hlp
import hmm as hmm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import policy_iteration2 as river_world
import policy_iteration_original as russel_norvig_world


def run_russel_norvig_world():
    """Run calculation under russel and norvig world.

    """
    hlp.print_h1('compute optimal policy')
    T, p, u, r, gamma = russel_norvig_world.main_iterative()
    hlp.print_h1("a priori analysis")

    hlp.print_h2('enumerate all policies')
    start_state = 8
    states = [i for i in range(12)]
    actions = [i for i in range(4)]
    start_p = [0.0 for i in range(12)]
    start_p[start_state] = 1.0

    policies = hlp.enumerate_policies(states, actions, [5], [3, 7])
    print("first policy returned:")
    russel_norvig_world.print_policy(policies[0], (3, 4))
    print("last policy returned:")
    russel_norvig_world.print_policy(policies[-1], (3, 4))


def run_river_world():
    """Run calculation under our custom river world.

    """
    # river_world.main_iterative()
        # Define an MDP


def run_russel_norvig_world_optimal_policy_viterbi_path_only():
    """Run calculation under russel and norvig world.

    This version only analyzes the viterbi path to the end state using the optimal policy
    """
    hlp.print_h1('create markov decision process and compute optimal policy')
    T, p, u, r, gamma = russel_norvig_world.main_iterative()
    hlp.print_h2("a priori analysis")
    hlp.print_h2("MDP + Policy = Markov Chain")
    print("optimal policy: ")
    policy = [np.NaN if np.isnan(i) else int(i) for i in p]
    russel_norvig_world.print_policy(policy, (3, 4))
    print("markov chain:")
    markov_chain = hlp.to_markov_chain(policy, T, 12)
    markov_chain_df = pd.DataFrame(markov_chain)
    print(markov_chain_df.to_string())
    # set obstacles to loop
    markov_chain[5][5] = 1.0
    # set terminal state to loop
    markov_chain[3][3] = 1.0
    markov_chain[7][7] = 1.0
    # set start state
    state = [
        [0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0,
         1.0, 0.0, 0.0, 0.0]]
    state_history = [state[0]]
    for x in range(20):
        next_state = [[sum(a * b for a, b in zip(state_row, markov_chain_col))
                       for markov_chain_col in zip(*markov_chain)]
                      for state_row in state]
        state_history.append(next_state[0])
        state = next_state
    hlp.print_h2("stationary distribution")
    hlp.print_world(state, (3, 4))
    state_history_df = pd.DataFrame(state_history)
    # state_history_df.plot()
    # plt.show()
    hlp.print_h2("create hidden markov model with mdp and policy")
    # Viterbi needs 12x12 transition matrix
    # Generate the one induced by the policy
    trans_p = []
    for i in range(12):
        trans_p.append([0.0 for j in range(12)])
        if not np.isnan(p[i]) and not p[i] == -1:
            for j in range(12):
                trans_p[i][j] = T[i, j, int(p[i])]
    # emmission probabilities are induced by the policy
    emit_p = []
    for i in range(12):
        emit_p.append([0.0 for j in range(5)])
        # TODO - make nondeterministic policy possible
        if not np.isnan(p[i]):
            emit_p[i][int(p[i]) + 1] = 1.0


def main():
    hlp.print_h1('markov decision process policy leakage calculation program')
    while True:
        print("please select an option:")
        print("1) russel and norvig world")
        print("2) river world")
        print("3) russel and norvig world with optimal policy/viterbi path only")
        selection = input("enter your selection: ")

        if selection == "1":
            print("you selected option 1")
            run_russel_norvig_world()
            break
        elif selection == "2":
            print("your selected option 2")
            run_river_world()
            break
        elif selection == "3":
            print("you selected option 3")
            run_russel_norvig_world_optimal_policy_viterbi_path_only()()
            break
        else:
            print("Invalid selection. Please try again.\n")


if __name__ == "__main__":
    main()
