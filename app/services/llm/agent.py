"""Minimal LLM agent shim.

This module provides a tiny runtime-safe agent with a `chat` method that
returns a placeholder when no LLM is configured. Routers call higher-level
endpoints which may import this agent — keeping a stable API avoids crashes.
"""

from typing import Any, Dict, List


class Agent:
	def __init__(self, model_name: str | None = None):
		self.model_name = model_name

	def chat(self, prompt: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
		"""Return a safe placeholder response.

		Replace or extend this method to integrate a real LLM.
		"""
		return {
			"answer": "LLM not configured. This is a placeholder response.",
			"model": self.model_name,
			"actions": [],
		}


# convenience top-level function used by routers if needed
def chat(prompt: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
	agent = Agent()
	return agent.chat(prompt, context)
