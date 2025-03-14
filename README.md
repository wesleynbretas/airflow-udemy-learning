# Domine Apache Airflow - Repositório de Estudos

Este repositório contém meus estudos e implementações baseadas no curso [Domine Apache Airflow](https://www.udemy.com/course/domine-apache-airflow) da Udemy. Aqui você encontrará DAGs, exemplos práticos, configurações e insights adquiridos durante o aprendizado.

## Tecnologias Utilizadas

- **Apache Airflow** - Orquestração de workflows
- **Docker & Docker Compose** - Ambientes isolados e fácil deploy
- **Python** - Linguagem principal para as DAGs
- **PostgreSQL** - Banco de dados backend do Airflow

## Estrutura do Repositório

```
/
|-- dags/                   # DAGs implementadas
|-- plugins/                # Plugins personalizados
|-- config/                 # Configurações do Airflow
|-- docker-compose.yml      # Configuração para execução com Docker
|-- requirements.txt        # Dependências do projeto
|-- README.md               # Documentação do projeto
```

## Como Executar o Projeto

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

### 2. Configurar e Subir o Airflow com Docker
```bash
export AIRFLOW_UID=$(id -u)
docker-compose up -d
```

### 3. Acessar a Interface Web do Airflow
Acesse no navegador:
```
http://localhost:8080
```
Usuário padrão: `airflow`
Senha padrão: `airflow`

## Aprendizados e Implementações

- **Configuração do ambiente**: Utilização do Docker para facilitar a instalação.
- **Criação de DAGs**: Pipelines de dados automatizados.
- **Integração com APIs e bancos**: Extração e carga de dados.
- **Uso de Operators personalizados**: Automatização de tarefas complexas.

## Referências

- [Curso Domine Apache Airflow](https://www.udemy.com/course/domine-apache-airflow)
- [Documentação Oficial do Apache Airflow](https://airflow.apache.org/)

🚀 Let's coding

