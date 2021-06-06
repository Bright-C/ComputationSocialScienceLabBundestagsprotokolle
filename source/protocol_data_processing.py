class ProtocolDataProcessor:
    def __init__(self):
        pass

    """
        ### Parameters
    1. data : ProtocolData
        - The protocol data to perform processing on. The results of the evaluation should be written back to the object using setters.

    ### Returns
    - void
    """
    def process_data(self, data):
        pass

class CountWordsPrecedingInterjection(ProtocolDataProcessor):
    def __init__(self, neighborhood_character_distance):
        super()
        self.neighborhood_distance = neighborhood_character_distance

    def process_data(self, data):
        for interjection, location in data.interjection_locations.items():
            preceding_neighbor_words = data.text[location - self.neighborhood_distance:location].split()

            for word in preceding_neighbor_words:
                data.count_word_preceding_interjection(word)

class Vector2WordProcessor(ProtocolDataProcessor):
    def process_data(self, data):
        return super().process_data(data)
