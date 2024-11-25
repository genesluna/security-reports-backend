![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

# 🛡️ Security Reports back-end

API REST para o aplicativo de denúncia de vazamento de dados referente ao projeto integrador VI-B do curso de análise de sistemas do CESMAC.

## 🎯 Objetivo

O objetivo deste projeto é desenvolver uma API RESTful utilizando o framework Django e o DjangoRestFramework, implementando a "Vertical Slices Architecture" para oferecer uma solução robusta, escalável e modular para a gestão de dados em uma aplicação web. Esta API visa não apenas atender às necessidades imediatas de operações CRUD (Create, Read, Update, Delete), mas também proporcionar uma base flexível e extensível que possa ser adaptada e ampliada conforme os requisitos da aplicação evoluem.

Outrossim, o projeto busca explorar e demonstrar as vantagens da "Vertical Slices Architecture" em termos de coesão, isolamento de funcionalidades e facilitação de testes, comparando-a com a arquitetura em camadas tradicional. Um outro objetivo importante é fornecer um ambiente de desenvolvimento que permita a colaboração eficiente entre desenvolvedores, possibilitando o trabalho paralelo em diferentes fatias da aplicação, o que acelera o desenvolvimento e melhora a qualidade do código.

Finalmente, este projeto também tem o objetivo de contribuir para a formação acadêmica, proporcionando uma experiência prática e aplicada dos conceitos teóricos aprendidos na disciplina de back-end, e preparando os estudantes para desafios reais no desenvolvimento de software.

#### Contexto e Relevância

A crescente demanda por aplicações web complexas e escaláveis exige soluções que possam atender a essas necessidades de forma eficiente. A arquitetura de software escolhida para um projeto pode impactar significativamente seu sucesso, influenciando desde a manutenibilidade até a performance e a escalabilidade da aplicação.

#### Fundamentação Teórica

A arquitetura "Vertical Slices" propõe uma organização do código em fatias verticais, onde cada fatia representa uma funcionalidade completa da aplicação. Esta abordagem contrasta com a arquitetura em camadas tradicional, oferecendo benefícios como:

Maior coesão: Cada fatia contém tudo o que é necessário para uma funcionalidade específica, incluindo modelos, serviços e controladores.
Melhor isolamento: Facilita a implementação de mudanças e novas funcionalidades sem impactar outras partes do sistema.
Testabilidade: A separação clara de funcionalidades simplifica a criação de testes unitários e de integração.

O uso do Django e do DjangoRestFramework proporciona uma base sólida para o desenvolvimento de APIs RESTful, aproveitando a robustez e a flexibilidade do Django combinado com as ferramentas especializadas do DjangoRestFramework para a criação de APIs.

#### Impacto e Benefícios

A implementação desta API com a "Vertical Slices Architecture" oferece vários benefícios tangíveis:

Facilidade de manutenção: Mudanças e melhorias podem ser realizadas em uma fatia específica sem afetar outras partes do sistema.
Escalabilidade: A API pode ser expandida de forma modular, adicionando novas funcionalidades como fatias independentes.
Eficiência no desenvolvimento: Equipes podem trabalhar de forma paralela em diferentes fatias, acelerando o desenvolvimento.

## 👨‍💻 Desenvolvimento

#### Planejamento e Design

O desenvolvimento da API RESTful começou com uma fase de planejamento e design, na qual foram definidos os requisitos do projeto e a arquitetura a ser utilizada. Durante essa fase, optou-se pela utilização do Django e do DjangoRestFramework (DRF) devido à sua robustez, flexibilidade e capacidade de facilitar o desenvolvimento de APIs escaláveis e seguras. A "Vertical Slices Architecture" foi escolhida como a abordagem arquitetural para garantir a modularidade e a facilidade de manutenção do código.

#### Implementação dos Vertical Slices

A implementação seguiu a "Vertical Slices Architecture", onde cada fatia vertical representava uma funcionalidade completa do sistema. Cada fatia foi desenvolvida de forma independente, contendo seus próprios modelos, entidades, casos de uso, visualizações, serializers, roteadores, etc. Essa abordagem permitiu que funcionalidades específicas fossem desenvolvidas e testadas de maneira isolada, facilitando a identificação e correção de erros.

Modelagem de Dados: Para cada fatia, foram definidos modelos de dados que representavam as entidades do sistema. Utilizando o ORM (Object-Relational Mapping) do Django, foi possível mapear esses modelos diretamente para tabelas no banco de dados.

Serialização de Dados: Com o DRF, foram criados serializers para converter os dados dos modelos para formatos JSON e vice-versa. Isso permitiu que os dados fossem facilmente transmitidos pela API em um formato padronizado.

Criação de Endpoints: Foram desenvolvidos endpoints específicos para cada caso de uso (Create, Read, Update, Patch, Delete), garantindo que cada fatia tivesse seus próprios pontos de entrada na API.

#### Testes e Validação

A fase de testes foi crucial para garantir a qualidade e a funcionalidade da API. Foram realizados testes unitários, de integração e end-to-end (E2E) para assegurar que cada fatia da API funcionasse corretamente e que o sistema como um todo atendesse aos requisitos de performance e segurança.

- Testes Unitários: Foram criados para cada modelo, serializer, e view, garantindo que cada componente individual funcionasse conforme esperado.

- Testes de Integração: Verificaram a interação entre diferentes componentes da API, assegurando que os dados fluíssem corretamente através do sistema e que todas as dependências fossem resolvidas adequadamente.

- Testes End-to-End (E2E): Esses testes foram realizados para simular o comportamento do aplicativo cliente, testando o sistema de back-end de ponta a ponta.

#### Documentação

A documentação da API foi criada utilizando ferramentas como o Swagger e o DRF-YASG, que permitem a geração automática de documentação a partir do código-fonte. Isso facilitou a compreensão e o uso da API por outros desenvolvedores e usuários finais.

## ⚠️ Alerta

Embora eu conheça um pouco de Pythton, não sou versado em Django. Tenho certeza que alguém especializado no framework vai encontrar várias formas de melhorar o código e os testes. Meu objetivo principal era somente demonstrar que é possível e relativamente fácil seguir outros padrões arquitetônicos em Django além do _default_.

## ⚙️ Instalação

1. Clone este repositório:

   ```bash
   git https://github.com/genesluna/security-reports-backend.git
   cd security-reports-backend
   ```

2. Crie um ambiente virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv/Scripts/Activate.ps1  # Windows Powershell
   ```

3. Atualizar o pip:

   ```bash
    pip install --upgrade pip
   ```

4. Instalar dependências:
   ```bash
    pip install -r requirements.txt
   ```
5. Execute as migrações para criar o banco de dados:

   ```bash
   python manage.py migrate
   ```

6. Crie um superusuário para acessar o Django Admin:

   ```bash
   python manage.py createsuperuser
   ```

7. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```
