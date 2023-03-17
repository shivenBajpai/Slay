from Constants import AUTOREBOOT
from Slay_Server import main

try:
    if AUTOREBOOT:     
        while True:
            result = main()
            print(f'Server stopped with code/result: {result}')
            print('  |\n  |\n  |Auto Restarting\n  |\n  |\n')       
    else:
        result = main()
        print(f'Server stopped with code/result: {result}')
except KeyboardInterrupt:
    print('KeyboardInterrupt caught')