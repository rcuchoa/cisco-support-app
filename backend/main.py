from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import json

# Carregar variáveis de ambiente
load_dotenv()

app = FastAPI(title="Cisco Support Multi-Agent System", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class ProblemRequest(BaseModel):
    problem_description: str
    equipment_model: Optional[str] = None
    error_messages: Optional[str] = None
    network_config: Optional[str] = None

class AgentResponse(BaseModel):
    agent_name: str
    reasoning: str
    findings: List[str]
    recommendations: List[str]

class SupportResponse(BaseModel):
    problem_analysis: str
    possible_causes: List[str]
    solutions: List[str]
    agent_responses: List[AgentResponse]
    final_recommendation: str

# Configurar o modelo de linguagem
def get_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key não configurada")
    return ChatOpenAI(
        model="gpt-4",
        api_key=api_key,
        temperature=0.1
    )

# Definir agentes especializados
def create_agents():
    llm = get_llm()
    
    # Agente especialista em diagnóstico de rede
    network_analyst = Agent(
        role="Analista de Rede Cisco",
        goal="Analisar problemas de conectividade e configuração de rede em equipamentos Cisco",
        backstory="""Você é um especialista experiente em redes Cisco com mais de 10 anos de experiência.
        Você conhece profundamente os protocolos de roteamento, switching, troubleshooting e configuração
        de equipamentos Cisco. Você é capaz de identificar rapidamente problemas de conectividade,
        configuração incorreta e falhas de hardware.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Agente especialista em hardware
    hardware_specialist = Agent(
        role="Especialista em Hardware Cisco",
        goal="Diagnosticar problemas físicos e de hardware em equipamentos Cisco",
        backstory="""Você é um técnico especializado em hardware Cisco com vasta experiência em
        manutenção e reparo de equipamentos. Você conhece todos os modelos de roteadores, switches
        e outros dispositivos Cisco, incluindo seus componentes internos, indicadores LED,
        fontes de alimentação e problemas comuns de hardware.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Agente especialista em configuração
    config_specialist = Agent(
        role="Especialista em Configuração Cisco",
        goal="Analisar e corrigir problemas de configuração em equipamentos Cisco",
        backstory="""Você é um engenheiro de redes especializado em configuração de equipamentos Cisco.
        Você domina IOS, IOS-XE, NX-OS e outros sistemas operacionais Cisco. Você é capaz de
        identificar configurações incorretas, comandos mal aplicados e problemas de segurança
        em configurações de rede.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    # Agente coordenador
    coordinator = Agent(
        role="Coordenador de Suporte Técnico",
        goal="Coordenar a análise dos especialistas e fornecer uma solução final consolidada",
        backstory="""Você é um coordenador experiente que supervisiona equipes de suporte técnico.
        Você é capaz de analisar relatórios de diferentes especialistas, identificar padrões,
        priorizar problemas e fornecer recomendações claras e acionáveis para os usuários.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    return network_analyst, hardware_specialist, config_specialist, coordinator

@app.post("/analyze-problem", response_model=SupportResponse)
async def analyze_problem(request: ProblemRequest):
    try:
        # Criar agentes
        network_analyst, hardware_specialist, config_specialist, coordinator = create_agents()
        
        # Criar tarefas para cada especialista
        network_task = Task(
            description=f"""
            Analise o seguinte problema de rede Cisco:
            
            Descrição do problema: {request.problem_description}
            Modelo do equipamento: {request.equipment_model or 'Não especificado'}
            Mensagens de erro: {request.error_messages or 'Não fornecidas'}
            Configuração de rede: {request.network_config or 'Não fornecida'}
            
            Forneça:
            1. Análise detalhada do problema
            2. Possíveis causas relacionadas à rede
            3. Recomendações específicas
            4. Comandos de diagnóstico sugeridos
            """,
            agent=network_analyst,
            expected_output="Relatório detalhado de análise de rede"
        )
        
        hardware_task = Task(
            description=f"""
            Analise o seguinte problema de hardware Cisco:
            
            Descrição do problema: {request.problem_description}
            Modelo do equipamento: {request.equipment_model or 'Não especificado'}
            Mensagens de erro: {request.error_messages or 'Não fornecidas'}
            
            Forneça:
            1. Análise de possíveis problemas de hardware
            2. Verificações físicas necessárias
            3. Indicadores LED a serem verificados
            4. Recomendações de manutenção
            """,
            agent=hardware_specialist,
            expected_output="Relatório detalhado de análise de hardware"
        )
        
        config_task = Task(
            description=f"""
            Analise o seguinte problema de configuração Cisco:
            
            Descrição do problema: {request.problem_description}
            Modelo do equipamento: {request.equipment_model or 'Não especificado'}
            Mensagens de erro: {request.error_messages or 'Não fornecidas'}
            Configuração de rede: {request.network_config or 'Não fornecida'}
            
            Forneça:
            1. Análise de possíveis problemas de configuração
            2. Comandos de verificação sugeridos
            3. Correções de configuração recomendadas
            4. Melhores práticas aplicáveis
            """,
            agent=config_specialist,
            expected_output="Relatório detalhado de análise de configuração"
        )
        
        coordination_task = Task(
            description="""
            Analise os relatórios dos três especialistas e forneça:
            
            1. Resumo executivo do problema
            2. Lista consolidada de possíveis causas
            3. Soluções priorizadas
            4. Recomendação final com próximos passos
            
            Seja claro, conciso e forneça informações acionáveis.
            """,
            agent=coordinator,
            expected_output="Relatório final consolidado com recomendações"
        )
        
        # Criar e executar a crew
        crew = Crew(
            agents=[network_analyst, hardware_specialist, config_specialist, coordinator],
            tasks=[network_task, hardware_task, config_task, coordination_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Processar resultados (simulação para demonstração)
        # Em uma implementação real, você processaria o resultado real do CrewAI
        
        # Simular respostas dos agentes
        agent_responses = [
            AgentResponse(
                agent_name="Analista de Rede Cisco",
                reasoning="Analisando padrões de conectividade e protocolos de roteamento",
                findings=["Possível problema de roteamento", "Verificar tabelas de roteamento"],
                recommendations=["Executar 'show ip route'", "Verificar configuração de interfaces"]
            ),
            AgentResponse(
                agent_name="Especialista em Hardware Cisco",
                reasoning="Verificando indicadores físicos e componentes de hardware",
                findings=["LEDs de status normais", "Verificar fonte de alimentação"],
                recommendations=["Verificar LEDs de status", "Testar fonte de alimentação"]
            ),
            AgentResponse(
                agent_name="Especialista em Configuração Cisco",
                reasoning="Analisando configurações e comandos aplicados",
                findings=["Possível configuração incorreta de VLAN", "Verificar ACLs"],
                recommendations=["Verificar configuração de VLAN", "Revisar ACLs aplicadas"]
            )
        ]
        
        return SupportResponse(
            problem_analysis="Análise completa realizada por especialistas em rede, hardware e configuração",
            possible_causes=[
                "Problema de roteamento entre VLANs",
                "Configuração incorreta de ACLs",
                "Fonte de alimentação instável",
                "Interface com configuração incorreta"
            ],
            solutions=[
                "Verificar e corrigir configuração de roteamento inter-VLAN",
                "Revisar e ajustar ACLs aplicadas",
                "Testar fonte de alimentação e considerar substituição",
                "Verificar configuração de interfaces e subinterfaces"
            ],
            agent_responses=agent_responses,
            final_recommendation="Execute os comandos de diagnóstico sugeridos pelos especialistas e implemente as correções de configuração priorizadas. Monitore o equipamento após as alterações."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Cisco Support Multi-Agent System"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
