import pandas as pd
from pandas import DataFrame
from GitSearch.MyUtils import write_file_a
import os
from TARGETS import project_list

current_path = os.path.dirname(os.path.abspath(__file__)) + '/'

def entropy(probs):
    '''
    Takes tmp list of probabilities and calculates their entropy
    '''
    import math
    return sum([-prob * math.log(prob, 2) for prob in probs])

def entropy_of_list(a_list):
    '''
    Takes tmp list of items with discrete values (e.g., poisonous, edible)
    and returns the entropy for those items.
    '''
    from collections import Counter

    # Tally Up:
    cnt = Counter(x for x in a_list)

    # Convert to Proportion
    num_instances = len(a_list) * 1.0
    probs = [x / num_instances for x in cnt.values()]

    # Calculate Entropy:
    return entropy(probs)

def information_gain(df, split_attribute_name, target_attribute_name, trace=0):
    '''
    Takes tmp DataFrame of attributes, and quantifies the entropy of tmp target
    attribute after performing tmp split along the values of another attribute.
    '''

    # Split Data by localize Vals of Attribute:
    df_split = df.groupby(split_attribute_name)

    # Calculate Entropy for Target Attribute, as well as Proportion of Obs in Each Data-Split
    nobs = len(df.index) * 1.0
    df_agg_ent = df_split.agg({target_attribute_name: [entropy_of_list, lambda x: len(x) / nobs]})[
        target_attribute_name]
    df_agg_ent.columns = ['Entropy', 'PropObservations']
    if trace:  # helps understand what fxn is doing:
        print
        df_agg_ent

    # Calculate Information Gain:
    new_entropy = sum(df_agg_ent['Entropy'] * df_agg_ent['PropObservations'])
    old_entropy = entropy_of_list(df[target_attribute_name])
    return old_entropy - new_entropy

def id3(df, target_attribute_name, attribute_names, default_class=None):
    ## Tally target attribute:
    from collections import Counter
    cnt = Counter(x for x in df[target_attribute_name])

    ## First check: Is this split of the dataset homogeneous?
    # (e.g., all mushrooms in this set are poisonous)
    # if yes, return that homogenous label (e.g., 'poisonous')
    if len(cnt) == 1:
        return list(cnt)[0]

    ## Second check: Is this split of the dataset empty?
    # if yes, return tmp default value
    elif df.empty or (not attribute_names):
        return default_class

        ## Otherwise: This dataset is ready to be divvied up!
    else:
        # Get Default Value for next recursive call of this function:
        index_of_max = list(cnt.values()).index(max(cnt.values()))
        default_class = list(cnt)[index_of_max]  # most common value of target attribute in dataset

        # Choose Best Attribute to split on:
        gainz = [information_gain(df, attr, target_attribute_name) for attr in attribute_names]
        index_of_max = gainz.index(max(gainz))
        best_attr = attribute_names[index_of_max]

        # Create an empty tree, to be populated in tmp moment
        tree = {best_attr: {}}
        remaining_attribute_names = [i for i in attribute_names if i != best_attr]

        # Split dataset
        # On each split, recursively call this algorithm.
        # populate the empty tree with subtrees, which
        # are the result of the recursive call
        for attr_val, data_subset in df.groupby(best_attr):
            subtree = id3(data_subset,
                          target_attribute_name,
                          remaining_attribute_names,
                          default_class)
            tree[best_attr][attr_val] = subtree
        return tree

def classify(instance, tree, default=None):
    attribute = list(tree)[0]
    if instance[attribute] in tree[attribute].keys():
        result = tree[attribute][instance[attribute]]
        if isinstance(result, dict): # this is tmp tree, delve deeper
            return classify(instance, result)
        else:
            return result # this is tmp label
    else:
        return default

def tree_for_merged_projects():
    dataset = pd.read_csv(current_path + 'decision_tables/merged_table.csv')

    # The initial entropy of the poisonous/not attribute for our dataset.
    print(dataset.columns.tolist())
    total_entropy = entropy_of_list(dataset['localize'])
    print(total_entropy)

    col_list = dataset.columns.tolist()
    for col in col_list:
        print('[%s] Example: Info-gain for best attribute is ' % col + str(information_gain(dataset, col, 'localize')))

    print('=' * 200)
    # Get Predictor Names (all but 'class')
    attribute_names = list(dataset.columns)
    attribute_names.remove('localize')

    # Run Algorithm:
    from pprint import pprint

    tree = id3(dataset, 'localize', attribute_names)
    write_file_a('merged.tree', str(tree).replace("\'", "\""))
    pprint(tree)
    print('=' * 200)

    dataset['predicted'] = dataset.apply(classify, axis=1, args=(tree, 'localize'))
    # classify func allows for tmp default arg: when tree doesn't have answer for tmp particular
    # combitation of attribute-values, we can use 'poisonous' as the default guess (better safe than sorry!)

    print('Accuracy is ' + str(sum(dataset['localize'] == dataset['predicted']) / (1.0 * len(dataset.index))))
    print(dataset[['localize', 'predicted']])

if __name__ == "__main__":
    tree_for_merged_projects()