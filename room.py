from collections import defaultdict
from functools import reduce
import re

class Room:
    def __init__(self, room_name):
        self.room_name = room_name
        self.name = self.get_name()
        self.sector_id = self.get_sector_id()
        self.checksum = self.get_checksum()
        self.real_name = self.get_realname()
    
    def get_name(self):
        name_match = re.compile('([a-z]+\-)+').match(self.room_name)
        return name_match.group().rstrip('-')
    
    def get_sector_id(self):
        last_hyphen = [m.start() for m in re.finditer('-',self.room_name)][-1]
        beginning_index = last_hyphen + 1
        end_index = self.room_name.find('[')

        return int(self.room_name[beginning_index:end_index]) 
    
    def get_checksum(self):
        beginning_index = self.room_name.find('[') + 1
        end_index = self.room_name.find(']')
        
        return self.room_name[beginning_index:end_index]

    def get_realname(self):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'*100

        def translate(char, steps):
            if char == '-':
                return ' '
            else:
                new_index = alphabet.find(char) + steps
                return alphabet[new_index]
            
        
        exploded = [translate(char, self.sector_id) for char in list(self.name)]
        return ''.join(exploded)
    

def validate(room):
    no_hyphens = room.name.replace("-", "")
    counts = {char: str(no_hyphens.count(char)) for char in set(no_hyphens)}
    
    count_frequencies = defaultdict(list)
    for char, value in counts.items():
        count_frequencies[value].append(char)

    reverse_sorted_count_frequencies = [sorted(count_frequencies[char], reverse=True) for char in sorted(count_frequencies)]
    order = reduce((lambda x, y: x + y), reverse_sorted_count_frequencies)

    return not any([char not in order[-5:] for char in room.checksum]) 


if __name__ == "__main__":
    with open('./input.txt', 'r') as f:
        names = [ line.rstrip('\n') for line in f.readlines() ]
    
    valid_rooms = [Room(name) for name in names if validate(Room(name))]
    print("Sum of valid room sector_id's: ", sum([ room.sector_id for room in valid_rooms ]) )
    
    pole_rooms = [room.sector_id for room in valid_rooms if 'pole' in room.real_name]
    print("sector_id for room with North Pole Storage:", pole_rooms)
