"""Generic or common schemas."""

from typing import Literal

from celery import Task
from pydantic import BaseModel, Field

class CeleryMetaData(BaseModel):
    """TODO"""

    task: str | None = Field(default=None)
    state: str | None = Field(default=None)
    current: int = Field(default=0, ge=0, le=100)
    total: Literal[100] = Field(default=100)
    error: str | None = Field(default=None)
    result: dict[str, str | int] = Field(default={})

    def propagate(self, task: Task) -> None:
        """TODO"""
        task.update_state(state=self.state, meta=self.model_dump())
