from exceptions import IndexError

def first_or_none (q): 
    try: 
        return q[0] 
    except IndexError: 
        return None 