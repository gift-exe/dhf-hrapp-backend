from typing import Optional, List
from pydantic import BaseModel
from message.model import Message as MMessage
from message.model import Comment as MComment
from sqlalchemy.orm import Session
from user import utils as user_utils

class RequestReport(BaseModel):
    date_range: str

# class ReturnReportMessage(BaseModel):
#     created_at: str
#     sender: str
#     recipients: List[str]
#     document: Optional[str] = None
#     status: Optional[str] = None

#     @classmethod
#     def to_dict(cls, message: MMessage) -> 'RequestReport':
#         recipients = [f'{r.first_name} {r.last_name}' for r in message.recipients]
#         return cls(
#             sender=f'{message.sender.first_name} {message.sender.last_name}',
#             created_at = message.created_at.isoformat(),
#             recipients = recipients,
#             document = message.document,
#             status = message.status
#         )

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    id: int
    sender_id: int
    label: str
    title: str
    text: Optional[str]
    document: Optional[str]
    type: Optional[str]
    status: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

    @classmethod
    def to_dict(cls, message) -> 'MessageBase':
        recipients = [f'{r.first_name} {r.last_name}' for r in message.recipients]
        return cls(
            id=message.id,
            sender_id=message.sender_id,
            label=message.label,
            title=message.title,
            text=message.text,
            document=message.document,
            type=message.type,
            status=message.status,
            created_at=message.created_at.isoformat(),
            updated_at=message.updated_at.isoformat(),
            recipients=recipients
        )

class EvaluationBase(BaseModel):
    id: int
    created_at: str
    updated_at: str
    supervisor: str
    supervisor_post: str
    term: str
    session: str
    peer: str
    peer_post: str
    remark: str
    date: str
    supervisor_signature: str
    school_admin_signature: Optional[str]
    head_teacher_signature: Optional[str]
    director_signature: Optional[str]

    class Config:
        from_attributes = True

    @classmethod
    def to_dict(cls, evaluation) -> 'EvaluationBase':
        recipients = [f'{r.first_name} {r.last_name}' for r in evaluation.recipients]
        return cls(
            id=evaluation.id,
            created_at=evaluation.created_at.isoformat(),
            updated_at=evaluation.updated_at.isoformat(),
            supervisor=evaluation.supervisor,
            supervisor_post=evaluation.supervisor_post,
            term=evaluation.term,
            session=evaluation.session,
            peer=evaluation.peer,
            peer_post=evaluation.peer_post,
            remark=evaluation.remark,
            date=evaluation.date,
            supervisor_signature=evaluation.supervisor_signature,
            school_admin_signature=evaluation.school_admin_signature,
            head_teacher_signature=evaluation.head_teacher_signature,
            director_signature=evaluation.director_signature,
            recipients=recipients
        )

class EarlyClosureBase(BaseModel):
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

    class Config:
        from_attributes = True

    @classmethod
    def to_dict(cls, early_closure) -> 'EarlyClosureBase':
        recipients = [f'{r.first_name} {r.last_name}' for r in early_closure.recipients]
        return cls(
            id=early_closure.id,
            created_at=early_closure.created_at.isoformat(),
            updated_at=early_closure.updated_at.isoformat(),
            teacher=early_closure.teacher,
            clas=early_closure.clas,
            section=early_closure.section,
            permission=early_closure.permission,
            period=early_closure.period,
            reason=early_closure.reason,
            teacher_date=early_closure.teacher_date,
            head_comment=early_closure.head_comment,
            head_date=early_closure.head_date,
            appraiser_name=early_closure.appraiser_name,
            appraiser_post=early_closure.appraiser_post,
            hro_comment=early_closure.hro_comment,
            hro_date=early_closure.hro_date,
            director_comment=early_closure.director_comment,
            director_date=early_closure.director_date,
            teacher_signature=early_closure.teacher_signature,
            head_signature=early_closure.head_signature,
            hro_signature=early_closure.hro_signature,
            director_signature=early_closure.director_signature,
            school_stamp=early_closure.school_stamp,
            recipients=recipients
        )

class StudyLeaveBase(BaseModel):
    id: int
    created_at: str
    updated_at: str
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
    study_relevance: str
    applicant_job_desc: str
    duties_to_cover: str
    remark: str
    head_name: str
    head_post: str
    head_date: str
    salary_cost: str
    accountant_name: str
    accountant_post: str
    account_date: str
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
    approval_status: str
    director_date: str
    applicant_signature: str
    head_signature: str
    accountant_signature: str
    hr_signature: str
    director_signature: str

    class Config:
        from_attributes = True

    @classmethod
    def to_dict(cls, study_leave) -> 'StudyLeaveBase':
        recipients = [f'{r.first_name} {r.last_name}' for r in study_leave.recipients]
        return cls(
            id=study_leave.id,
            created_at=study_leave.created_at.isoformat(),
            updated_at=study_leave.updated_at.isoformat(),
            applicant_name=study_leave.applicant_name,
            designation=study_leave.designation,
            years_served=study_leave.years_served,
            institute_of_study=study_leave.institute_of_study,
            course_of_study=study_leave.course_of_study,
            area_of_study=study_leave.area_of_study,
            duration_of_study=study_leave.duration_of_study,
            purpose_of_study=study_leave.purpose_of_study,
            start_date=study_leave.start_date,
            end_date=study_leave.end_date,
            education_status=study_leave.education_status,
            year_obtained=study_leave.year_obtained,
            last_study_period=study_leave.last_study_period,
            pursue_indication=study_leave.pursue_indication,
            applicant_date=study_leave.applicant_date,
            study_relevance=study_leave.study_relevance,
            applicant_job_desc=study_leave.applicant_job_desc,
            duties_to_cover=study_leave.duties_to_cover,
            remark=study_leave.remark,
            head_name=study_leave.head_name,
            head_post=study_leave.head_post,
            head_date=study_leave.head_date,
            salary_cost=study_leave.salary_cost,
            accountant_name=study_leave.accountant_name,
            accountant_post=study_leave.accountant_post,
            account_date=study_leave.account_date,
            approval_grant=study_leave.approval_grant,
            grant_with_pay=study_leave.grant_with_pay,
            granted_program=study_leave.granted_program,
            years_after_resumption=study_leave.years_after_resumption,
            certificate_upgrade=study_leave.certificate_upgrade,
            beneficiary_number=study_leave.beneficiary_number,
            applicant_not_supported=study_leave.applicant_not_supported,
            hr_name=study_leave.hr_name,
            hr_post=study_leave.hr_post,
            hr_date=study_leave.hr_date,
            approval_status=study_leave.approval_status,
            director_date=study_leave.director_date,
            applicant_signature=study_leave.applicant_signature,
            head_signature=study_leave.head_signature,
            accountant_signature=study_leave.accountant_signature,
            hr_signature=study_leave.hr_signature,
            director_signature=study_leave.director_signature,
            recipients=recipients
        )
