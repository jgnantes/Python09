from enum import Enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(Enum):
    """ """
    cadet = 1
    officer = 2
    lieutenant = 3
    captain = 4
    commander = 5


class CrewMember(BaseModel):
    """ """
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    """ """
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_time: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_id(self):
        """ """
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with capital M")
        return self

    @model_validator(mode='after')
    def validate_leadership(self):
        """ """
        for member in self.crew:
            if member.rank in {Rank.commander, Rank.captain}::
                return self
        raise ValueError("Missions must have at least one captain or commander")

    @model_validator(mode='after')
    def validate_crew_size(self):
        """ """
        if self.duration_days > 365:
            experienced_crew: int = 0
            for member in self.crew:
                if member.years_experience >= 5:
                    experienced_crew += 1
            if experienced_crew < (len(self.crew)/2):
                raise ValueError("Missions longer than 1 year must have at least 50% crew members with over 5 years of experience")
        return self

    @model_validator(mode='after')
    def validate_activity(self):
        """ """
        for member in self.crew:
            if not member.is_active:
                raise ValueError("All crew members must be active")
        return self


if __name__ == "__main__":
