def encode_base36(num: int) -> str:
    """Convert a number to base36 string"""
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    
    if num == 0:
        return alphabet[0]
    
    result = ""
    while num > 0:
        remainder = num % 36
        result = alphabet[remainder] + result
        num = num // 36
    
    return result

def decode_base36(code: str) -> int:
    """Convert a base36 string back to a number"""
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    
    result = 0
    for char in code:
        result = result * 36 + alphabet.index(char)
    
    return result