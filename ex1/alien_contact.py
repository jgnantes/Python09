from enum import Enum
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, model_validator

class ContactType(Enum):
    """ """
    radio = 1
    visual = 2
    physical = 3
    telepathic = 4


class AlienContact(BaseModel):
    """ """
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=300)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=200)
    is_verified: bool =  Field(default=False)

    @model_validator(mode='after')
    def validate_id(self):
        """ """
        if not self.contact_id.startswith("AC"):
            raise ValueError("ID must start with 'AC'")
        return self

    @model_validator(mode='after')
    def validate_physical(self):
        """ """
        if (self.contact_type == ContactType.physical
        and not self.is_verified):
            raise ValueError("Physical contacts must be verified")
        return self

    @model_validator(mode='after')
    def validate_telepathic(self):
        """ """
        if (self.contact_type == ContactType.telepathic
        and self.witness_count < 3):
            raise ValueError(
                "Telepathic contacts must have at least 3 witnesses")
        return self

    @model_validator(mode='after')
    def validate_strong_signal_messages(self):
        """ """
        if (self.signal_strength > 7.0
        and (self.message_received is None 
        or len(self.message_received) == 0)):
            raise ValueError(
                "Contacts w/ Signal Strength above 7 must contain a message")
        return self


if __name__ == "__main__":
    ac1 = AlienContact(
        contact_id= "AC_2024_001",
        timestamp = datetime.now(),
        contact_type=ContactType(1),
        location="Area 51, Nevada",
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
    )
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    print(f"ID: {ac1.contact_id}")
    print(f"Type: {ac1.contact_type.name}")
    print(f"Location: {ac1.location}")
    print(f"Signal: {ac1.signal_strength}/10")
    print(f"Duration: {ac1.duration_minutes} minutes")
    print(f"Witnesses: {ac1.witness_count}")
    print(f"Message: '{ac1.message_received}'")

    print("\n======================================")
    print("Expected validation error:")
    try:
        ac1 = AlienContact(
            contact_id= "AC_2024_001",
            timestamp = datetime.now(),
            contact_type=ContactType(4),
            location="sei la meo",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received=""
        )
    except ValidationError as e:
        print(e)
