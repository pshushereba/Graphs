import random
from util import Queue

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}

        # this is your adjacency list representation of a graph.
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship

        Therefore creates an undirected graph

        Makes TWO friendships
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def get_friends(self, user_id):
        return self.friendships[user_id]

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
        self.users = {}
        self.friendships = {}

        # Add users
        for user in range(num_users):
            self.add_user(user)
            
        # Create friendships
        friendship_combinations = []

        for user in range(1, self.last_id + 1):
            for friend in range(user + 1, self.last_id + 1):
                friendship_combinations.append((user, friend))

        # shuffle the list
        random.shuffle(friendship_combinations)

#       # Calculate the number of friendships (edges) needed in the graph.
        total_friendships = num_users * avg_friendships

        friends_to_make = friendship_combinations[:(total_friendships // 2)]

        # Create friendships
        for friendship in friends_to_make:
            self.add_friendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        #visited = set()
        # Create an empty queue and enqueue A PATH TO the starting vertex ID.
        q = Queue()
        # Create a Set to store visited vertices.
        path = [user_id]
        q.enqueue(path)
        # While the queue is not empty...
        while q.size() > 0:
        # Dequeue from the front of the line, this is our current path.
            current_path = q.dequeue()
        # current_node is the last thing in the path
            current_node = current_path[-1]
        # Check if we've visited yet, if not:
            if current_node not in visited:
                # mark as visited
                #visited.add(current_node)
                visited[current_node] = current_path

                # get the current node's friends
                friends = self.get_friends(current_node)
                # iterate over the friends
                for friend in friends:
                    # add the neighbor to the path
                    friend_path = current_path.copy()
                    friend_path.append(friend)
                    # enqueue the neighbor's path
                    q.enqueue(friend_path)
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
