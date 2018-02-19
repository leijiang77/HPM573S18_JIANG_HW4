from enum import Enum
import numpy as np

class flipresult(Enum):
    """ health status of patients  """
    HEAD = 1
    TAIL = 0

class Game(object):
    def __init__(self, id, winprob):
        """ initiates a patient
        :param id: ID of the patient
        :param mortality_prob: probability of death during a time-step (must be in [0,1])
        """
        self._id = id
        self._rnd = np.random       # random number generator for this patient
        self._rnd.seed(self._id)    # specifying the seed of random number generator for this patient

        self._winprob = winprob
        self._result = []
        self._reward = -250  #initial payment

    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """

        t = 0  # simulation current time

        # while the patient is alive and simulation length is not yet reached
        while t < n_time_steps:
            # determine if the patient will die during this time-step
            if self._rnd.sample() < self._winprob:
                self._result.append(flipresult.HEAD)
            else:
                self._result.append(flipresult.TAIL)
            # increment time

            if t >= 2 and self._result[t-2] == 0 and self._result[t-1] == 0 and self._result[t] == 1:
                self._reward += 100
            t += 1

        return self._result
    def get_reward(self):
        return self._reward


#test = Game(2,0.5)
#print(test.simulate(20))
#print(test.get_reward())


class Cohort:
    def __init__(self, id, pop_size,n_time_steps,winprob):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param mortality_prob: probability of death for each patient in this cohort over a time-step (must be in [0,1])
        """
        self._coins =[]
        self._rewards = []
        # populate the cohort
        n = 1
        while n <= pop_size:
            coin = Game(id * pop_size + n, winprob)
            # add the patient to the cohort
            self._coins.append(coin)
            coin.simulate(n_time_steps)
            self._rewards.append(coin.get_reward())
            # increase the population size
            n += 1

    def test(self):
        return self._rewards

    def get_average(self):
        """ returns the average survival time of patients in this cohort """
        return sum(self._rewards)/len(self._rewards)

cohort_test = Cohort(2,1000,20,0.5)

#print(cohort_test.test())
print('Average reward for fair coin is', cohort_test.get_average())

