from __future__ import annotations
from typing import Callable, Any, Optional, Union
import uuid


class TextInput:
    STYLES = {"short": 1, "paragraph": 2}

    def __init__(
        self,
        label: str,
        custom_id: Optional[str] = None,
        style: str = "short",
        placeholder: Optional[str] = None,
        value: Optional[str] = None,
        required: bool = True,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
    ):
        if len(label) > 45:
            raise ValueError("TextInput label cannot exceed 45 characters.")

        if style not in self.STYLES:
            raise ValueError(f"Invalid style '{style}'. Use 'short' or 'paragraph'.")

        if min_length is not None and min_length < 0:
            raise ValueError("min_length must be >= 0.")
        if max_length is not None and max_length > 4000:
            raise ValueError("max_length cannot exceed 4000.")
        if min_length is not None and max_length is not None and min_length > max_length:
            raise ValueError("min_length cannot be greater than max_length.")

        self.label = label
        self.custom_id = custom_id or f"{label.lower().replace(' ', '_')}_{uuid.uuid4().hex[:6]}"
        self.style = style
        self.placeholder = placeholder
        self.value = value
        self.required = required
        self.min_length = min_length
        self.max_length = max_length

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "type": 4,
            "custom_id": self.custom_id,
            "label": self.label,
            "style": self.STYLES[self.style],
            "required": self.required,
        }
        if self.placeholder:
            data["placeholder"] = self.placeholder
        if self.value:
            data["value"] = self.value
        if self.min_length is not None:
            data["min_length"] = self.min_length
        if self.max_length is not None:
            data["max_length"] = self.max_length
        return data


class Modal:
    def __init__(
        self,
        title: str,
        fields: list[Union[dict[str, Any], TextInput]],
        callback: Callable[..., Any],
        custom_id: Optional[str] = None,
    ):
        if len(title) > 45:
            raise ValueError("Modal title cannot exceed 45 characters.")
        if len(fields) > 5:
            raise ValueError("A modal cannot have more than 5 text input fields.")

        self.title = title
        self.fields: list[TextInput] = [
            TextInput(**field) if isinstance(field, dict) else field for field in fields
        ]
        self.callback = callback
        self.custom_id = custom_id or f"{title.lower().replace(' ', '_')}_{uuid.uuid4().hex[:6]}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "custom_id": self.custom_id,
            "components": [{"type": 1, "components": [field.to_dict()]} for field in self.fields],
        }

    def add_field(
        self,
        label: str,
        custom_id: Optional[str] = None,
        style: str = "short",
        placeholder: Optional[str] = None,
        required: bool = True,
        **kwargs,
    ) -> Modal:
        if len(self.fields) >= 5:
            raise ValueError("A modal cannot have more than 5 fields.")
        field = TextInput(label, custom_id, style, placeholder, required=required, **kwargs)
        self.fields.append(field)
        return self

    @classmethod
    def quick(
        cls,
        title: str,
        callback: Callable[..., Any],
        *field_labels: str,
        **field_kwargs: dict[str, Any],
    ) -> Modal:
        fields = []
        for label in field_labels:
            fields.append({"label": label, "required": True})
        for label, opts in field_kwargs.items():
            if isinstance(opts, dict):
                fields.append({"label": label, **opts})
            else:
                fields.append({"label": label, "required": bool(opts)})
        return cls(title, fields, callback)
