from enum import StrEnum
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Literal,
    Protocol,
    TypedDict,
    TypeVar,
)

if TYPE_CHECKING:
    from chainlit.element import ElementDict
    from chainlit.step import StepDict

from dataclasses import field

from dataclasses_json import DataClassJsonMixin
from pydantic import BaseModel, model_validator
from pydantic.dataclasses import dataclass

InputWidgetType = Literal[
    "switch",
    "slider",
    "select",
    "textinput",
    "tags",
    "numberinput",
    "multiselect",
    "checkbox",
    "radio",
    "datepicker",
]
ToastType = Literal["info", "success", "warning", "error"]


class ThreadDict(TypedDict):
    id: str
    createdAt: str
    name: str | None
    userId: str | None
    userIdentifier: str | None
    tags: list[str] | None
    metadata: dict | None
    steps: list[StepDict]
    elements: list[ElementDict] | None


class Pagination(BaseModel):
    first: int
    cursor: str | None = None


class ThreadFilter(BaseModel):
    feedback: Literal[0, 1] | None = None
    userId: str | None = None
    search: str | None = None


@dataclass
class PageInfo:
    hasNextPage: bool
    startCursor: str | None
    endCursor: str | None

    def to_dict(self):
        return {
            "hasNextPage": self.hasNextPage,
            "startCursor": self.startCursor,
            "endCursor": self.endCursor,
        }

    @classmethod
    def from_dict(cls, page_info_dict: dict) -> PageInfo:
        hasNextPage = page_info_dict.get("hasNextPage", False)
        startCursor = page_info_dict.get("startCursor", None)
        endCursor = page_info_dict.get("endCursor", None)
        return cls(
            hasNextPage=hasNextPage, startCursor=startCursor, endCursor=endCursor
        )


T = TypeVar("T", covariant=True)


class HasFromDict(Protocol[T]):
    @classmethod
    def from_dict(cls, obj_dict: Any) -> T:
        raise NotImplementedError


@dataclass
class PaginatedResponse(Generic[T]):  # noqa: UP046
    pageInfo: PageInfo
    data: list[T]

    def to_dict(self):
        return {
            "pageInfo": self.pageInfo.to_dict(),
            "data": [
                (d.to_dict() if hasattr(d, "to_dict") and callable(d.to_dict) else d)
                for d in self.data
            ],
        }

    @classmethod
    def from_dict(
        cls, paginated_response_dict: dict, the_class: HasFromDict[T]
    ) -> PaginatedResponse[T]:
        pageInfo = PageInfo.from_dict(paginated_response_dict.get("pageInfo", {}))

        data = [the_class.from_dict(d) for d in paginated_response_dict.get("data", [])]

        return cls(pageInfo=pageInfo, data=data)


@dataclass
class FileSpec(DataClassJsonMixin):
    accept: list[str] | dict[str, list[str]]
    max_files: int
    max_size_mb: int


@dataclass
class ActionSpec(DataClassJsonMixin):
    keys: list[str]


@dataclass
class AskSpec(DataClassJsonMixin):
    """Specification for asking the user."""

    timeout: int
    type: Literal["text", "file", "action", "element"]
    step_id: str


@dataclass
class AskFileSpec(FileSpec, AskSpec, DataClassJsonMixin):
    """Specification for asking the user a file."""


@dataclass
class AskActionSpec(ActionSpec, AskSpec, DataClassJsonMixin):
    """Specification for asking the user an action"""


@dataclass
class AskElementSpec(AskSpec, DataClassJsonMixin):
    """Specification for asking the user a custom element"""

    element_id: str


class FileReference(TypedDict):
    id: str


class FileDict(TypedDict):
    id: str
    name: str
    path: Path
    size: int
    type: str


class MessagePayload(TypedDict):
    message: StepDict
    fileReferences: list[FileReference] | None


class InputAudioChunkPayload(TypedDict):
    isStart: bool
    mimeType: str
    elapsedTime: float
    data: bytes


@dataclass
class InputAudioChunk:
    isStart: bool
    mimeType: str
    elapsedTime: float
    data: bytes


class OutputAudioChunk(TypedDict):
    track: str
    mimeType: str
    data: bytes


@dataclass
class AskFileResponse:
    id: str
    name: str
    path: str
    size: int
    type: str


class AskActionResponse(TypedDict):
    name: str
    payload: dict
    label: str
    tooltip: str
    forId: str
    id: str


class AskElementResponse(TypedDict, total=False):
    submitted: bool


class UpdateThreadRequest(BaseModel):
    threadId: str
    name: str


class ShareThreadRequest(BaseModel):
    threadId: str
    isShared: bool


class DeleteThreadRequest(BaseModel):
    threadId: str


class DeleteFeedbackRequest(BaseModel):
    feedbackId: str


class GetThreadsRequest(BaseModel):
    pagination: Pagination
    filter: ThreadFilter


class CallActionRequest(BaseModel):
    action: dict
    sessionId: str


class ConnectMCPRequest(BaseModel):
    """Request to connect an MCP server.

    Named server (developer-configured in config): provide sessionId + name only.
    User-provided server (SSE/HTTP only, when enabled): also provide clientType + url.
    """

    sessionId: str
    name: str
    # Present only for user-provided connections:
    clientType: Literal["sse", "streamable-http"] | None = None
    url: str | None = None
    headers: dict[str, str] | None = None

    @model_validator(mode="after")
    def validate_user_provided_consistency(self) -> ConnectMCPRequest:
        has_url = self.url is not None
        has_type = self.clientType is not None
        if has_url != has_type:
            raise ValueError(
                "Both 'url' and 'clientType' must be provided together for user-provided connections"
            )
        return self


class DisconnectMCPRequest(BaseModel):
    sessionId: str
    name: str


class ElementRequest(BaseModel):
    element: dict
    sessionId: str


class Theme(StrEnum):
    light = "light"
    dark = "dark"


@dataclass
class Starter(DataClassJsonMixin):
    """Specification for a starter that can be chosen by the user at the thread start."""

    label: str
    message: str
    command: str | None = None
    icon: str | None = None


@dataclass
class StarterCategory(DataClassJsonMixin):
    """A category/group of starters with an optional icon."""

    label: str
    icon: str | None = None
    starters: list[Starter] = field(default_factory=list)


@dataclass
class ChatProfile(DataClassJsonMixin):
    """Specification for a chat profile that can be chosen by the user at the thread start."""

    name: str
    markdown_description: str
    icon: str | None = None
    display_name: str | None = None
    default: bool = False
    starters: list[Starter] | None = None
    config_overrides: Any = None


FeedbackStrategy = Literal["BINARY"]


class CommandDict(TypedDict):
    # The identifier of the command, will be displayed in the UI
    id: str
    # The description of the command, will be displayed in the UI
    description: str
    # The lucide icon name
    icon: str
    # Display the command as a button in the composer
    button: bool | None
    # Whether the command will be persistent unless the user toggles it
    persistent: bool | None
    # Whether the command should be pre-selected when loaded
    selected: bool | None


class FeedbackDict(TypedDict):
    forId: str
    id: str | None
    value: Literal[0, 1]
    comment: str | None


@dataclass
class Feedback:
    forId: str
    value: Literal[0, 1]
    threadId: str | None = None
    id: str | None = None
    comment: str | None = None


class UpdateFeedbackRequest(BaseModel):
    feedback: Feedback
    sessionId: str
