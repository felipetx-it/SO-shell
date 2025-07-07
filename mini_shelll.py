import os


# Ler comando
def prompt():
    command = os.read(0, 4096)
    command = command.decode("utf-8").strip()
    command = command.split()
    if not command:
        return []  # Retorna lista vazia para que o shell só pule a linha
    if command[0] == "echo":
        return expandeVariaveis(command)
    #if command[0] == "cat":
    #    return resolveCat(command)
    return command


# Função para expandir variáveis como PATH e USER. Sem ela, echo repete $PATH ao invés do experado (exibir o PATH do sistema)
def expandeVariaveis(command):
    variaveisExpandidas = [
        os.path.expandvars(x) if '$' in x else x for x in command
    ]
    return variaveisExpandidas


def exec_command(command):
    pid = os.fork()
    # Processo pai
    if pid > 0:
        os.wait()
    # Processo filho
    elif pid == 0:
        if "cat" and ">" in command:
            command.remove(">")
            d = command[len(command) - 1]
            command.pop()
            #command.append('/dev/null')
            fd_out = os.open(
                d,
                os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
            )
            os.dup2(fd_out, 1)
            os.close(fd_out)
            #fd_null = os.open('/dev/null', os.O_RDONLY)
            #os.dup2(fd_null, 0)
            #os.close(fd_null)
        try:
            os.execvp(command[0], command)
        except FileNotFoundError:
            os.write(2, "Comando não encontrado\n".encode("utf-8"))
            os._exit(1)
        except PermissionError:
            os.write(2, f"Erro: permissão negada:{command[0]}\n".encode("utf-8"))
            os._exit(1)
        


# Resolve problema de concatenar com Cat
'''def resolveCat(command):
    if ">" in command:
        command.remove(">")
        d = command[len(command)-1]
        command.pop()
        command.append('/dev/null')
        print(command)
        fd_out = os.open(d, os.O_WRONLY | os.O_CREAT | os.O_TRUNC,)
        os.dup2(fd_out, 1)
        os.close(fd_out)
        fd_null = os.open('/dev/null', os.O_RDONLY)
        os.dup2(fd_null, 0)
        os.close(fd_null)
    return command'''


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
