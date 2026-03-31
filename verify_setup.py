from importlib.metadata import version

import litellm
import markdown
import matplotlib
import mesa
import numpy
import pandas
from dotenv import load_dotenv


load_dotenv()

print("All required packages imported successfully.")
print(f"Mesa version: {mesa.__version__}")
print(f"Numpy version: {numpy.__version__}")
print(f"Pandas version: {pandas.__version__}")
print(f"Matplotlib version: {matplotlib.__version__}")
print(f"Markdown module: {markdown.__version__}")
print(f"LiteLLM version: {version('litellm')}")
