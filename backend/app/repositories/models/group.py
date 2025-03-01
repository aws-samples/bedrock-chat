from pydantic import BaseModel

class GroupModel(BaseModel):
    group_id: str # {LMS instance Id}-{course_id}
    group_name: str # name of the course in LMS
    create_time: float
    update_time: float
    create_by: str 
    role: str # values: TEACHER, SCHOOLADMIN, DISTRICTADMIN, SUPERADMIN
    user_name: str # name of the user