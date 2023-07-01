import datetime
from colorama import init, Fore, Style

def log(message, level='INFO'):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if level == 'INFO':
        log_message = f'{Fore.GREEN}[INFO]{Style.RESET_ALL}'
    elif level == 'SUCCESS':
        log_message = f'{Fore.CYAN}[SUCCESS]{Style.RESET_ALL}'
    elif level == 'ERROR':
        log_message = f'{Fore.RED}[ERROR]{Style.RESET_ALL}'
    else:
        log_message = f'{Fore.YELLOW}[{level}]{Style.RESET_ALL}'
    
    print(f'{timestamp} {log_message} {message}')