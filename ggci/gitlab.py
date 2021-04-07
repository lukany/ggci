from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from ggci.commons import User, format_users, Message


class UnsupportedEvent(Exception):
    pass


class Action(Enum):
    OPEN = 'open'
    UPDATE = 'update'
    MERGE = 'merge'
    APPROVED = 'approved'


@dataclass
class AssigneesChange:

    previous: List[User]
    current: List[User]

    @classmethod
    def from_dict(
        cls,
        changes: Dict[str, List[Dict[str, Any]]],
    ) -> AssigneesChange:
        return cls(
            previous=[User.from_dict(asgn) for asgn in changes['previous']],
            current=[User.from_dict(asgn) for asgn in changes['current']],
        )


@dataclass
class MergeRequestEvent:

    # pylint: disable=too-many-instance-attributes

    mr_id: int
    mr_iid: int
    assignees: List[User]
    description: str
    url: str
    title: str
    action: Action
    event_author: User
    assignees_change: Optional[AssigneesChange] = None

    @classmethod
    def from_dict(cls, event_dict: Dict[str, Any]) -> MergeRequestEvent:

        if event_dict['event_type'] != 'merge_request':
            raise UnsupportedEvent(
                f'Only "merge_request" events are currently supported, got:'
                f' {event_dict["event_type"]}'
            )

        mr_attrs = event_dict['object_attributes']

        action = Action(mr_attrs['action'])

        try:
            assignees_change_dict = event_dict['changes']['assignees']
        except KeyError as exc:
            if action == Action.UPDATE:
                raise UnsupportedEvent(
                    'Only assignee changes are supported for "update" action'
                    ' of "merge_request" event.'
                ) from exc
            assignees_change = None
        else:
            assignees_change = AssigneesChange.from_dict(assignees_change_dict)

        return cls(
            mr_id=mr_attrs['id'],
            mr_iid=mr_attrs['iid'],
            assignees=[
                User(gitlab_user_id=gitlab_user_id)
                for gitlab_user_id in mr_attrs['assignee_ids']
            ],
            description=mr_attrs['description'],
            url=mr_attrs['url'],
            title=mr_attrs['title'],
            action=Action(mr_attrs['action']),
            event_author=User.from_dict(user_dict=event_dict['user']),
            assignees_change=assignees_change,
        )

    @property
    def long_link(self) -> str:
        return f'<{self.url}|!{self.mr_iid} *{self.title}*>'

    @property
    def short_link(self) -> str:
        return f'<{self.url}|!{self.mr_iid}>'

    def create_message(self) -> Message:

        if self.action == Action.OPEN:
            assignees = format_users(self.assignees, mention=True)
            text = '\n'.join(
                (
                    f'*Opened* {self.long_link} by {self.event_author}',
                    f'*Assignees:* {assignees}',
                    f'*Description:* {self.description}',
                )
            )
        elif self.action == Action.APPROVED:
            text = f'{self.short_link} *approved* by {self.event_author}.'
        elif self.action == Action.MERGE:
            text = f'{self.short_link} *merged* by {self.event_author}.'
        elif self.action == Action.UPDATE:
            assert isinstance(self.assignees_change, AssigneesChange)
            previous = format_users(users=self.assignees_change.previous)
            current = format_users(
                users=self.assignees_change.current, mention=True
            )
            text = '\n'.join(
                (
                    f'{self.short_link} *reassigned* by {self.event_author}',
                    f'\tPrevious assignees: {previous}',
                    f'\tCurrent assignees: {current}',
                )
            )

        return Message(text=text, thread_key=self.mr_id)
