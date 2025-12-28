from math import floor

from voluptuous import Schema, Required, Range

from ultraconv.models import UltrastarFile, AbstractProcessor, ProcessorType, ProcessorInfo, UltrastarText, UltrastarBreak

class AlignerSimpleAlgo(AbstractProcessor):

    def __init__(self, config):
        super().__init__(config)
        self.line_length_pct = config.get('line_length_pct', 0.95)
        self.word_length_pct = config.get('word_length_pct', 0.8)

    def run(self, data: UltrastarFile) -> UltrastarFile:
        if not data.events or len(data.events) == 0:
            return data
        
        new_events = []
        current_line = []

        def _find_next_line_start(index):
            if index+1 < len(data.events):
                return data.events[index+1].time
            # TODO: return total song length ??
            return data.events[index].time + data.to_beat(5) # arbitrary 5 seconds after last event

        for i in range(len(data.events)):
            event = data.events[i]

            if isinstance(event, UltrastarBreak):
                # once we hit a break, process the current line

                if len(current_line) < 2:
                    # if less than 2 text events, skip realignment
                    new_events.extend(current_line)
                else:
                    start = current_line[0].time
                    next_line_start = _find_next_line_start(i)
                    nb_letters = sum([len(x.text) for x in current_line])

                    line_duration = (next_line_start - start) * self.line_length_pct # use 90% of line length for word, and keep 10% for the break
                    avg_duration_by_letter = line_duration / nb_letters

                    # realign words
                    for line_evt in current_line:
                        if isinstance(line_evt, UltrastarText):
                            word = line_evt.text
                            word_full_duration = len(word) * avg_duration_by_letter
                            word_duration = word_full_duration * self.word_length_pct # use only 80% of the timeframe as we also need "blank" space between words
                            
                            line_evt.time = start
                            line_evt.length = floor(word_duration)
                            new_events.append(line_evt)

                            start += floor(word_full_duration)
                    # add break
                    event.time = start # start = line_duration (since all words have been added); so, break duration = (next_line_start - start) * (1 - line_length_pct)
                    new_events.append(event)

                # reset for next line
                current_line = []
            else:
                current_line.append(event)
    
        data.events = new_events
        return data

    @staticmethod
    def get_info() -> ProcessorInfo:
        """Return the info of the processor."""
        return ProcessorInfo(
            name="Basic length-based aligner",
            description="Aligns lyrics based on word length. Only works when lines are already time-aligned.",
            processor_type=ProcessorType.LYRICS_ALIGNER
        )
    
    @staticmethod
    def is_available():
        return True

    @staticmethod
    def get_options():
        return Schema({
            Required("line_length_pct", default=0.95): Range(min=0.1, max=1.0),
            Required("word_length_pct", default=0.8): Range(min=0.1, max=1.0)
        })
