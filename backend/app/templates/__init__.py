"""
Template module for Excel templates
"""
import io
import pandas as pd
from pathlib import Path

# Path to the reordered template
REORDERED_TEMPLATE_PATH = Path(__file__).parent.parent.parent / "static" / "templates" / "exam_template_reordered.xlsx"
from .course_template import generate_course_template
from .exam_template import generate_exam_template
from .student_template import generate_student_template

__all__ = [
    "generate_course_template",
    "generate_exam_template",
    "generate_student_template"
]
