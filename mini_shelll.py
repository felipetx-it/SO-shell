import os


# Ler comando
def prompt():
    try:
        command = os.read(0, 4096)
        # Checa EOF (crtl D)
        if command == b"":
            raise EOFError
    
        command = command.decode("utf-8").strip()
        command = command.split()
        if not command:
            return []
        if command[0] == "echo":
            return expandeVariaveis(command)

        return command
    except EOFError:
        return ["exit"] # crtl D -> exit shell
    except Exception as e:
        os.write(2, f"Erro ao ler comando: {str(e)}\n".encode("utf-8"))
        return []


# Função para expandir variáveis como PATH e USER. Sem ela, echo repete $PATH ao invés do experado (exibir o PATH do sistema)
def expandeVariaveis(command):
    variaveisExpandidas = [
        os.path.expandvars(x) if '$' in x else x for x in command
    ]
    return variaveisExpandidas


def exec_command(command):
    try:
        pid = os.fork()
    except OSError as e:
        os.write(2, f"Erro ao criar processo: {os.strerror(e.errno)}\n".encode("utf-8"))
        return
    
    # Processo pai
    if pid > 0:
        try:
            os.wait()
        except OSError as e:
            os.write(2, f"Erro ao aguardar processo filho: {os.strerror(e.errno)}\n".encode("utf-8"))

    # Processo filho
    if pid == 0:
            
        if "cat" in command and ">" in command:
            i = command.index(">") #encontra o ">"
            d = command[i+1]       #pega o proximo item, que nesse caso é o arquivo final
            command = command[:i]  #remove do comando de i (">") em diante
            try: 

                fd_out = os.open(
                    d,
                    os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
                    0o644
                )
                os.dup2(fd_out, 1)
                os.close(fd_out)  
            except OSError as e:
                    os.write(2, f"Erro ao abrir arquivo '{d}': {os.strerror(e.errno)}\n".encode("utf-8"))
                    os._exit(1)     
        try:
            os.execvp(command[0], command)
        except FileNotFoundError:
            os.write(2, "Comando não encontrado\n".encode("utf-8"))
            os._exit(1)
        except PermissionError:
            os.write(2, f"Erro: permissão negada: {command[0]}\n".encode("utf-8"))
            os._exit(1)
        except OSError as e:
            os.write(2, f"Erro ao executar comando: {os.strerror(e.errno)}\n".encode("utf-8"))
            os._exit(1)
        

def mini_shell():
    os.write(1, b"\nIniciando mini-shell...\n")

    try:
        while True:
            os.write(1, b"> ")
            command = prompt()

            if not command:
                continue
            if command == ["exit"]:
                break

            exec_command(command)
        os.write(1, b"Finalizando mini-shell...\n")
    except KeyboardInterrupt:
        os.write(1, b"Digite 'exit' para sair\n")
    except Exception as e:
        os.write(2, f"\nErro inesperado: {str(e)}\n".encode("utf-8"))


if __name__ == "__main__":
    mini_shell()
