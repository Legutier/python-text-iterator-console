from typing import List, Optional

from dataclasses import dataclass, field


@dataclass
class TextData:
    main_stack: List[str]
    traversed_stack: List[str] = field(default_factory=list)
    actual_text: Optional[str] = None
