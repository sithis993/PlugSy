'''
PlugSy Utils - Topological sort for sorting plugin dependencies
'''

# Import libs

# Import package modules
from ..Exceptions import PluginCircularDependency

def toposort(data):
    '''
    Topological sorting function

    :param data: Dictionary of <string>:<set> where string is a an item name of forms, and <set> is a list of the
        item's dependencies
    :return: Items are yielded in topologically sorted order
    '''

    # Check data isn't empty
    if len(data) == 0:
        return

    # Copy data
    data = data.copy()

    # Remove any self-dependencies
    for item, deps in data.items():
        deps.discard(item)

    # Find all independent items (items within a deps set that don't have a dep set of their own)
    independent_items = set()
    for item, deps in data.items():
        # Iterate all of the keys values and check for deps not in keys list
        for dependency in data[item]:
            if dependency not in data:
                independent_items.update([dependency])

    # Add independent items with a deps set to the data, with an empty set
    for item in independent_items:
        data.update({item: set()})

    # Resolve dependencies until none remaining
    while True:
        # Add items with no deps to set and yield them. Break if none left
        ordered = set(item for item, dep in data.items() if len(dep) == 0)
        if not ordered:
            break
        yield ordered

        # This is where items the deps of items are basically removed until that item has no more deps
        data = {
            item: (dep - ordered) for item, dep in data.items() if item not in ordered
        }

    # If there are items remaining, must be circular dependency
    if len(data) > 0:
        raise PluginCircularDependency()
