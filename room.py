import re

class Room:
    def __init__(self, room_name):
        self.room_name = room_name
        self.name = self.get_name()
        self.sector_id = self.get_sector_id()
        self.checksum = self.get_checksum()
    
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
    

def validate(room):
    no_hyphens = room.name.replace("-", "")
    counts = {char: str(no_hyphens.count(char)) for char in set(no_hyphens)}
    count_frequencies = {}
    for char, value in counts.items():
        if value in count_frequencies.keys():
            count_frequencies[value].append(char)
        else:
            count_frequencies[value] = [char]
    
    order = []
    for frequency in iter(sorted(count_frequencies, reverse=True)):
        order = order + sorted(count_frequencies[frequency])

    return not any([char not in order[:5] for char in room.checksum]) 


if __name__ == "__main__":
    with open('./input.txt', 'r') as f:
        names = [ line.rstrip('\n') for line in f.readlines() ]
    
    sum = 0
    for name in names:
        room = Room(name)
        if validate(room):
            sum += room.sector_id
    
    print(sum)