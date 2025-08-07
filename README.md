# Sistema de Suporte Técnico Cisco - Multi-Agent

Uma aplicação inteligente baseada no framework CrewAI que oferece suporte técnico especializado para equipamentos Cisco através de múltiplos agentes especializados.

## 🚀 Características

- **Multi-Agent System**: Utiliza 4 agentes especializados para análise completa
- **Interface Moderna**: Frontend responsivo e intuitivo
- **Análise Inteligente**: Diagnóstico baseado em IA para problemas Cisco
- **Especialização**: Agentes focados em rede, hardware, configuração e coordenação
- **API RESTful**: Backend robusto com FastAPI

## 🤖 Agentes Especializados

### 1. Analista de Rede Cisco
- **Especialidade**: Problemas de conectividade e configuração de rede
- **Foco**: Protocolos de roteamento, switching, troubleshooting
- **Saída**: Análise de conectividade e comandos de diagnóstico

### 2. Especialista em Hardware Cisco
- **Especialidade**: Problemas físicos e de hardware
- **Foco**: Componentes internos, LEDs, fontes de alimentação
- **Saída**: Diagnóstico de hardware e verificações físicas

### 3. Especialista em Configuração Cisco
- **Especialidade**: Problemas de configuração
- **Foco**: IOS, IOS-XE, NX-OS, comandos de configuração
- **Saída**: Análise de configurações e correções sugeridas

### 4. Coordenador de Suporte Técnico
- **Especialidade**: Consolidação e coordenação
- **Foco**: Análise de relatórios e recomendações finais
- **Saída**: Resumo executivo e recomendações consolidadas

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **FastAPI**: Framework web moderno e rápido
- **CrewAI**: Framework para sistemas multi-agente
- **LangChain**: Integração com modelos de linguagem
- **OpenAI GPT-4**: Modelo de linguagem para análise

### Frontend
- **HTML5/CSS3**: Interface responsiva
- **JavaScript**: Interatividade e comunicação com API
- **Font Awesome**: Ícones modernos
- **Design System**: Interface consistente e profissional

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Chave de API da OpenAI
- Navegador web moderno

## 🔧 Instalação

1. **Clone o repositório**:
```bash
git clone <repository-url>
cd cisco-support-app
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**:
```bash
# Crie um arquivo .env na raiz do projeto
echo "OPENAI_API_KEY=sua_chave_api_aqui" > .env
```

4. **Execute o servidor backend**:
```bash
cd backend
python main.py
```

5. **Abra o frontend**:
```bash
# Abra o arquivo frontend/index.html no seu navegador
# Ou use um servidor local simples:
python -m http.server 8080
# Depois acesse: http://localhost:8080/frontend/
```

## 🚀 Como Usar

1. **Acesse a interface web** no navegador
2. **Preencha o formulário** com:
   - Descrição detalhada do problema
   - Modelo do equipamento Cisco
   - Mensagens de erro (se houver)
   - Configuração de rede (se disponível)
3. **Clique em "Analisar Problema"**
4. **Aguarde a análise** dos agentes especializados
5. **Revise os resultados**:
   - Resumo da análise
   - Possíveis causas
   - Soluções recomendadas
   - Análises individuais dos especialistas
   - Recomendação final

## 📁 Estrutura do Projeto

```
cisco-support-app/
├── backend/
│   └── main.py              # Servidor FastAPI principal
├── frontend/
│   └── index.html           # Interface web
├── requirements.txt         # Dependências Python
├── .env                     # Variáveis de ambiente
└── README.md               # Documentação
```

## 🔌 Endpoints da API

### POST /analyze-problem
Analisa um problema técnico usando o sistema multi-agente.

**Request Body**:
```json
{
  "problem_description": "string",
  "equipment_model": "string (opcional)",
  "error_messages": "string (opcional)",
  "network_config": "string (opcional)"
}
```

**Response**:
```json
{
  "problem_analysis": "string",
  "possible_causes": ["string"],
  "solutions": ["string"],
  "agent_responses": [
    {
      "agent_name": "string",
      "reasoning": "string",
      "findings": ["string"],
      "recommendations": ["string"]
    }
  ],
  "final_recommendation": "string"
}
```

### GET /health
Verifica o status do servidor.

## 🎯 Exemplos de Uso

### Problema de Conectividade
```
Descrição: "O switch não está permitindo comunicação entre VLANs"
Modelo: "Cisco Catalyst 2960"
Erros: "VLAN 10 cannot communicate with VLAN 20"
```

### Problema de Hardware
```
Descrição: "O roteador não está ligando, LED de power piscando"
Modelo: "Cisco ASR 1000"
Erros: "Power supply failure detected"
```

### Problema de Configuração
```
Descrição: "ACLs estão bloqueando tráfego legítimo"
Modelo: "Cisco ISR 4321"
Config: "show running-config output"
```

## 🔒 Configuração de Segurança

- Configure CORS adequadamente para produção
- Use HTTPS em ambiente de produção
- Implemente autenticação se necessário
- Proteja sua chave de API da OpenAI

## 🚧 Desenvolvimento

### Adicionando Novos Agentes

1. Crie uma nova função de agente em `main.py`
2. Defina o role, goal e backstory
3. Crie uma nova Task para o agente
4. Adicione o agente à Crew

### Personalizando a Interface

- Modifique o CSS em `frontend/index.html`
- Adicione novos campos no formulário
- Implemente novas visualizações de dados

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para suporte técnico ou dúvidas sobre o projeto, abra uma issue no repositório.

---

**Desenvolvido com ❤️ para a comunidade de redes Cisco**
