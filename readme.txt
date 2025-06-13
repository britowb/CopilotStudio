Foi criado um novo agente em branco. 
	Descrição: Esse agente servirá para gerenciar operações bancárias com sistema de login baseado em planilhas. Atualizarei o sistema bancário em POO para criar endpoints REST. 
	Resposta generativa habilitada, GPT-4o. 
 Instruções gerais 
  O Agente se entenderá como um secretário do sistema bancário. Será responsável por manipular e validar dados localizados no planilhas através de respostas generativas direcionadas.



Registrei um novo aplicativo no Microsoft Azure AD (IAM), BancoGraphAPI.
Obtidas as identificações que serão usadas para autenticar e gerar token que autorizam as calls à Microsoft Graph API.
	Microsoft Graph API irá nos permitir fazer CRUD através de métodos HTTP nas planilhas.
		CRUD - Create, Read, Update, Delete. 
			POST é usado para criar
			GET para ler
			PUT/PATCH atualiza
			DELETE exclui dados.

BancoGraphAPI -
	Controle de acesso: Qualquer um com conta Microsoft ou corporativa poderá acessar. 
	Tenho como objetivo fazer uma autenticação da conta.
	Associaremos o ID da conta autenticada com o CPF para verificar as permissões antes de qualquer manipulação/acesso de dados.
	Limitações: Acessar o próprio CPF.

Library MSAL - Para receber tokens de acesso usando a partir das credenciais fornecidas pelo aplicativo BancoGraphAPI.
	CLIENT_ID
	CLIENT_SECRET
	TENANT_ID
 Responsável por validar chamadas ao Graph API.


Criamos um arquivo .env para armazenar variáveis de ambiente como chaves API ou config de database.
  Mantém configs do projeto separadas do código.

	import OS - lib para acessar var de ambiente, como as salvas no arquivo .env (não confundir com .venv)

	from flask import flask - importa flask para criar a aplicação web

	from dotenv import load_dotenv - permite carregar as var definidas no arquivo .env, evitando inserir dados sensiveis no código.
		load_dotenv()  procura um arquivo .env na raíz do projeto e carrega suas var para serem acessadas por os.getenv()

Uma vez configurado o .env descobri precisar dar permissões de API para a aplicação BancoGraphAPI.
	BancoGraphAPI >> Gerenciar >> Permissões de APIs >> Microsoft Graph API >> Solicitar permissões de API >> Files.ReadWrite.All and Sites.Read.All
	Selecionei as permissões em questão e dei consentimento do admnistrador.
	Configuramos então a autorização de acesso e manipulação de arquivos no OneDrive.

Foi impossível configurar o OneDrive por falta de assinatura. Utilizaremos o PowerApps. Não mais utilizaremos o Microsoft Graph
Nossa API Rest irá manipular os registros na tabela através do DataVerse.

Tenant do Azure AD: permitindo todos tipos de conta.

Criemos duas tabelas no PowerApps:
	
	Contas, Transacoes
		Contas:
			TabelaContas: CPF, Nome, Saldo, UserObjectID     [ PESQUISÁVEL ]
		Transacoes:
			TabelaTransporte: CPF, Data/Hora, Tipo, Valor, SaldoFim

UserObjectID irá armazenar o token (oid), permitindo gerenciar a conexão

Usaremos endpoints OData no lugar de Microsoft Graph.
Trocado o nome da API "BancoGraphAPI" para "BancoDataVerseAPI" afim de evitar confusões.

 	Minha API Rest consultará os dados da tabela no Dataverse usando o Web API (também conhecido como Common Data Service Web API).
	A API fará operações GET, POST, PATCH, DELETE no registro das entidades através de endpoints OData.
	BancoDataVerseAPI requer permissões de "user_impersonation" para a API do Dynamics CRM (Dataverse).
		Autoriza o aplicativo a chamar o Web API do Dataverse (com URL base do tipo https://<YOUR_ORG>.crm.dynamics.com/api/data/v9.2/) em nome do usuário.
		Garante o acesso aos dados em nome do user, permitindo o PowerApps(ou a API que consome o DataVerse) ter o acesso necessário para realizar operações
			Consultas; inserções; atualizações; exclusões: Diretamente no Dataverse
		Concedido consentimento admnistrativo.








	



 



