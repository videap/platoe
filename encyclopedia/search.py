
def search_string(substring, items):
    found = []
   
    for item in items:
        item = str(item)
        if item.lower().find(substring.lower()) != -1:
            found.append(item)
    
    return found
