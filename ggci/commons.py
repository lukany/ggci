from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from flask import current_app

_LOGGER = logging.getLogger(__name__)


def format_users(users: Union[User, List[User]], mention: bool = False) -> str:

    if isinstance(users, User):
        users = [users]

    if mention:
        formatted_users = [user.mention() for user in users]
    else:
        formatted_users = [str(user) for user in users]

    return ', '.join(formatted_users)


def _get_google_chat_id(gitlab_user_id: int) -> Optional[int]:
    return current_app.config['GGCI_USER_MAPPINGS'].get(gitlab_user_id)


@dataclass
class User:
    def __init__(self, gitlab_user_id: int, name: Optional[str] = None):
        self.gitlab_user_id = gitlab_user_id
        self.name = name

    def __str__(self):
        return self.name if self.name is not None else str(self.gitlab_user_id)

    def mention(self) -> str:
        google_chat_user_id = _get_google_chat_id(self.gitlab_user_id)
        if google_chat_user_id is None:
            _LOGGER.warning(
                'No Google Chat user ID found for GitLab user ID %d',
                self.gitlab_user_id,
            )
            return str(self)
        return f'<users/{google_chat_user_id}>'

    @classmethod
    def from_dict(cls, user_dict: Dict[str, Any]) -> User:
        return cls(
            gitlab_user_id=user_dict['id'],
            name=user_dict.get('name'),
        )


@dataclass
class Message:
    text: str
    thread_key: Optional[str] = None
