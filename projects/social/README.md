# Social Graph

You have been assigned the task of building a new friend-based social network. In this network, users are able to view their own friends, friends of their friends, friends of their friends' friends, and so on. People connected to you through any number of friendship connections are considered a part of your extended social network.

The functionality behind creating users and friendships has been completed already. Your job is to implement a function that shows all the friends in a user's extended social network and chain of friendships that link them. The number of connections between one user and another are called the degrees of separation.

Your client is also interested in how the performance will scale as more users join so she has asked you to implement a feature that creates large numbers of users to the network and assigns them a random distribution of friends.

## 1. Generating Users and Friendships

It will be easier to build your extended social network if you have users to test it with. `populate_graph()` takes in a number of users to create and the average number of friends each user should have and creates them.

```
>>> sg = SocialGraph()
>>> sg.populate_graph(10, 2)  # Creates 10 users with an average of 2 friends each
>>> print(sg.friendships)
{1: {8, 10, 5}, 2: {10, 5, 7}, 3: {4}, 4: {9, 3}, 5: {8, 1, 2}, 6: {10}, 7: {2}, 8: {1, 5}, 9: {4}, 10: {1, 2, 6}}
>>> sg = SocialGraph()
>>> sg.populate_graph(10, 2)
>>> print(sg.friendships)
{1: {8}, 2: set(), 3: {6}, 4: {9, 5, 7}, 5: {9, 10, 4, 6}, 6: {8, 3, 5}, 7: {4}, 8: {1, 6}, 9: {10, 4, 5}, 10: {9, 5}}
```

Note that in the above example, the average number of friendships is exactly 2 but the actual number of friends per user ranges anywhere from 0 to 4.

* Hint 1: To create N random friendships, you could create a list with all possible friendship combinations, shuffle the list, then grab the first N elements from the list. You will need to `import random` to get shuffle.
* Hint 2: `add_friendship(1, 2)` is the same as `add_friendship(2, 1)`. You should avoid calling one after the other since it will do nothing but print a warning. You can avoid this by only creating friendships where user1 < user2.

## 2. Degrees of Separation

Now that you have a graph full of users and friendships, you can crawl through their social graphs. `get_all_social_paths()` takes a userID and returns a dictionary containing every user in that user's extended network along with the shortest friendship path between each.

```
>>> sg = SocialGraph()
>>> sg.populate_graph(10, 2)
>>> print(sg.friendships)
{1: {8, 10, 5}, 2: {10, 5, 7}, 3: {4}, 4: {9, 3}, 5: {8, 1, 2}, 6: {10}, 7: {2}, 8: {1, 5}, 9: {4}, 10: {1, 2, 6}}
>>> connections = sg.get_all_social_paths(1)
>>> print(connections)
{1: [1], 8: [1, 8], 10: [1, 10], 5: [1, 5], 2: [1, 10, 2], 6: [1, 10, 6], 7: [1, 10, 2, 7]}
```
Note that in this sample, Users 3, 4 and 9 are not in User 1's extended social network.

* Hint 1: What kind of graph search guarantees you a shortest path?
* Hint 2: Instead of using a `set` to mark users as visited, you could use a `dictionary`. Similar to sets, checking if something is in a dictionary runs in O(1) time. If the visited user is the key, what would the value be?

## 3. Questions

1. To create 100 users with an average of 10 friends each, how many times would you need to call `add_friendship()`? Why?

```
In order to get a group of people to have 10 friends with a minimum number of calls, I need to get 11 people to be friends with eachother. Since I only need to call add_friendship once per direction, the number of times this needs to be called decreases per person, with the final person already being friends with 10 people by the time we get to them.

This is exemplified by the sum

  n
  Σ   n - i
i = 1

where n is 10, in this case. This simplifies to (n² - n)/2 calls, which is 45 calls, in our case. We need to do this for all groups of 11 people in our group of 100. This means we multiply tha number by (100 / 11). In agrigate, if our total is T, and our average friends is n, we need to make about (n² - n)/2 * T/(n+1) calls. For our case, this is ~410 calls.

That function can be rewriten as (n T)/2 + (n T)/(1 + n); the discrete asymptotic of that function is (n T)/2, so the number of calls is linear in the product of the average and the total.

My implementation, in order to be more random, is not this efficient. Instead, it makes n calls per person. This is n * T, or 1000 calls. These calls just add 10 random friends to the person, 10 calls per person with 100 people is 1000 calls.

Update: I replaced my old implementation with one with O(T + T n) time.
```

2. If you create 1000 users with an average of 5 random friends each, what percentage of other users will be in a particular user's extended social network? What is the average degree of separation between a user and those in his/her extended network?

```
???What this is basically asking is "what's the likelyhood that the graph is fully connected", as the extended network will try covering the whole graph. This likelihood will simply be one minus our probabilty. (See http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.45.7433&rep=rep1&type=pdf, t(c, n), page 2). That means the likelihood of a connection should be 199/200, or 99.5%.???

The average degree of separation should be on the order of log₅(1000) ~= 4.29. (See: http://www.math.ucsd.edu/~fan/wp/aveflong.pdf, Theorem 1). This is born out by some experimenting;

>>> from numpy import mean
>>> from social import *
>>> s =  SocialGraph()
>>> s.populate_graph(1000, 5)
>>> mean([ len(p)-1 for i in s.users for p in s.get_all_social_paths(i).values() ])
4.270242
```


## 4. Stretch Goal

1. You might have found the results from question #2 above to be surprising. Would you expect results like this in real life? If not, what are some ways you could improve your friendship distribution model for more realistic results?

2. If you followed the hints for part 1, your `populate_graph()` will run in O(n^2) time. Refactor your code to run in O(n) time. Are there any tradeoffs that come with this implementation?

```
I can say there's collision problems. The actual likelihood ends up being slightly lower than the input.
```

