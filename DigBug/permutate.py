from itertools import permutations, combinations

# Get all permutations of [1, 2, 3]
perm = permutations([1, 2, 3])

l = ['classname', 'developer', 'attachment', 'description', 'stacktrace']
perm = permutations(l)
# Print the obtained permutations
for i in list(perm):
    print(i)
# print(combinations(l))


from itertools import chain, combinations

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)  # allows duplicate elements
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

stuff = [1, 2, 3]
for i, combo in enumerate(powerset(l), 1):
    print('combo #{}: {}'.format(i, combo))