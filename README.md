🛰️ FastAPI S3 Versioning Manager
Este projeto é uma API robusta desenvolvida para gerenciar o ciclo de vida de arquivos em um bucket Amazon S3, utilizando FastAPI e a biblioteca Boto3. O sistema foca em integridade de dados através de versionamento automático, permitindo restaurar versões anteriores e auditar mudanças.

Para facilitar o desenvolvimento e testes, o ambiente é totalmente containerizado com Docker e utiliza o LocalStack para simular os serviços da AWS localmente.

🚀 Funcionalidades
Upload de Arquivos: Salva arquivos no S3 gerando IDs de versão únicos.

Listagem de Versões: Exibe o histórico completo de alterações de um arquivo.

Restore (Restauração): Promove uma versão antiga para ser a atual (IsLatest) sem perder o histórico.

Delete Logico: Suporte a Delete Markers, permitindo recuperar arquivos excluídos por acidente.

Auditoria Automatizada: Endpoint que compara a versão atual com a anterior, analisando tamanho e tempo entre modificações.

🛠️ Tecnologias Utilizadas
Python 3.12

FastAPI: Framework web de alta performance.

Boto3: SDK oficial da AWS para Python.

Docker & Docker Compose: Isolamento de ambiente e orquestração.

LocalStack: Simulação de serviços AWS (S3).

📂 Estrutura do Projeto
Plaintext
.
├── routes/
│   └── routes.py      # Definição dos endpoints (APIRouter)
├── services/
│   ├── s3_service.py  # Lógica de interação com AWS S3
│   └── audit.py       # Lógica de análise e auditoria de dados
├── main.py            # Ponto de entrada da aplicação
├── Dockerfile         # Configuração da imagem Docker da API
├── docker-compose.yml # Orquestração da API + LocalStack
└── requirements.txt   # Dependências do projeto

🔧 Como Rodar o Projeto
Pré-requisitos
Docker e Docker Compose instalados.

Passo a Passo
Clone o repositório:

Bash
git clone https://github.com/seu-usuario/fastapi-s3-manager.git
cd fastapi-s3-manager
Suba os containers:

Bash
docker-compose up -d
Isso iniciará a API na porta 8000 e o LocalStack na porta 4566.

Acesse a Documentação (Swagger):
Abra o navegador em: http://localhost:8000/docs