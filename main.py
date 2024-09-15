import os
import shutil
import sys
import subprocess

def clear():
    if os.name == 'nt':  
        os.system('cls')
    else:  
        os.system('clear')

def get_terminal_size():
    size = shutil.get_terminal_size((80, 20))
    return size.columns, size.lines

def center_text_horizontally(text_lines):
    columns, _ = get_terminal_size()

    for line in text_lines:
        print(line.center(columns))

def get(filename):
    program = []
    with open(filename, 'r') as file:
        for line in file:
            program.append(line.rstrip('\n'))
    return program

def execute_shell_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    program = get(sys.argv[1])
    os_type = 'nt' if os.name == 'nt' else 'unix'
    execute_section = None
    last_input = None
    condition_met = False

    for line in program:
        if line.startswith('#'):
            text = line[2:]
            center_text_horizontally([text])
        elif line.startswith('$'):
            text = line[2:]
            last_input = input(text)
            clear()
        elif line.startswith('&'):
            if last_input is not None:
                print(last_input)
        elif line.startswith('!'):
            metadata = line[1:].strip()
            if metadata == 'nt' and os_type == 'nt':
                execute_section = 'nt'
            elif metadata == 'unix' and os_type == 'unix':
                execute_section = 'unix'
            else:
                execute_section = None
        elif line.startswith('<if') and line.endswith('>'):
            condition = line[4:-1].strip()
            if last_input == condition:
                condition_met = True
            else:
                condition_met = False
        elif line.startswith('</if>'):
            condition_met = False
        elif line.startswith('<') and line.endswith('>'):
            command = line[1:-1].strip()
            if execute_section and condition_met:
                if last_input is not None:
                    command = command.replace('&', last_input)
                execute_shell_command(command)
        else:
            # Handle escaped characters
            line = line.replace('\\#', '#').replace('\\$', '$').replace('\\&', '&').replace('\\<', '<').replace('\\>', '>')
            if condition_met or execute_section:
                print(line)
