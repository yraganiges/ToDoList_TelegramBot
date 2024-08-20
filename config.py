from json import load

# --JSON--
with open("data\\config.json", 'r') as json_file:
    j = load(json_file)
    
current_note: str = None