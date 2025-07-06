import os

# Ler comando
def prompt():
    call = b""
    while b"\n" not in call:
        ent = os.read(0, 1)
        if call == None: break
    call += ent
    return call.decode().strip().strip()

def exec_command(command):
    command = ["python3"] + command
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
        if command == "exit":
            break
            
        exec_command(command)
    os.write(1, b"Finalizando mini-shell...")

if __name__ == "__main__":
    mini_shell()
