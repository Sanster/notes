import numpy as np
import torch

from crf import CRF
from utils import crf_train_loop

fair_dice = np.array([1 / 6] * 6)
loaded_dice = np.array([0.04, 0.04, 0.04, 0.04, 0.04, 0.8])

probabilities = {'fair': fair_dice,
                 'loaded': loaded_dice}

transition_mat = {'fair': np.array([0.6, 0.4, 0.0]),
                  'loaded': np.array([0.3, 0.7, 0.0]),
                  'start': np.array([0.5, 0.5, 0.0])}

states = ['fair', 'loaded', 'start']

state2ix = {'fair': 0,
            'loaded': 1,
            'start': 2}

log_likelihood = np.hstack([np.log(fair_dice).reshape(-1, 1),
                            np.log(loaded_dice).reshape(-1, 1)])


def simulate_data(n_timesteps):
    data = np.zeros(n_timesteps)
    prev_state = 'start'
    state_list = np.zeros(n_timesteps)
    for n in range(n_timesteps):
        next_state = np.random.choice(states, p=transition_mat[prev_state])
        state_list[n] = state2ix[next_state]
        next_data = np.random.choice([0, 1, 2, 3, 4, 5], p=probabilities[next_state])
        data[n] = next_data
        prev_state = next_state
    return data, state_list


if __name__ == "__main__":
    n_obs = 15
    rolls = np.zeros((5000, n_obs)).astype(int)
    targets = np.zeros((5000, n_obs)).astype(int)

    for i in range(5000):
        data, dices = simulate_data(n_obs)
        rolls[i] = data.reshape(1, -1).astype(int)
        targets[i] = dices.reshape(1, -1).astype(int)

    model = CRF(2, log_likelihood)
    model = crf_train_loop(model, rolls, targets, 1, 0.001)
    torch.save(model.state_dict(), "./checkpoint.hdf5")
