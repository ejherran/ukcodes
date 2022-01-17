import re

class TextUtility:

    @staticmethod
    def remove_ghost_line(lines: list) -> list:

        if lines[-1] == '':
            lines.pop()
        
        return lines
    
    @staticmethod
    def block_to_lines(block: str) -> list:
        
        block = block.replace('\r', '')
        return block.split('\n')

    @staticmethod
    def clean_line(line: bytearray) -> str:
        line = line.decode('utf-8')
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        return line
    
    @staticmethod
    def match_regex(regex: str, line: str) -> bool:
        match = re.match(regex, line)
        if match:
            return True
        else:
            return False
    
    @staticmethod
    def validCoordinate(line: str) -> bool:
        
        try:
            
            line = line.split(',')
            lat = float(line[0])
            lon = float(line[1])

            if (lat >= -90 and lat <= 90) and (lon >= -180 and lon <= 180):
                return True
            else:
                return False
                
        except:
            return False


    @staticmethod
    def warninRegister(warnings: dict, category: str, data: str) -> dict:
        
        if category in warnings:
            warnings[category] += ', ' + data
        else:
            warnings[category] = data
        
        return warnings