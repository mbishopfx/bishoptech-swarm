from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AgentTemplateBase(BaseModel):
    name: str
    system_prompt: str
    default_api: str

class AgentTemplateCreate(AgentTemplateBase):
    pass

class AgentTemplate(AgentTemplateBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class SwarmAgentCreate(BaseModel):
    agent_template_id: int
    sequence_order: int

class SwarmBase(BaseModel):
    name: str
    description: str

class SwarmCreate(SwarmBase):
    agents: List[SwarmAgentCreate]

class Swarm(SwarmBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class KnowledgeBaseBase(BaseModel):
    name: str
    description: Optional[str] = None

class KnowledgeBaseCreate(KnowledgeBaseBase):
    pass

class KnowledgeBase(KnowledgeBaseBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    filename: str
    kb_id: int

class Document(DocumentBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class SwarmRunCreate(BaseModel):
    input_prompt: str
    use_rag: bool = False
    kb_id: Optional[int] = None

class RunLog(BaseModel):
    id: int
    run_id: int
    agent_name: str
    input_context: str
    output: str
    timestamp: datetime
    class Config:
        from_attributes = True

class SwarmRun(BaseModel):
    id: int
    swarm_id: int
    status: str
    input_prompt: str
    final_output: Optional[str]
    use_rag: bool
    kb_id: Optional[int]
    created_at: datetime
    completed_at: Optional[datetime]
    logs: Optional[List[RunLog]] = []
    class Config:
        from_attributes = True
