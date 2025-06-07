import argparse
import json
import requests

import platform
import subprocess
import os
import time
from multiprocessing import Process
from functools import partial


# print("DIR ->",os.path.dirname(os.path.realpath(__file__)))


# from text import clear_markdown_to_color
#from ..utils  import  text
# import sys
# sys.path.append("../utils")

import sys
# Get the current directory and its parent directory
current_directory = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current_directory)
utils_directory = os.path.join(parent_directory, "utils")
print("parent ->", parent_directory) 
print("utils ->", utils_directory) 
# Add the utils directory to sys.path
sys.path.append(utils_directory)



from text import clear_markdown_to_color, Colors, ask_yes_no
from system import get_system_info

 
class Spinner:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Spinner, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.clear_function = None
        self.color = "\033[96m"
        self.process = None
        self.counter = 0

    class Colors:
        CYAN = "\033[96m"
 

    @staticmethod
    def spinner_symbols():
        return ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴']

    def set_color(self, color):
        self.color = color

    def set_clear_function(self, clear_function):
        self.clear_function = clear_function

    def start(self):
        self._safe_target = partial(self._start_method)
        self._process = Process(target=self._safe_target)

        if not os.name == 'nt':
            try:
                import psutil
                parent_process = psutil.Process(os.getpid())
                for child in parent_process.children(recursive=True):
                    child.kill()
            except Exception as e:
                print(f'Warning: Could not clean up processes correctly - {e}')
        else:
            pass  # Windows does this differently, we'll just start the process directly

        self._process.start()

    def stop(self):
        if self.clear_function is not None:
            self.clear_function()
        print("\r", end="")
        self._process.terminate()   # Properly terminate
        self._process.join()       # wait for the process to finish.


    def _start_method(self):
        symbols = Spinner.spinner_symbols()

        while True:
            symbol = symbols[self.counter % len(symbols)]
            if callable(self.clear_function):
                self.clear_function()
            print(f'\r{self.color}🤖{symbol}\033[0m ', end='', flush=True)
            self.counter += 1
            time.sleep(0.1)

# Load the configuration from config.json

def load_config():
    try:
        config_path = os.path.join(current_directory, "config.json")
        with open(config_path) as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("Configuration file (config.json) is missing!")
        exit(1)
    except KeyError as e:
        print(f"Missing key in config: {str(e)}")
        exit(1)

    except FileNotFoundError:
        print("Configuration file (config.json) is missing!")
        exit(1)
    except KeyError as e:
        print(f"Missing key in config: {str(e)}")
        exit(1)


def process_ollama_response(response):
    full_response = ""
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line)
            if not chunk.get("done"):
                response_piece = chunk.get("response", "")
                full_response += response_piece
                # print(response_piece, end="", flush=True)

def create_payload_query(prompt):
    ollama_prompt_explanation = """
        Explain what the shell command and its parameters do. Be concise. Don't use markdown on reply
    """

    return {
        "model": MODEL_NAME,
        "prompt": f"{ollama_prompt_explanation}\n\n{prompt}"
    }


def query_ollama_stream(prompt):

    payload = create_payload_query(prompt)
    with requests.post(OLLAMA_URL, json=payload, stream=True) as response:

        response.raise_for_status()

        # Variable to hold concatenated response strings if no callback is provided
        full_response = ""

        # Iterating over the response line by line and displaying the details
        for line in response.iter_lines():
            if line:
                # Parsing each line (JSON chunk) and extracting the details
                chunk = json.loads(line)

                # If this is not the last chunk, add the "response" field value to full_response and print it
                if not chunk.get("done"):
                    response_piece = chunk.get("response", "")
                    full_response += response_piece
                    print(response_piece, end="", flush=True)

        if response == "":
            print("Error parsing response")
            exit(-1)


def query_ollama(prompt):

    payload = create_payload_query(prompt)

    spinner = Spinner()
    spinner.start()
 
    response_text = ""

    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True) as response:
            response.raise_for_status()
 
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    # Check if the chunk has a done flag
                    if not chunk.get("done"):
                        response_piece = chunk.get("response", "")
                        response_text += response_piece
                        # print(response_piece, end="", flush=True)

            print()  # To ensure new line after printing the command

    except requests.RequestException as e:
        print(f"Error fetching data from Ollama: {str(e)}")
    finally:
        if response_text.strip() == "":
            return "No response received."

        spinner.stop()
        return clear_markdown_to_color(response_text)
       
def query_ollama_file(prompt):

    response_text = ""


def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return None, e.output

def main():

    # print(get_system_info())
    # print( ask_yes_no("Do you want to continue ?"))

    parser = argparse.ArgumentParser(description="Agent helper for terminal commands")
    parser.add_argument('-s','--stream', action='store_true',   help='Stream the response')
    parser.add_argument('-q', metavar='<prompt>', type=str, help='Query Ollama about <command>')
    parser.add_argument('-e', metavar='<command>', type=str, help='Execute <command>')
    parser.add_argument('-f', metavar='<prompt>', type=str, help='Query Ollama about <command>')
    parser.add_argument('search_string', type=str, nargs='?', default=None, help='The string to find within the file')

    args = parser.parse_args()

    if args.q:
        if args.stream:
            # print("Stream the response ...")
            query_ollama_stream(args.q)
            return

        response = query_ollama(args.q)
        print(response)

    elif args.e:
        stdout, stderr = execute_command(args.e)
        if stdout is None:
            print(f"Error executing command: {stderr}")
        else:
            print(stdout)

    elif args.f:
        print("File",args.f )
        if args.search_string:
            print("Prompt",args.search_string)


if __name__ == "__main__":
    config = load_config()
    OLLAMA_URL = config["ollama_url"]
    MODEL_NAME = config["model"]
    main()