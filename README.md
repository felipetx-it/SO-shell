# Sistemas Operacionais - Mini Shell

Autores: Arthur do Carmo, Felipe Teixeira, Henrique Sacramento

Mini Shell desenvolvido para a aula de Sistemas Operacionais na UFBA.
O Shell foi desenvolvido em Python. Assim, para rodar o programa basta baixar o arquivo mini_shell.py, acessar a pasta em que foi baixado e chamar o programa utilizando: 

`$ python3 mini_shell.py `

Limitações conhecidas:
* O programa foi desenvolvido e testado em Linux e não funciona em ambiente Windows, pois o Windows, diferentemente de Linux, não tem a chamada fork (ou os.fork, no caso de python).
* A entrada pode ter no máximo 4096 bytes e, portanto, comandos extremamente longos não são aceitos.

Funções:
* echo: Funciona inclusive com formatações e exibição de variáveis (como $USER e $PATH).
* cat: Cria, concatena e exibe conteúdo de arquivos de texto.
* ls: 

Chamadas utilizadas:
* os.read() - Entrada de dados.
* os.write() - Saída de dados (escrita no mini shell).
* os.wait() - Fazer o processo pai aguardar o término do processo filho.
* os.fork() - Criar um processo filho fazendo uma cópia do processo pai.
* os.open() - Abre um arquivo e retorna o descritor deste arquivo.
* os.close() - Fecha o descritor do arquivo.
* os.dup2(A,B) - Faz com que o arquivo descrito pelo descritor A passe também a ser descrito pelo descritor B.
* os.execvp() - Executa um comando, substituindo o processo em curso.
* os.path.expandvars() - Expande variáveis de ambiente, como $PATH.

os.open(), neste caso, é usado para criar o arquivo que vai receber a concatenação de arquivos solicitada ao comando Cat. Isto se faz necessário pois o código de concatenção do Cat no formato:
`$ cat arquivo1.txt arquivo2.txt > arquivo3.txt ` 
se utiliza do ">", que é um recurso de redirecionamento comum de shells. Como implementamos um mini shell, evidentemente não podemos usar esse recurso, daí a necessidade do uso de os.open(), os.close() e os.dup2().

os.dup2() faz com que o arquivo aberto (arquivo3.txt, neste exemplo) passe a ser descrito também pelo descritor 1, que é o descritor de stdout (saída padrão). Então o que antes sairia na saída padrão (neste caso o terminal), passa a ser redirecionado para este arquivo3.txt. Quando o cat é efetivamente chamado pelo execvp(), ele lança o conteúdo de arquivo1.txt e arquivo2.txt na saída padrão, cujo descritor agora aponta para arquivo3.txt, concatenando ambos.

os.close() fecha o descritor original de arquivo3.txt, apenas por segurança.

Após a execuçao, o processo filho é encerrado. Como cada processo possui a sua tabela de descritores de arquivo, a operação de fazer stdout apontar para arquivo3.txt é perdida, evitando que os próximos textos escritos na saída padrão sejam também enviados para o arquivo3.txt.



Entradas e Saídas

      - Início (ao rodar o código)
      ```
      Iniciando mini-shell...
      >
      ```

1. cat
   
      input | criar um arquivo 'test.txt'
      ```
      > cat > test.txt
      Testando criação de arquivos com cat
      Arquivo criado com sucesso
      #EOF (crtl D)
      ```
      <img width="818" height="135" alt="Image" src="https://github.com/user-attachments/assets/bf7b198a-1c43-42b6-85ac-9a0ef982f931" />


      input | imprimir o arquivo 'test.txt'
      ```
      > cat test.txt
      ```
      output
      ```
      Testando criação de arquivos com cat
      Arquivo criado com sucesso
      ```


      

3. ls
   
      input | listar 
      ```
      ls
      ```
      output
      ```
      main.py  prim.py  so_alpha.py  test.txt
      ```


4. echo
   
      input | imprimir
      ```
      > echo Hello World!
      ```
      output 
      ```
      Hello World!
      ```
      
      
      input | imprimir com formatação (tab)
      ```
      > echo -e Teste \tnumero 5
      ```
      output 2
      ```
      Teste   numero 5
      ```
