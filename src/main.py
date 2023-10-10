import sys
sys.path.append("src/utilis")

import os

path = os.path.abspath("src/messages")
sys.path.append(path)
sys.path.append("src/agents/currency")
import userDatabase
import currencyrates
import my_email

