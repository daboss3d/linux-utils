
# Dependencies
# requests,  psutil

import os
import sys
import psutil

# sys.path.append("/utils")
from utils.text import clear_markdown_to_color, Colors, ask_yes_no
from utils.system import get_system_info



def get_shell():
    # return first non python parent process, and remove .exe
    for process in psutil.Process(os.getppid()).parents():
        if "python" not in process.name().lower():
            return process.name().lower().replace(".exe", "")


# Determine AI_TERMINAL_ASSISTANT_HOME based on the current python script location (full path)
def get_assistant_home():
    return os.path.dirname(os.path.realpath(__file__))

def user_confirm(text,template, path):
    # Let user check and confirm
    yellow = "\033[93m"
    reset = "\033[0m"
    print(Colors.yellow + template + Colors.ENDC)
    print(text)
    print(f"  {Colors.yellow}{path}{Colors.ENDC}")
    print("Press enter to continue, or Ctrl+C to cancel.")
    input()


shell = get_shell()
print("Working dir ->", get_assistant_home())

if shell == "powershell":

    print("Installing PowerShell profile...")
    # Read the $PROFILE variable with powershell
    try:
        import subprocess

        result = subprocess.check_output(
            ['pwsh', '-Command', 'echo $PROFILE'], stderr=subprocess.STDOUT, universal_newlines=True)
        profile_path = result.strip()
        if profile_path:
            print("PowerShell Profile Path:", profile_path)
        else:
            print("Could not determine PowerShell profile path.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.output}")

elif shell == "bash":
    # Log
    print("Installing Bash profile...")

    # Support colors in Windows Terminal
    os.system('')

    # Read the .bash_profile file
    profile_path = os.path.expanduser("~/.bashrc")
    profile_content = open(profile_path, "r").read()

    # Use regex replace to remove function ai() {...} from the profile
    profile_content = re.sub(r"function ai\(\) {.*?^}\s*", "", profile_content,
                             flags=re.DOTALL | re.MULTILINE)
    
    ai_function = '''
function ai {
    python3 "$AI_TERMINAL_ASSISTANT_HOME" "$*"
}
        '''
    ai_function = ai_function.replace("$AI_TERMINAL_ASSISTANT_HOME", get_assistant_home()+"/agent-helper/ah.py" )
    print("Func ->",ai_function)

    profile_content += '\n' + ai_function

    user_confirm("The above functions will be merged into your Bash profile:",ai_function, profile_path)

    # Write the profile content back to the profile
    open(profile_path, "w").write(profile_content)



elif shell == "windowsterminal":
    try:
        import subprocess
        print("Installing windowsterminal profile...")
        result = subprocess.check_output(
            ['pwsh', '-Command', 'echo $PROFILE'], stderr=subprocess.STDOUT, universal_newlines=True)
        profile_path = result.strip()

        print("profile ->",profile_path)

        ai_function = '''
function ai {
    $arguments = $args -join ' '
    python "$AI_TERMINAL_ASSISTANT_HOME" $arguments
}
        '''
        ai_function = ai_function.replace("$AI_TERMINAL_ASSISTANT_HOME", get_assistant_home()+"\\agent-helper\\ah.py" )
        print("Func ->",ai_function)

        # with open(profile_path, 'a') as file:
        #     file.write(ai_function)
        try:
            with open(profile_path, "r") as file:
                content = file.read()
                if "function ai {" in content:
                    print("Removing existing 'ai' function from profile...")
                    content = content.split('function ai {')[0]
                    content += "\n"
                    with open(profile_path, "w") as profile_file:
                        profile_file.write(content)
            print("Appending new 'ai' function to profile...")
            with open(profile_path, "a") as file:
                file.write("\n" + ai_function)

        except FileNotFoundError:
            print(f"The profile path does not exist: {profile_path}")


    except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e.output}")
else:
    print("Unsupported shell:", shell)

    sys.exit(1)    