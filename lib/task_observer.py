"""Task-Observer pattern: async task tracking with observer notifications.

Provides a TaskManager singleton for creating, tracking, and observing
long-running operations in the Streamlit portal. UI components subscribe
to task state changes and receive progress updates.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    """A trackable unit of work with progress and result."""

    name: str
    status: TaskStatus = TaskStatus.PENDING
    progress: float = 0.0  # 0.0 to 1.0
    message: str = ""
    result: Any = None
    error: str | None = None
    created_at: float = field(default_factory=time.time)
    started_at: float | None = None
    completed_at: float | None = None
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    @property
    def duration(self) -> float | None:
        if self.started_at is None:
            return None
        end = self.completed_at or time.time()
        return round(end - self.started_at, 2)

    @property
    def elapsed(self) -> float:
        start = self.started_at or self.created_at
        return round(time.time() - start, 2)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "progress": self.progress,
            "message": self.message,
            "error": self.error,
            "duration": self.duration,
            "created_at": datetime.fromtimestamp(self.created_at).isoformat(),
        }


ObserverCallback = Callable[[Task], None]


class TaskObserver:
    """Simple observer pattern — subscribers get notified on task state changes."""

    def __init__(self) -> None:
        self._subscribers: list[ObserverCallback] = []

    def subscribe(self, callback: ObserverCallback) -> Callable[[], None]:
        """Register a callback. Returns an unsubscribe function."""
        self._subscribers.append(callback)

        def _unsubscribe() -> None:
            if callback in self._subscribers:
                self._subscribers.remove(callback)

        return _unsubscribe

    def notify(self, task: Task) -> None:
        for cb in self._subscribers:
            try:
                cb(task)
            except Exception as exc:
                print(f"[TASK_OBSERVER] Subscriber error: {exc}")


class TaskManager:
    """Singleton manager for all tasks in the portal session."""

    _instance: TaskManager | None = None
    _lock = threading.Lock()

    def __new__(cls) -> TaskManager:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._tasks: dict[str, Task] = {}
                    cls._instance._observer = TaskObserver()
                    cls._instance._history: list[Task] = []
        return cls._instance

    # ------------------------------------------------------------------
    # Task lifecycle
    # ------------------------------------------------------------------

    def create_task(self, name: str) -> Task:
        task = Task(name=name)
        self._tasks[task.id] = task
        print(f"[TASK] Created: {name} ({task.id})")
        self._observer.notify(task)
        return task

    def start_task(self, task_id: str) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        task.status = TaskStatus.RUNNING
        task.started_at = time.time()
        task.message = "In progress..."
        print(f"[TASK] Started: {task.name} ({task_id})")
        self._observer.notify(task)
        return task

    def update_task(self, task_id: str, progress: float | None = None, message: str | None = None) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        if progress is not None:
            task.progress = min(max(progress, 0.0), 1.0)
        if message is not None:
            task.message = message
        self._observer.notify(task)
        return task

    def complete_task(self, task_id: str, result: Any = None) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        task.status = TaskStatus.COMPLETED
        task.progress = 1.0
        task.completed_at = time.time()
        task.result = result
        task.message = "Completed"
        print(f"[TASK] Completed: {task.name} ({task_id}) in {task.duration}s")
        self._archive_task(task_id)
        self._observer.notify(task)
        return task

    def fail_task(self, task_id: str, error: str) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        task.status = TaskStatus.FAILED
        task.completed_at = time.time()
        task.error = error
        task.message = f"Failed: {error}"
        print(f"[TASK] Failed: {task.name} ({task_id}): {error}")
        self._archive_task(task_id)
        self._observer.notify(task)
        return task

    def get_task(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def active_tasks(self) -> list[Task]:
        return [t for t in self._tasks.values() if t.status in (TaskStatus.PENDING, TaskStatus.RUNNING)]

    def completed_tasks(self) -> list[Task]:
        return list(self._history)

    def subscribe(self, callback: ObserverCallback) -> Callable[[], None]:
        return self._observer.subscribe(callback)

    # ------------------------------------------------------------------
    # Context manager for safe task lifecycle
    # ------------------------------------------------------------------

    def run(self, name: str) -> "_TaskContext":
        return _TaskContext(self, name)

    def _archive_task(self, task_id: str) -> None:
        task = self._tasks.pop(task_id, None)
        if task:
            self._history.append(task)
            if len(self._history) > 50:
                self._history.pop(0)


class _TaskContext:
    """Context manager: task tracking with auto-complete/auto-fail."""

    def __init__(self, manager: TaskManager, name: str) -> None:
        self._manager = manager
        self._task = manager.create_task(name)
        self._task_id = self._task.id

    def __enter__(self) -> "_TaskContext":
        self._manager.start_task(self._task_id)
        return self

    def __exit__(self, exc_type: type | None, exc_val: Exception | None, exc_tb: Any) -> None:
        if exc_type and exc_val:
            self._manager.fail_task(self._task_id, str(exc_val))
        else:
            self._manager.complete_task(self._task_id)

    @property
    def task_id(self) -> str:
        return self._task_id
