import hashlib
import sys

import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
    if not 1 <= len(sys.argv) <= 2:
        print('Incorrect number of arguments.')
        print('Usage:')
        print('\tpython3 are-upcat-results-out.py (old UPCAT results hash)')

        sys.exit(-1)

    url = 'https://upcat.up.edu.ph/results/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html5lib')

    # Websites should really use IDs in their HTML elements.
    # Get the hash of the passers group (in the UPCAT results home page) table.
    html_passers_groups_table = str(soup.find_all('table')[1]).encode('utf-8')
    current_hash = hashlib.md5(html_passers_groups_table).hexdigest()
    
    if len(sys.argv) == 2:
        if sys.argv[1] == '--print-current-hash':
            # Produce the current hash of the UPCAT results home page.
            print(current_hash)
        elif sys.argv[1] == '--update-current-hash':
            with open('current-upcat-results-hash.txt', 'w') as f:
                f.write(current_hash)
        else:
            print('Unknown argument. Only the argument '
                  + '\'--get-current-hash\' is recognized.')
    else:
        with open('current-upcat-results-hash.txt', 'r') as f:
            old_results_hash = f.readline().strip()

        print('Yes' if current_hash != old_results_hash else 'No')
