import re
import time
import math
from colorama import Fore, init

# Initialize colorama for colored output
init(autoreset=True)

def print_banner():
    banner = r"""
         ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗          
        ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗         
        ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║         
        ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║         
        ██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝         
        ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝          
                                                                                    
███████╗████████╗██████╗ ███████╗███╗   ██╗ ██████╗████████╗██╗  ██╗███████╗██████╗ 
██╔════╝╚══██╔══╝██╔══██╗██╔════╝████╗  ██║██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗
███████╗   ██║   ██████╔╝█████╗  ██╔██╗ ██║██║  ███╗  ██║   ███████║█████╗  ██████╔╝
╚════██║   ██║   ██╔══██╗██╔══╝  ██║╚██╗██║██║   ██║  ██║   ██╔══██║██╔══╝  ██╔══██╗
███████║   ██║   ██║  ██║███████╗██║ ╚████║╚██████╔╝  ██║   ██║  ██║███████╗██║  ██║
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                    
        [ PASSWORD STRENGTHER ]
    """
    print(Fore.CYAN + banner + Fore.RESET)

def analyze_password(password):
    suggestions = []
    length = len(password)

    # Initialize counts to 0
    upper_count = lower_count = digit_count = special_count = 0

    # Check length
    if length < 8:
        suggestions.append("Use at least 8 characters.")
    elif length < 12:
        suggestions.append("Use 12+ characters for better security.")

    # Check for uppercase
    if not re.search(r'[A-Z]', password):
        suggestions.append("Add uppercase letters.")
    else:
        upper_count = sum(1 for c in password if c.isupper())

    # Check for lowercase
    if not re.search(r'[a-z]', password):
        suggestions.append("Add lowercase letters.")
    else:
        lower_count = sum(1 for c in password if c.islower())

    # Check for digits
    if not re.search(r'[0-9]', password):
        suggestions.append("Add numbers.")
    else:
        digit_count = sum(1 for c in password if c.isdigit())

    # Check for special characters
    if not re.search(r'[^A-Za-z0-9]', password):
        suggestions.append("Add special characters (e.g., !@#$%).")
    else:
        special_count = sum(1 for c in password if not c.isalnum())

    # Check for common patterns
    common_patterns = ['123456', 'password', 'qwerty', '111111', 'abc123', 'admin', 'welcome', 'letmein']
    if any(pattern in password.lower() for pattern in common_patterns):
        suggestions.append("Avoid common words or patterns.")

    # Check for repeated characters
    if re.search(r'(.)\1{2,}', password):
        suggestions.append("Avoid repeated characters.")

    # Check for sequential characters
    if re.search(r'(?:abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789|890)', password.lower()):
        suggestions.append("Avoid sequential characters.")

    # Determine strength
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[^A-Za-z0-9]', password))

    # Additional checks for character diversity
    char_diversity = len(set(password))
    complexity_score = (upper_count + lower_count + digit_count + special_count) / 4

    if length >= 12 and has_upper and has_lower and has_digit and has_special and char_diversity >= 4 and complexity_score >= 3:
        strength = "Very Strong"
        color = Fore.GREEN
    elif length >= 10 and (has_upper + has_lower + has_digit + has_special) >= 3 and char_diversity >= 3 and complexity_score >= 2:
        strength = "Strong"
        color = Fore.CYAN
    elif length >= 8 and (has_upper + has_lower + has_digit + has_special) >= 2 and char_diversity >= 2 and complexity_score >= 1:
        strength = "Medium"
        color = Fore.YELLOW
    elif length >= 6 and (has_upper + has_lower + has_digit + has_special) >= 1 and char_diversity >= 1 and complexity_score >= 0.5:
        strength = "Weak"
        color = Fore.RED
    else:
        strength = "Very Weak"
        color = Fore.RED

    # Estimate time to crack (in years)
    charset_size = 0
    if has_upper:
        charset_size += 26
    if has_lower:
        charset_size += 26
    if has_digit:
        charset_size += 10
    if has_special:
        charset_size += 32  # Approximate number of special chars

    if charset_size == 0:
        charset_size = 26  # Default to lowercase only

    # Assume 1 trillion guesses per second (modern cracking rig)
    guesses_per_second = 1e12
    possible_combinations = charset_size ** length
    time_to_crack_seconds = possible_combinations / guesses_per_second

    if time_to_crack_seconds < 1:
        time_to_crack = "Instant"
    elif time_to_crack_seconds < 60:
        time_to_crack = f"{int(time_to_crack_seconds)} seconds"
    elif time_to_crack_seconds < 3600:
        time_to_crack = f"{int(time_to_crack_seconds / 60)} minutes"
    elif time_to_crack_seconds < 86400:
        time_to_crack = f"{int(time_to_crack_seconds / 3600)} hours"
    elif time_to_crack_seconds < 31536000:
        time_to_crack = f"{int(time_to_crack_seconds / 86400)} days"
    else:
        time_to_crack = f"{int(time_to_crack_seconds / 31536000)} years"

    return strength, color, time_to_crack, suggestions

def main():
    print_banner()
    password = input(Fore.CYAN + "Enter your password: " + Fore.RESET)

    if not password:
        print(Fore.RED + "Error: No password entered." + Fore.RESET)
        return

    strength, color, time_to_crack, suggestions = analyze_password(password)

    print("\n" + Fore.CYAN + "--- Results ---" + Fore.RESET)
    print(f"Strength: {color}{strength}{Fore.RESET}")
    print(f"Time to Crack: {time_to_crack}")

    if suggestions:
        print(f"\n{Fore.CYAN}Suggestions to improve:{Fore.RESET}")
        for suggestion in suggestions:
            print(f"- {suggestion}")
    else:
        print(f"\n{Fore.GREEN}Your password is strong!{Fore.RESET}")

if __name__ == "__main__":
    main()
