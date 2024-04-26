# Projeto disciplina de DataOps

## Projeto final de DataOps, da Faculdade Impacta de Tecnologia, focado para tratamento automatizado de dados para o metadado via Docker.

### Escopo do projeto abaixo:

![](imgs/imagem1.jpeg)

O principal objetivo é estar utilizando o site https://randomuser.me/api/?results=10 para coleta dados.

Para esse trabalho foram criados duas camadas de dados: raw e trusted.

Utilizamos Python para leitura, gravação em raw, transformação e gravação em trusted.

Após a coleta de dados, é feita a transformação e então inserido em uma tabela do MySQL.

Os dados tratados foram caracteres especiais transformação das strings para lowercase (minúsculas).

Durante o processo de ingestão e preparação, utilizamos o "try except" para geração de logs.

Para a visualização dos dados tratados, foi criado um Dockerfile a partir da imagem do MySQL.

    make build: para criar a imagem docker.

    make up: para subir a imagem docker local.

Foi gerado um Docker-Image e gerado um Docker-Compose para a criação do container e a execução da visualização dos dados tratados.

```
dataops04
│ README.md
│ .gitignore
│ .github/workflows
| README.md
| docker-compose.yml
└───imgs
|
└───python
│ | Dockerfile
| └────scripts
│ │ │ ingestion.py
│ │ │ config.py
│ │ │ utils.py
│ │ │ metadado.xlsx
│ └────data
│ │ │ └─── raw
| │ | └─── work
|
└───mysql
│ | Dockerfile
│ └────db
| | | CreateDtabase.sql
```

Integrantes:

Alisson Machado Sousa

Tatiana Fernanda Terra

Daniel Kardec de Santana Oliveira

Fábio Augusto de Lorenzo Tavares

Luis Fernando Joaquim de Sena

Eduardo Vitor Oliveira Cunha
