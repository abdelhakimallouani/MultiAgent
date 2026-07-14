from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.agent import Agent
from app.schemas.agent import (
    AgentCreate,
    AgentUpdate,
    AgentResponse
)

router = APIRouter()

@router.post(
    "/",
    response_model=AgentResponse
)
def create_agent(
    agent: AgentCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Agent).filter(
        Agent.name == agent.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Agent already exists"
        )

    new_agent = Agent(**agent.dict())

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return new_agent

@router.get(
    "/",
    response_model=list[AgentResponse]
)
def get_agents(
    db: Session = Depends(get_db)
):
    return db.query(Agent).all()

@router.get(
    "/{agent_id}",
    response_model=AgentResponse
)
def get_agent(
    agent_id: int,
    db: Session = Depends(get_db)
):

    agent = db.query(Agent).filter(
        Agent.id == agent_id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    return agent

@router.put(
    "/{agent_id}",
    response_model=AgentResponse
)
def update_agent(
    agent_id: int,
    data: AgentUpdate,
    db: Session = Depends(get_db)
):

    agent = db.query(Agent).filter(
        Agent.id == agent_id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    update_data = data.dict(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(agent, key, value)

    db.commit()
    db.refresh(agent)

    return agent

@router.delete("/{agent_id}")
def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db)
):

    agent = db.query(Agent).filter(
        Agent.id == agent_id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    db.delete(agent)
    db.commit()

    return {
        "message": "Agent deleted successfully"
    }
    
@router.patch(
    "/{agent_id}/status")


def change_status(
    agent_id: int,
    db: Session = Depends(get_db)
):

    agent = db.query(Agent).filter(
        Agent.id == agent_id
    ).first()

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    agent.is_active = not agent.is_active

    db.commit()
    db.refresh(agent)

    return {
        "id": agent.id,
        "name": agent.name,
        "is_active": agent.is_active
    }