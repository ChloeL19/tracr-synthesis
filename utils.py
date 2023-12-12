import subprocess
import time
import re
import ast

# Start the REPL subprocess
python_exe = '/Users/18084/Desktop/CS252R/final_project/rasp-env-py3.9/Scripts/python.exe' #SETUP THING: replace with path to your python environment

'''
THE FOLLOWING FUNCTIONS ARE DEPRECATED
'''
def clean_carrots(text):
    pattern = r">>(.*?)>>"

    match = re.search(pattern, text)
    if match:
        result = match.group(1).strip()  # .strip() is used to remove any leading/trailing whitespace
        return result

def parse_output(out):
    out = clean_carrots(out)
    out = ast.literal_eval(out)
    # can arrive as tuple, list, or dictionary
    # ultimately want to convert everything to list form
    if isinstance(out, dict):
        return list(out.values())
    if isinstance(out, tuple):
        return list(out)
    if isinstance(out, list):
        return list
    raise Exception("Error executing rasp program.")

def run_repl(command):
    '''
    Runs the RASP repl in a separate subprocess.
    '''
    process = subprocess.Popen([python_exe, 'RASP/RASP_support/REPL.py'], 
                            stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            text=True)

    # Send commands to the REPL
    process.stdin.write(f'{command}\nexit()\n')
    process.stdin.flush()

    # Check periodically if the subprocess has terminated
    while True:
        if process.poll() is not None:
            # The subprocess has terminated
            break
        time.sleep(0.1)  # Wait for a short period (e.g., 0.1 seconds) before checking again

    # Close the subprocess if still running
    if process.poll() is None:
        process.terminate()

    # Read output and error
    output = process.stdout.readlines()
    error = process.stderr.readlines()

    # Print output and error
    str_output = ""
    str_error = ""
    for line in output:
        str_output += line.strip() + " "
    for line in error:
        str_error += line.strip() + " "
    
    str_output = parse_output(str_output)
    return str_output, str_error

if __name__ == "__main__":
    command = "select(tokens, tokens, ==)(\"hi\");"
    res, _res_err = run_repl(command)
    print(res)
    
    command = "selector_width(select(tokens, tokens, ==))(\"hi\");"
    res, _res_err = run_repl(command)
    print(res)