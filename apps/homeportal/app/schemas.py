"""Generic or common schemas."""

from typing import Literal

from celery import Task
from pydantic import BaseModel, Field


class CeleryMetaData(BaseModel):
    """
    Metadata model for Celery task execution.

    This Pydantic model holds metadata about the execution of a Celery task,
    including the current state, progress, and results. It is used to update
    task state and provide progress feedback to users.

    Attributes:
        state (str): Current state of the task execution.
        task (str | None): Name of the task being executed.
        current (int): Current progress value (0-100).
        total (Literal[100]): Total progress value (always 100).
        error (str | None): Error message if the task failed.
        result (dict[str, str | int]): Dictionary containing task results.
    """

    state: str = Field(default="Starting...")
    task: str | None = Field(default=None)
    current: int = Field(default=0, ge=0, le=100)
    total: Literal[100] = Field(default=100)
    error: str | None = Field(default=None)
    result: dict[str, str | int] = Field(default={})

    def propagate(self, task: Task) -> None:
        """
        Update the Celery task state with current metadata.

        This method propagates the current metadata to the Celery task,
        allowing progress tracking and state updates to be visible to
        task consumers.

        Args:
            task (Task): The Celery task instance to update.
        """
        task.update_state(state=self.state, meta=self.model_dump())
