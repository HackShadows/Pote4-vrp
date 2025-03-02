from datetime import datetime
from jinja2.nativetypes import NativeEnvironment

SESSION['APP'] = "Serial Critique"
SESSION['BASELINE'] = "Critiquez vos séries !"
SESSION['HISTORIQUE'] = dict()
SESSION['CURRENT_YEAR'] = datetime.now().year