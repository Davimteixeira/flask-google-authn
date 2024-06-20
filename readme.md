### Exemplo de autenticação hospedada pelo Google no Flask

Objetivo: demonstrar como usar o Google para lidar com a autenticação do usuário (authN) para um aplicativo da web de balão de demonstração.

Para executar este aplicativo, execute cmd: `docker-compose build` e depois `docker-compose up` (certifique-se de instalar o Docker localmente primeiro!)

Credit: https://www.youtube.com/watch?v=FKgJEfrhU1E 

Para configurar isso com sua conta do Google (do serviço):
* https://console.cloud.google.com/ 
* Registre um serviço no Google > crie um novo projeto (nomeie-o). 
*Dentro do novo projeto, vá para APIs + Serviços > Criar credenciais > Configurar tela de consentimento > Usuários externos > nomeie o projeto novamente (o mesmo nome está ok) > insira o e-mail de suporte ao usuário > deixe os padrões > crie usuários de teste se desejar 
*Volte para painel > Credenciais > Criar credenciais > ID do cliente OAuth > aplicativo web > defina o URL de redirecionamento do seu aplicativo web (http://localhost/callback)
*Crie o retorno de chamada> baixe seus créditos como um arquivo json 
*Copie este `client_secret.json` localmente para o repositório do projeto
*Atualize o `GOOGLE_CLIENT_ID` em `app.py` com o que está presente no client_secret.json que você obteve do Google.
 
