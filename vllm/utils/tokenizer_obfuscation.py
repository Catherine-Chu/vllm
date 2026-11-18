# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the vLLM project
"""Optional startup bridge for the independently packaged mixed tokenizer.

The native default configuration never imports the optional package. Deployment
policy and artifact loading live in that package; this module only identifies
configurations that need its startup hooks.
"""

from importlib import import_module
from typing import Any


def _get(value: Any, key: str, default: Any = None) -> Any:
    return (
        value.get(key, default)
        if isinstance(value, dict)
        else getattr(value, key, default)
    )


def needs_obfuscation_hook(args: Any) -> bool:
    """Recognize explicitly configured capabilities, excluding native auto."""
    if getattr(args, "_tokenizer_obfuscation_preparing", False):
        # The trusted builder must first resolve the unmodified native config.
        # This private in-process marker is intentionally absent from the CLI.
        return False
    structured = getattr(args, "structured_outputs_config", None)
    reasoning = getattr(args, "reasoning_config", None)
    return bool(
        getattr(args, "enable_tokenizer_obfuscation", False)
        or getattr(args, "tokenizer_obfuscation_artifacts", None)
        or getattr(args, "tokenizer_mode", None) == "mixed_bytes"
        or getattr(args, "reasoning_parser", None)
        or getattr(args, "reasoning_parser_plugin", None)
        or getattr(args, "enable_auto_tool_choice", False)
        or getattr(args, "tool_call_parser", None)
        or getattr(args, "tool_strict_level", "auto") not in (None, "auto")
        or _get(structured, "backend", "auto") != "auto"
        or _get(structured, "reasoning_parser", "")
        or _get(structured, "reasoning_parser_plugin", "")
        or _get(structured, "enable_in_reasoning", False)
        or _get(structured, "disable_any_whitespace", False)
        or _get(structured, "disable_additional_properties", False)
        or _get(reasoning, "reasoning_parser", "")
        or _get(reasoning, "reasoning_start_str", "")
        or _get(reasoning, "reasoning_end_str", "")
    )


def run_obfuscation_hook(name: str, args: Any, *extra: Any) -> None:
    """Delegate configuration without adding a dependency to native startup."""
    if needs_obfuscation_hook(args):
        module = import_module("mixed_tokenizer.scheme31_startup")
        getattr(module, name)(args, *extra)
