import random
import math

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = { i for i in range(num_users) }
        self.friendships = { i:set() for i in range(num_users) }

        # Probability
        log_prob = math.log(1.0 - avg_friendships/num_users)

        # This is an implementation of ALG. 1 from http://vlado.fmf.uni-lj.si/pub/networks/doc/ms/rndgen.pdf
        # Nodes in graph are from 0,n-1 (start with u2 as the second node index).
        u1 = -1
        u2 = 1
        while u2 < num_users:
            log_rand = math.log(1.0 - random.random())
            # At every step, a random number is added to u1 and that new number is
            # added to the friendship. This number is sized so the probability of
            # a friend is ~ avg_friendships/num_users. If num_users was 1000 and
            # avg_friendships was 5, then int(log_rand/log_prob) would be about
            # 1000/5 = 200, on average.
            u1 = u1 + 1 + int(log_rand/log_prob)
            while u1 >= u2 and u2 < num_users:
                u1 = u1 - u2
                # u2 is incremented here to avoid potentially over-sampling nodes.
                # A later node has many opertunities to be friends with a newer
                # one; this skips older nodes roughly in proportion to their
                # likelihood of being oversampled.
                u2 = u2 + 1
            if u2 < num_users:
                self.add_friendship(u2, u1)


    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {user_id:[user_id]}
        
        stack = [[user_id]]

        while stack != []:
            stack = [ path + [f] for path in stack
                                 for f in self.friendships[path[-1]]
                                 if f not in visited ]
            for path in stack:
                visited[path[-1]] = path

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
