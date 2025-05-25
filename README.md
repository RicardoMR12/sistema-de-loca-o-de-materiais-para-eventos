# Sistema de locação de materiais para eventos
[![NPM](https://img.shields.io/npm/l/react)](https://github.com/devsuperior/sds1-wmazoni/blob/master/LICENSE) 

# Sobre o projeto

Sistema de locação de materiais e um sistema com objetivo de auxiliar a organização e controle de estoque de uma locadora de materiais para eventos.

A aplicação foi criada primeiramente para ser usada como trabalho de faculdade, mas diante de um trabalho que persiste na vida real na organização de controle de estoque de uma empresa ele será continuada.

## Layout web
![Login](https://github.com/user-attachments/assets/65980797-49b8-4cde-85fb-d3ba8d8ad61d)

![Criacao](https://github.com/user-attachments/assets/f5be0c03-7c71-487b-895f-388366974627)

![Redefinir](https://github.com/user-attachments/assets/a6a6393c-25d0-4062-911e-0f225ca67616)

![Locacao](https://github.com/user-attachments/assets/76a4941f-ae18-43f8-a811-b2bfb70ee69d)

![Relatorio](https://github.com/user-attachments/assets/2c069964-ac73-44a3-9cb1-0cf36110d082)

![Adicacao](https://github.com/user-attachments/assets/3be70c68-9550-45c9-b354-49a593f723ee)

# Tecnologias utilizadas
## Back end
- Python
- Flask
  
## Front end
- HTML 
- CSS

## Banco de Dados
- SQLite
- SQLAlchemy

# Como executar o projeto

## Back end
Pré-requisitos recomendados:
- VsCode
- Python extension
- SqLite

```bash
# Clonar repositório
https://github.com/RicardoMR12/sistema-de-loca-o-de-materiais-para-eventos

# Entrar no console do projeto back end do arquivo .py
## Colar instalavel obrigatório:
"pip install flask flask_sqlalchemy"

# Executar o projeto
## Colar comando no console:
"python *NomeDoArquivo*.py"
#Apertar enter e entra no servidor local:
http://127.0.0.1:5000

# Abrir banco de dados
## Assim que executado a primeira vez o "database.db" será criado

# Como abrir o banco de dados primeira maneira 
Abrir o console do projeto e colar:
"python access_db.py"

# Como abrir o banco de dados segunda maneira
- Abrir o DB Browser for SQLite
- Abrir por meio do OpenDatabase a pasta do arquivo do sistema
- Abrir a pasta "instance" e abrir o arquivo "database"
- Os arquivos do sistema do banco de dados estarão em "Browse Data"

# Finalizar servidor
Apertar Ctrl + C

# Observação:
Para abrir a aba "Adicionar material", precisa botar o a senha "0987admin", sendo possivel
altera-la no arquivo "locacao.html" no código "const senhaCorreta = "0987admin";" na linha 64


# Autor

Ricardo Martins Ribeiro
https://www.linkedin.com/in/ricardo-martins-dev/


