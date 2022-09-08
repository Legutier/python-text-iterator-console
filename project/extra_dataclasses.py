from typing import List, Optional, Dict, Union

from dataclasses import dataclass, field


@dataclass
class TextData:
    main_stack: List[str]
    traversed_stack: List[str] = field(default_factory=list)
    actual_text: Optional[str] = None
    to_compare_text: Optional[str] = None
    metrics_summary: Dict[str, Union[str, int]] = field(default_factory=dict)
