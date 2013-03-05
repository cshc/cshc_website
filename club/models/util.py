from exceptions import IndexError

# This file contains utility methods used in multiple other files/modules.
# Whenever you write a method that relates to models and is generic and re-usable, 
# put it in here!

def first_or_none (q): 
    """ Returns the first item from a query-set, or None if the query-set is empty."""
    try: 
        return q[0] 
    except IndexError: 
        return None 