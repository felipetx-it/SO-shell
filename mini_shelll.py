import os

# Ler comando
def prompt():
    command = os.read(0, 4096)
    command = command.decode("utf-8").strip()
    command = command.split()

    return command 

def exec_command(command):
    pid = os.fork()
    # Processo pai
    if pid > 0: 
        os.wait()
    # Processo filho
    elif pid == 0:
        os.execvp(command[0], command)



def mini_shell():
    os.write(1, b"Iniciando mini-shell...")

    while True:
        os.write(1, b"> ")
        command = prompt()

        if not command:
            continue
        if command == ["exit"]:
            break
            
        exec_command(command)
    os.write(1, b"Finalizando mini-shell...")

if __name__ == "__main__":
    mini_shell()
