from enum import Enum

class Position(str, Enum):
    Admin = "Admin"
    Lead_Researcher = "Lead Researcher"
    Researcher = "Researcher"