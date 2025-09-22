# VM---comida-natural
Versão inicial da firmware da vending machine para controle de acesso e escaneamento de produtos via leitor de código de barras.
## Funcionamento do código
  * O código requisita um cartão/tag NFC/RFID ao usuário, caso essa esteja cadastrada, o acesso é liberado, caso contrário, o acesso é negado;
  * O código também solicita o código de barras contido nos produtos cadastrados na máquina para o pagamento, o funcionamento é semelhante ao controle de acesso.

Obs: Visto que o software não existe ainda, a leitura do código de barras e o controle de acesso resultam na liberação da porta, quando o software for implementado, a abertura ocorrerá após o controle de acesso somente.
