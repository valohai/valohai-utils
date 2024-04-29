from typing import Dict

import valohai

params: Dict = {"initial_date": "(2023, 9, 1)", "final_date": "(2023, 11, 30)"}

valohai.prepare(step="issue-129", default_parameters=params)
