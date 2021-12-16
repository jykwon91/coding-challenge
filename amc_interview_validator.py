### Amerisave Interview Challenge Validator
### author David Fajardo

import json
from pathlib import Path

NOOP_ERR = '''
You must either set OUTPUT_PATH to the directory location of your output files
or paste the JSON object to validate to VALIDATION_ENTRY
'''

OUTPUT_PATH = './Output'
VALIDATION_ENTRY = {
		"test.email@domain.com": 90,
		"other.email@domain.net": 180,
	}

def is_email(string):
    return all([
        '@' in string,
        string.split('.')[-1] in ('com', 'net', 'org')
    ])

def validate_single_entry(entry):
    if type(entry) != dict:
        raise TypeError(f'entry must be a JSON object: {entry}')

    invalid_values = [v for v in entry.values() if type(v) != int]
    if len(invalid_values) > 0:
        raise TypeError(f'JSON object values must be tallies and therefore of type Number: {invalid_values}')

    invalid_keys = [k for k in entry if not is_email(k)]
    if len(invalid_keys) > 0:
        raise ValueError(f'JSON object keys must be emails: {invalid_keys}')

if OUTPUT_PATH is not None:
    out_path = f'{OUTPUT_PATH}/' if not OUTPUT_PATH.endswith('/') else OUTPUT_PATH

    try:
        with open(f'{out_path}output.json') as total_tally_file:
            json_obj = json.load(total_tally_file)
            validate_single_entry(json_obj)
    except Exception as E:
        print('an error occurred reading final tally')
        raise E

    try:
        tally_dir = f'{out_path}Output'
        for json_file in Path(tally_dir).glob('*json'):
            json_obj = json.loads(json_file)
            validate_single_entry(json_obj)
    except Exception as E:
        print('an error occurred reading files from directory')
        raise E

elif VALIDATION_ENTRY is not None:
    validate_single_entry(VALIDATION_ENTRY)

else:
    raise RuntimeError(NOOP_ERR)

print('passed')

