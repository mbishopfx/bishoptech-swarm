from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class AgentTemplate(Base):
    __tablename__ = "agent_templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    system_prompt = Column(Text)
    default_api = Column(String) # "xAI" or "Gemini"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Swarm(Base):
    __tablename__ = "swarms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SwarmAgent(Base):
    __tablename__ = "swarm_agents"
    id = Column(Integer, primary_key=True, index=True)
    swarm_id = Column(Integer, ForeignKey("swarms.id"))
    agent_template_id = Column(Integer, ForeignKey("agent_templates.id"))
    sequence_order = Column(Integer)
    
    agent_template = relationship("AgentTemplate")

class KnowledgeBase(Base):
    __tablename__ = "knowledge_bases"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    documents = relationship("Document", back_populates="knowledge_base", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    kb_id = Column(Integer, ForeignKey("knowledge_bases.id"))
    filename = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    knowledge_base = relationship("KnowledgeBase", back_populates="documents")

class SwarmRun(Base):
    __tablename__ = "swarm_runs"
    id = Column(Integer, primary_key=True, index=True)
    swarm_id = Column(Integer, ForeignKey("swarms.id"))
    status = Column(String, default="pending") # pending, running, completed, failed
    input_prompt = Column(Text)
    final_output = Column(Text, nullable=True)
    use_rag = Column(Boolean, default=False)
    kb_id = Column(Integer, ForeignKey("knowledge_bases.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

class RunLog(Base):
    __tablename__ = "run_logs"
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("swarm_runs.id"))
    agent_name = Column(String)
    input_context = Column(Text)
    output = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("swarm_runs.id"))
    role = Column(String) # user or assistant
    content = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
