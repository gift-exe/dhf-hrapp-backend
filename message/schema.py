from typing import Optional, List
from pydantic import BaseModel
from message.model import Message as MMessage
from message.model import Comment as MComment
from message.model import Evaluation as MEvaluation
from sqlalchemy.orm import Session
from user import utils as user_utils
from datetime import datetime
class CreateComment(BaseModel):
    text: str
    message_id: int
    type: str


class CreateMessage(BaseModel):
    sender_id: int
    label: str
    title: str
    text: Optional[str] = None
    document: Optional[str] = None
    status: str
    type: str

class ReturnMessage(BaseModel):
    message_id: int
    sender: str
    recipients: List[str]
    label: str
    title: str
    text: Optional[str] = None
    document: Optional[str] = None
    status: str = None
    comments: List[dict] = []

    @classmethod
    def to_dict(cls, msg:MMessage, comments:MComment, db:Session) -> "ReturnMessage":
        recipients = [f'{r.first_name} {r.last_name}' for r in msg.recipients]
        return cls (
            message_id=msg.id, 
            sender=f"{user_utils.get_user(db=db, user_id=msg.sender_id).first_name} {user_utils.get_user(db=db, user_id=msg.sender_id).last_name}", 
            recipients=recipients,
            label=msg.label,
            title=msg.title,
            text=msg.text,
            document=msg.document,
            status=msg.status,
            comments = [{'comments_id':comment.id, 
                         'text':comment.text, 
                         'sender':f'{user_utils.get_user(db=db, user_id=comment.sender_id).first_name} {user_utils.get_user(db=db, user_id=comment.sender_id).last_name}'} 
                        for comment in comments]
        )

class LeaveResponse(BaseModel):
    message_id: int
    status: str

class ShareLeaveRequest(BaseModel):
    message_id: int
    recipients: List[str]


### EVALUATION ###
class GradeBase(BaseModel):
    completes_task_on_time: str
    attends_school_meetings_till_closure: str
    makes_positive_contributions: str
    handles_responsibilities_appropriately: str
    displays_technical_competence: str
    very_creative: str
    easy_to_work_with: str
    works_well_under_pressure: str
    communicates_well_in_written_form: str
    communicates_well_when_speaking: str
    assists_other_teams_when_needed: str
    demonstrates_good_problem_solving_skills: str
    listens_well: str
    works_well_with_parents: str
    coaches_class_assistant_well: str
    coaches_weak_students_well: str
    learns_quickly: str
    works_well_on_own: str
    reliable: str
    produces_high_quality_output: str
    handles_pupils_conflicts_well: str
    handles_cases_of_puppils_discipline_well: str
    accepts_and_perfects_corrections_well: str
    well_organized: str
    look_forward_to_working_again: str
    punctual_to_school: str
    regular_in_school: str
    does_well_on_duty: str
    class_namagement: str
    shows_concern_to_school_environment: str
    enforces_school_rules_always: str

class GradeCreate(GradeBase):
    pass

class EvaluationBase(BaseModel):
    supervisor: str
    supervisor_post: str
    term: str
    session: str
    peer: str
    peer_post: str
    remark: str
    date: str
    supervisor_signature: str
    grades: GradeCreate
    recipient_hos: str
    
class EvaluationHeadTeacherResponse(BaseModel):
    head_teacher_signature: str
    recipient_hr: str

class EvaluationHRResponse(BaseModel):
    school_admin_signature: str
    recipient_director: str    
class EvaluationDirectorResponse(BaseModel):
    director_signature: str

class EvaluationCreate(EvaluationBase):
    pass
class Evaluation(EvaluationBase):
    id: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        orm_mode = True

class Grade(GradeBase):
    id: int
    created_at: Optional[str]
    updated_at: Optional[str]
    evaluation_id: int

    class Config:
        orm_mode = True
        from_attributes = True


### EARLY CLOSURE ###

class EarlyClosureCreate(BaseModel):
    teacher: str
    clas: str
    section: str
    permission: str
    period: str
    reason: str
    teacher_date: str
    teacher_signature: str
    recipient_hos: str

class EarlyClosureHOSResponse(BaseModel):
    head_comment: str
    head_date: str
    appraiser_name: str
    appraiser_post: str
    head_signature: str
    recipient_hr: str

class EarlyClosureHRResponse(BaseModel):
    hro_comment: str
    hro_date: str
    hro_signature: str
    school_stamp: Optional[str] = None
    recipient_director: str

class EarlyClosureDirectorResponse(BaseModel):
    director_comment: str
    director_date: str
    director_signature: str
    school_stamp: Optional[str] = None


class EarlyClosureRetrieve(BaseModel):
    id: int
    created_at: str
    updated_at: str
    teacher: str
    clas: str
    section: str
    permission: str
    period: str
    reason: str
    teacher_date: str
    head_comment: str
    head_date: str
    appraiser_name: str
    appraiser_post: str
    hro_comment: str
    hro_date: str
    director_comment: str
    director_date: str
    teacher_signature: str
    head_signature: str
    hro_signature: str
    director_signature: str
    school_stamp: str


### STUDY LEAVE ###

class StudyLeaveApplicant(BaseModel):
    applicant_name: str
    designation: str
    years_served: str
    institute_of_study: str
    course_of_study: str
    area_of_study: str
    duration_of_study: str
    purpose_of_study: str
    start_date: str
    end_date: str
    education_status: str
    year_obtained: str
    last_study_period: str
    pursue_indication: str
    applicant_date: str
    applicant_signature: str
    recipient_hos: str

class StudyLeaveHeadTeacher(BaseModel):
    study_relevance: str
    applicant_job_desc: str
    duties_to_cover: str
    remark: str
    head_name: str
    head_post: str
    head_date: str
    head_signature: str
    recipient_hr: str

class StudyLeaveAccountant(BaseModel):
    salary_cost: str
    accountant_name: str
    accountant_post: str
    account_date: str
    accountant_signature: str

class StudyLeaveHR(BaseModel):
    approval_grant: str
    grant_with_pay: str
    granted_program: str
    years_after_resumption: str
    certificate_upgrade: str
    beneficiary_number: str
    applicant_not_supported: str
    hr_name: str
    hr_post: str
    hr_date: str
    hr_signature: str
    recipient_accountant: str
    recipient_director: str

class StudyLeaveDirector(BaseModel):
    approval_status: str
    director_date: str
    director_signature: str