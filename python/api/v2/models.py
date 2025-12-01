"""
Pydantic models for API v2 request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

# ============= Enums =============

class PersonaDomain(str, Enum):
    GENERAL = "general"
    ROBOTICS = "robotics"
    FINANCE = "finance"
    ENGINEERING = "engineering"
    MARKETING = "marketing"
    RESEARCH = "research"

class MemoryStrategy(str, Enum):
    FULL = "full"
    SUMMARIZED = "summarized"
    SELECTIVE = "selective"

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

# ============= Persona Models =============

class PersonaTraits(BaseModel):
    """Personality traits configuration (0-100 scale)"""
    formality: int = Field(50, ge=0, le=100, description="Casual (0) to Formal (100)")
    verbosity: int = Field(50, ge=0, le=100, description="Concise (0) to Verbose (100)")
    creativity: int = Field(50, ge=0, le=100, description="Analytical (0) to Creative (100)")
    empathy: int = Field(50, ge=0, le=100, description="Direct (0) to Empathetic (100)")
    humor: int = Field(50, ge=0, le=100, description="Serious (0) to Humorous (100)")

class PersonaBehavior(BaseModel):
    """Behavior configuration for persona"""
    greeting: str = Field("Hello! How can I help you today?", max_length=500)
    style: str = Field("professional and helpful", max_length=200)
    constraints: List[str] = Field(default_factory=list)
    preferences: List[str] = Field(default_factory=list)

class PersonaConfig(BaseModel):
    """System configuration for persona"""
    temperature: float = Field(0.7, ge=0, le=2)
    max_tokens: int = Field(2000, ge=100, le=8000)
    tools_enabled: List[str] = Field(default_factory=lambda: ["all"])
    memory_strategy: MemoryStrategy = MemoryStrategy.FULL

class PersonaCreate(BaseModel):
    """Request model for creating a persona"""
    name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=200)
    expertise: List[str] = Field(default_factory=list)
    avatar: Optional[str] = None
    traits: PersonaTraits = Field(default_factory=PersonaTraits)
    behavior: PersonaBehavior = Field(default_factory=PersonaBehavior)
    config: PersonaConfig = Field(default_factory=PersonaConfig)
    domain: PersonaDomain = PersonaDomain.GENERAL
    custom_instructions: Optional[str] = None

class PersonaUpdate(BaseModel):
    """Request model for updating a persona"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[str] = None
    expertise: Optional[List[str]] = None
    avatar: Optional[str] = None
    traits: Optional[PersonaTraits] = None
    behavior: Optional[PersonaBehavior] = None
    config: Optional[PersonaConfig] = None
    domain: Optional[PersonaDomain] = None
    custom_instructions: Optional[str] = None

class PersonaResponse(BaseModel):
    """Response model for persona"""
    id: str
    name: str
    role: str
    expertise: List[str]
    avatar: Optional[str]
    traits: PersonaTraits
    behavior: PersonaBehavior
    config: PersonaConfig
    domain: PersonaDomain
    custom_instructions: Optional[str]
    created_at: datetime
    updated_at: datetime
    user_id: str

# ============= Agent Models =============

class AgentCreate(BaseModel):
    """Request model for creating an agent"""
    name: str = Field(..., min_length=1, max_length=100)
    persona_id: str
    project_id: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)

class AgentUpdate(BaseModel):
    """Request model for updating an agent"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    persona_id: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

class AgentExecuteRequest(BaseModel):
    """Request model for executing agent task"""
    message: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None
    stream: bool = True
    context: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    """Response model for agent"""
    id: str
    name: str
    persona_id: str
    project_id: Optional[str]
    status: str
    config: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    user_id: str

# ============= Conversation Models =============

class Message(BaseModel):
    """Message in a conversation"""
    role: MessageRole
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

class ConversationCreate(BaseModel):
    """Request model for creating a conversation"""
    agent_id: str
    title: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ConversationUpdate(BaseModel):
    """Request model for updating a conversation"""
    title: Optional[str] = None
    archived: Optional[bool] = None

class ConversationResponse(BaseModel):
    """Response model for conversation"""
    id: str
    agent_id: str
    title: str
    messages: List[Message]
    context: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    archived: bool
    user_id: str

# ============= Memory Models =============

class MemoryCreate(BaseModel):
    """Request model for creating memory"""
    content: str = Field(..., min_length=1)
    type: str = Field("fragment", pattern="^(fragment|solution|fact)$")
    metadata: Optional[Dict[str, Any]] = None
    agent_id: Optional[str] = None

class MemorySearch(BaseModel):
    """Request model for memory search"""
    query: str = Field(..., min_length=1)
    limit: int = Field(10, ge=1, le=100)
    agent_id: Optional[str] = None
    type: Optional[str] = None

class MemoryResponse(BaseModel):
    """Response model for memory"""
    id: str
    content: str
    type: str
    metadata: Dict[str, Any]
    agent_id: Optional[str]
    relevance_score: Optional[float] = None
    created_at: datetime
    user_id: str

# ============= Analytics Models =============

class UsageStats(BaseModel):
    """Usage statistics"""
    total_messages: int
    total_tokens: int
    total_cost: float
    avg_response_time: float
    success_rate: float

class AnalyticsResponse(BaseModel):
    """Analytics response"""
    period: str
    usage: UsageStats
    top_agents: List[Dict[str, Any]]
    top_tools: List[Dict[str, Any]]
    cost_breakdown: Dict[str, float]

# ============= Auth Models =============

class UserRegister(BaseModel):
    """User registration request"""
    email: str = Field(..., regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    password: str = Field(..., min_length=8, max_length=100)
    name: str = Field(..., min_length=1, max_length=100)

class UserLogin(BaseModel):
    """User login request"""
    email: str
    password: str

class TokenResponse(BaseModel):
    """Authentication token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class UserResponse(BaseModel):
    """User profile response"""
    id: str
    email: str
    name: str
    created_at: datetime
    subscription_tier: str = "free"
