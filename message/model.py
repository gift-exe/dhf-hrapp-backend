from sqlalchemy import String, Column, DateTime, func, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from config.database import Base

message_recipients_association = Table(
    'message_recipients_association',
    Base.metadata,
    Column('message_id', Integer, ForeignKey('messages.id', ondelete='CASCADE')),
    Column('recipient_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('created_at', DateTime, nullable=False, default=func.now()),
    Column('updated_at', DateTime, nullable=False, default=func.now()),
)

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    label = Column(String, nullable=False)
    title = Column(String, nullable=False)
    text = Column(String, nullable=True)
    document = Column(String, nullable=True)
    type = Column(String)
    status = Column(String, nullable=False, default='pending')
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())
    
    sender = relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
    recipients = relationship("User", back_populates="received_messages", secondary=message_recipients_association)

    comments = relationship("Comment", back_populates="message", foreign_keys="[Comment.message_id]", cascade="all, delete-orphan")

class Comment(Base):
    #whaky hack lmao
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    
    message_id = Column(Integer, ForeignKey("messages.id", ondelete='CASCADE'))
    evaluation_id = Column(Integer, ForeignKey("evaluations.id", ondelete='CASCADE'))
    early_closure_id = Column(Integer, ForeignKey("early-closures.id", ondelete='CASCADE'))
    study_leave_id = Column(Integer, ForeignKey("study-leave.id", ondelete='CASCADE'))
    type = Column(String, nullable=False, default='message')
    
    sender_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))

    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    message = relationship("Message", back_populates="comments", foreign_keys=[message_id])
    evaluation = relationship("Evaluation", back_populates="comments", foreign_keys=[evaluation_id])
    early_closure = relationship("EarlyClosure", back_populates="comments", foreign_keys=[early_closure_id])
    study_leave = relationship("StudyLeave", back_populates="comments", foreign_keys=[study_leave_id])
    sender = relationship("User", back_populates="comments", foreign_keys=[sender_id])

evaluation_recipients_association = Table(
    'evaluation_recipients_association',
    Base.metadata,
    Column('evaluation_id', Integer, ForeignKey('evaluations.id', ondelete='CASCADE')),
    Column('recipient_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('created_at', DateTime, nullable=False, default=func.now()),
    Column('updated_at', DateTime, nullable=False, default=func.now()),
)

class Evaluation(Base):
    __tablename__ = 'evaluations'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    supervisor = Column(String, nullable=False)
    supervisor_post = Column(String, nullable=False)
    
    term = Column(String, nullable=False)
    session = Column(String, nullable=False)
    
    peer = Column(String, nullable=False)
    peer_post = Column(String, nullable=False)

    remark = Column(String, nullable=False)
    date = Column(String, nullable=False)
    
    #files
    supervisor_signature = Column(String, nullable=False) 
    school_admin_signature = Column(String)
    head_teacher_signature = Column(String)
    director_signature = Column(String)

    #grades
    grade = relationship('Grade', uselist=False, back_populates='evaluation', cascade="all, delete-orphan")

    sender_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'))
    sender = relationship("User", back_populates="sent_evaluations", foreign_keys=[sender_id])
    recipients = relationship("User", back_populates="received_evaluations", secondary=evaluation_recipients_association)
    comments = relationship("Comment", back_populates="evaluation", foreign_keys="[Comment.evaluation_id]", cascade="all, delete-orphan")

class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    completes_task_on_time = Column(String, nullable=False)
    attends_school_meetings_till_closure = Column(String, nullable=False)
    makes_positive_contributions = Column(String, nullable=False)
    handles_responsibilities_appropriately = Column(String, nullable=False)
    displays_technical_competence = Column(String, nullable=False)
    very_creative = Column(String, nullable=False)
    easy_to_work_with = Column(String, nullable=False)
    works_well_under_pressure = Column(String, nullable=False)
    communicates_well_in_written_form = Column(String, nullable=False)
    communicates_well_when_speaking = Column(String, nullable=False)
    assists_other_teams_when_needed = Column(String, nullable=False)
    demonstrates_good_problem_solving_skills = Column(String, nullable=False)
    listens_well = Column(String, nullable=False)
    works_well_with_parents = Column(String, nullable=False)
    coaches_class_assistant_well = Column(String, nullable=False)
    coaches_weak_students_well = Column(String, nullable=False)
    learns_quickly = Column(String, nullable=False)
    works_well_on_own = Column(String, nullable=False)
    reliable = Column(String, nullable=False)
    produces_high_quality_output = Column(String, nullable=False)
    handles_pupils_conflicts_well = Column(String, nullable=False)
    handles_cases_of_puppils_discipline_well = Column(String, nullable=False)
    accepts_and_perfects_corrections_well = Column(String, nullable=False)
    well_organized = Column(String, nullable=False)
    look_forward_to_working_again = Column(String, nullable=False)
    punctual_to_school = Column(String, nullable=False)
    regular_in_school = Column(String, nullable=False)
    does_well_on_duty = Column(String, nullable=False)
    class_namagement = Column(String, nullable=False)
    shows_concern_to_school_environment = Column(String, nullable=False)
    enforces_school_rules_always = Column(String, nullable=False)

    evaluation_id = Column(Integer, ForeignKey('evaluations.id'))
    evaluation = relationship('Evaluation', back_populates='grade')

early_closure_recipients_association = Table(
    'early_closure_recipients_association',
    Base.metadata,
    Column('early_closure_id', Integer, ForeignKey('early-closures.id', ondelete='CASCADE')),
    Column('recipient_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('created_at', DateTime, nullable=False, default=func.now()),
    Column('updated_at', DateTime, nullable=False, default=func.now()),
)

class EarlyClosure(Base):
    __tablename__ = 'early-closures'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    teacher = Column(String, nullable=False)
    clas = Column(String, nullable=False)
    section = Column(String, nullable=False)
    permission = Column(String, nullable=False)
    period = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    teacher_date = Column(String, nullable=False)
    
    head_comment = Column(String, nullable=False, default='no response')
    head_date = Column(String, nullable=False, default='no response')
    appraiser_name = Column(String, nullable=False, default='no response')
    appraiser_post = Column(String, nullable=False, default='no response')

    hro_comment = Column(String, nullable=False, default='no response')
    hro_date = Column(String, nullable=False, default='no response')

    director_comment = Column(String, nullable=False, default='no response')
    director_date = Column(String, nullable=False, default='no response')

    #files
    teacher_signature = Column(String, nullable=False)
    head_signature = Column(String, nullable=False, default='no response')
    hro_signature = Column(String, nullable=False, default='no response')
    director_signature = Column(String, nullable=False, default='no response')
    school_stamp = Column(String, nullable=False, default='no response')

    sender_id = Column(Integer, ForeignKey("users.id"))
    sender = relationship("User", back_populates="sent_early_closures", foreign_keys=[sender_id])
    comments = relationship("Comment", back_populates="early_closure", foreign_keys="[Comment.early_closure_id]", cascade="all, delete-orphan")
    recipients = relationship("User", back_populates="received_early_closures", secondary=early_closure_recipients_association)

study_leave_recipients_association = Table(
    'study_leave_recipients_association',
    Base.metadata,
    Column('early_leave_id', Integer, ForeignKey('study-leave.id', ondelete='CASCADE')),
    Column('recipient_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('created_at', DateTime, nullable=False, default=func.now()),
    Column('updated_at', DateTime, nullable=False, default=func.now()),
)
class StudyLeave(Base):
    __tablename__ = 'study-leave'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    #applicant info
    applicant_name = Column(String, nullable=False)
    designation = Column(String, nullable=False)
    years_served = Column(String, nullable=False)
    
    institute_of_study = Column(String, nullable=False)
    course_of_study = Column(String, nullable=False)
    area_of_study = Column(String, nullable=False)
    duration_of_study = Column(String, nullable=False)
    purpose_of_study = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    
    education_status = Column(String, nullable=False)
    year_obtained = Column(String, nullable=False)
    last_study_period = Column(String, nullable=False)

    pursue_indication = Column(String, nullable=False)

    applicant_date = Column(String, nullable=False)

    #headd teacher info
    study_relevance = Column(String, nullable=False, default='no response')
    applicant_job_desc = Column(String, nullable=False, default='no response')
    duties_to_cover = Column(String, nullable=False, default='no response')
    remark = Column(String, nullable=False, default='no response')
    
    head_name = Column(String, nullable=False, default='no response')
    head_post = Column(String, nullable=False, default='no response')
    head_date = Column(String, nullable=False, default='no response')
    
    #accountant info
    salary_cost = Column(String, nullable=False, default='no response')

    accountant_name = Column(String, nullable=False, default='no response')
    accountant_post = Column(String, nullable=False, default='no response')
    account_date = Column(String, nullable=False, default='no response')

    #HR info
    approval_grant = Column(String, nullable=False, default='no response')
    grant_with_pay = Column(String, nullable=False, default='no response')
    granted_program = Column(String, nullable=False, default='no response')
    years_after_resumption = Column(String, nullable=False, default='no response')
    certificate_upgrade = Column(String, nullable=False, default='no response')
    beneficiary_number = Column(String, nullable=False, default='no response')
    applicant_not_supported = Column(String, nullable=False, default='no response')

    hr_name = Column(String, nullable=False, default='no response')
    hr_post = Column(String, nullable=False, default='no response')
    hr_date = Column(String, nullable=False, default='no response')

    #director info
    approval_status = Column(String, nullable=False, default='no response')
    director_date = Column(String, nullable=False, default='no response')


    #files
    applicant_signature = Column(String, nullable=False)
    head_signature = Column(String, nullable=False, default='no response')
    accountant_signature = Column(String, nullable=False, default='no response')
    hr_signature = Column(String, nullable=False, default='no response')
    director_signature = Column(String, nullable=False, default='no response')

    sender_id = Column(Integer, ForeignKey("users.id"))
    sender = relationship("User", back_populates="sent_study_leaves", foreign_keys=[sender_id])
    comments = relationship("Comment", back_populates="study_leave", foreign_keys="[Comment.study_leave_id]", cascade="all, delete-orphan")
    recipients = relationship("User", back_populates="received_study_leaves", secondary=study_leave_recipients_association)
