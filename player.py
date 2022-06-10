import time
import multiprocessing
from sample_players import DataPlayer


class CustomPlayer(DataPlayer):
    run_count = 0
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        
        #import random
        #self.queue.put(random.choice(state.actions()))
        # print(len(state.actions()))
        # typically, len(actions) < 10. In one exception per game, len(actions) > 90.
        # so, maybe minimax with a variable depth based on len(actions) would give a good balance between speed and accuracy
        #print(len(state.actions()))
        this_run = self.run_count
        '''
        multiprocess = multiprocessing.Process(target = self.depth_altered_minimax, args = (self, state))
        multiprocess.start()
        time.sleep(1.49)
        multiprocess.terminate()
        
        if this_run == self.run_count:
            self.queue.put(random.choice(state.actions()))
        '''
        #print(len(state.actions()))
#        self.depth_altered_minimax(state)

#    def depth_altered_minimax(self, state):
        if len(state.actions()) < 5:
            self.queue.put(self.minimax(state, 5))
        elif len(state.actions()) < 10:
            #print('run 4')
            self.queue.put(self.minimax(state, 4))
        else:
            self.queue.put(self.minimax(state, 1))
#        self.run_count += 1

    def minimax(self, state, depth):

        def min_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1))
            return value

        def max_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1))
            return value
    
        return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1))

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)
