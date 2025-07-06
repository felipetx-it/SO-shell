# Sistemas Operacionais - Mini Shell

Autores: Arthur do Carmo, Felipe Teixeira, Henrique Sacramento

Mini Shell desenvolvido para a aula de Sistemas Operacionais na UFBA.
O Shell foi desenvolvido em Python. Assim, para rodar o programa basta baixar o arquivo mini_shell.py, acessar a pasta em que foi baixado e chamar o programa utilizando: 

`$ python3 mini_shell.py `

Limitações conhecidas:
* O programa foi desenvolvido e testado em Linux e não funciona em ambiente Windows, pois o Windows, diferentemente de Linux, não tem a chamada fork (ou os.fork, no caso de python).
* A entrada pode ter no máximo 4096 bytes e, portanto, comandos extremamente longos não são aceitos.
