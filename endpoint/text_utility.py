import re

class TextUtility:

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
    def warninRegister(warnings: dict, category: str, data: str) -> dict:
        
        if category in warnings:
            warnings[category] += ', ' + data
        else:
            warnings[category] = data
        
        return warnings