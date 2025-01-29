from dataclasses import dataclass

@dataclass
class Manual:
	system_prompt: str
	core_values: str
	principles: str