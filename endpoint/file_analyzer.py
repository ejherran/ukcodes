
from lib2to3.pgen2.token import tok_name
from tempfile import TemporaryFile
from text_utility import TextUtility

class FileAnalizer:

    def __init__(self, file: TemporaryFile) -> None:
        self.file = file
    
    def analyze(self) -> tuple:
        coordinates = set()
        warnings = {}
        ignored_lines = 0

        line_count = 0

        with self.file as file:

            while True:

                line = file.readline()

                if not line:
                    break
                
                line_count += 1
                print(line_count)

                line = TextUtility.clean_line(line)

                if line_count == 1:
                        
                    header = TextUtility.match_regex('^lat,lon$', line)
                    if not header:
                        print("vexor")
                        warnings = TextUtility.warninRegister(warnings, 'header', 'The first line does not match the header format (lat,lon).')
                    else:
                        ignored_lines += 1
                        continue

                if(line != ''):

                    match_format = TextUtility.match_regex('^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$', line)

                    if match_format:

                        line = line.split(',')
                        coordinate = (float(line[0]), float(line[1]))
                        coordinates.add(coordinate)

                    else:
                        ignored_lines += 1
                        warnings = TextUtility.warninRegister(warnings, 'wrong_coordinate_data', str(line_count))
                    
                else:
                    ignored_lines += 1
                    warnings = TextUtility.warninRegister(warnings, 'empty_line', str(line_count))
            
            duplicates = line_count-ignored_lines-len(coordinates)

            if duplicates > 0:
                warnings = TextUtility.warninRegister(warnings, 'duplicate_coordinates', str(duplicates)+" duplicates coordinates have been ignored.")

        return coordinates, warnings