from sqlalchemy.orm import Session
from message import model
from message import schema
from typing import List
from user import utils as user_utils

def create_message(db: Session, recipients:List[str], message: schema.CreateMessage):
    try:
        result = model.Message(sender_id=message.sender_id, 
                            label=message.label, 
                            title=message.title, 
                            text=message.text, 
                            document=message.document, 
                            type=message.type,
                            status=message.status)
        
        for recipient in recipients:
            user = user_utils.get_user_by_email(email=recipient, db=db)
            result.recipients.append(user)
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    except Exception as e:
        db.rollback()
        raise e
    
def get_message(db: Session, message_id):
    try:
        message = db.query(model.Message).filter(model.Message.id == message_id).first()
        return message
    except Exception as e:
        raise e

def create_comment(db: Session, comment: schema.CreateComment, sender_id):
    
    try:
        if comment.type == 'message':
            result = model.Comment(text=comment.text,
                                message_id=comment.message_id,
                                sender_id=sender_id,
                                type=comment.type)
        elif comment.type == 'study_leave':
            result = model.Comment(text=comment.text,
                                study_leave_id=comment.message_id,
                                sender_id=sender_id,
                                type=comment.type)
        elif comment.type == 'early closure':
            result = model.Comment(text=comment.text,
                                early_closure_id=comment.message_id,
                                sender_id=sender_id,
                                type=comment.type)
        elif comment.type == 'evaluation':
            result = model.Comment(text=comment.text,
                                evaluation_id=comment.message_id,
                                sender_id=sender_id,
                                type=comment.type)
        else:
            raise ValueError('message type not recognised valid types are: \
                             "message", "evaluation", "study leave" or "early closure"')
        
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    except Exception as e:
        db.rollback()
        raise e
    
def get_leave_requests(db: Session):
    try:
        leave_requests = db.query(model.StudyLeave).all()
        return leave_requests
    except Exception as e:
        raise e
    
def get_early_closures(db: Session):
    try:
        return db.query(model.EarlyClosure).all()
    except Exception as e:
        raise e
    
def create_evaluation_with_grade(db: Session, evaluation: schema.EvaluationCreate, sender:int):
    try:
        # Create Evaluation object
        eval = evaluation.model_dump()
        eval['sender_id'] = sender
        grade_data_dict = eval.pop('grades')

        db_evaluation = model.Evaluation(**eval)
        db.add(db_evaluation)
        db.commit()
        db.refresh(db_evaluation)

        # Create Grade object and associate it with the Evaluation
        grade_data_dict["evaluation_id"] = db_evaluation.id
        db_grade = model.Grade(**grade_data_dict)
        db.add(db_grade)
        db.commit()
        db.refresh(db_grade)
        
        return db_evaluation
    except Exception as e:
        db.rollback()
        raise e

def get_all_evaluations(db: Session):
    try:
        evaluations = db.query(model.Evaluation).all()
        return evaluations
    except Exception as e:
        raise e


def create_early_closure(db: Session, early_closure_data: schema.EarlyClosureCreate, sender:int):
    try:
        ecd = early_closure_data.model_dump()
        ecd['sender_id'] = sender
        db_early_closure = model.EarlyClosure(**ecd)
        db.add(db_early_closure)
        db.commit()
        db.refresh(db_early_closure)
        return db_early_closure
    except Exception as e:
        raise e

def update_early_closure_hos_response(db: Session, early_closure_id: int, response_data: schema.EarlyClosureHOSResponse):
    try:
        db_early_closure = db.query(model.EarlyClosure).filter(model.EarlyClosure.id == early_closure_id).first()
        if db_early_closure:
            db_early_closure.head_comment = response_data.head_comment
            db_early_closure.head_date = response_data.head_date
            db_early_closure.appraiser_name = response_data.appraiser_name
            db_early_closure.appraiser_post = response_data.appraiser_post
            db_early_closure.head_signature = response_data.head_signature
            db.commit()
        else:
            raise ValueError("Early closure not found")
    except Exception as e:
        raise e

def update_early_closure_hr_response(db: Session, early_closure_id: int, response_data: schema.EarlyClosureHRResponse):
    try:
        db_early_closure = db.query(model.EarlyClosure).filter(model.EarlyClosure.id == early_closure_id).first()
        if db_early_closure:
            db_early_closure.hro_comment = response_data.hro_comment
            db_early_closure.hro_date = response_data.hro_date
            db_early_closure.hro_signature = response_data.hro_signature
            if response_data.school_stamp:
                db_early_closure.school_stamp = response_data.school_stamp
            db.commit()
        else:
            raise ValueError("Early closure not found")
    except Exception as e:
        raise e

def update_early_closure_director_response(db: Session, early_closure_id: int, response_data: schema.EarlyClosureDirectorResponse):
    try:
        db_early_closure = db.query(model.EarlyClosure).filter(model.EarlyClosure.id == early_closure_id).first()
        if db_early_closure:
            db_early_closure.director_comment = response_data.director_comment
            db_early_closure.director_date = response_data.director_date
            db_early_closure.director_signature = response_data.director_signature
            if response_data.school_stamp:
                db_early_closure.school_stamp = response_data.school_stamp
            db.commit()
        else:
            raise ValueError("Early closure not found")
    except Exception as e:
        raise e


def create_study_leave(db: Session, study_leave_data: schema.StudyLeaveApplicant, sender: int):
    try:
        sld = study_leave_data.model_dump()
        sld['sender_id']=sender
        db_study_leave = model.StudyLeave(**sld)
        db.add(db_study_leave)
        db.commit()
        db.refresh(db_study_leave)
        return db_study_leave
    except Exception as e:
        raise e

def update_study_leave_head_teacher_response(db: Session, study_leave_id: int, response_data: schema.StudyLeaveHeadTeacher):
    try:
        db_study_leave = db.query(model.StudyLeave).filter(model.StudyLeave.id == study_leave_id).first()
        if db_study_leave:
            db_study_leave.study_relevance = response_data.study_relevance
            db_study_leave.applicant_job_desc = response_data.applicant_job_desc
            db_study_leave.duties_to_cover = response_data.duties_to_cover
            db_study_leave.remark = response_data.remark
            db_study_leave.head_name = response_data.head_name
            db_study_leave.head_post = response_data.head_post
            db_study_leave.head_date = response_data.head_date
            db_study_leave.head_signature = response_data.head_signature
            db.commit()
        else:
            raise ValueError("Study leave not found")
    except Exception as e:
        raise e

def update_study_leave_accountant_response(db: Session, study_leave_id: int, response_data: schema.StudyLeaveAccountant):
    try:
        db_study_leave = db.query(model.StudyLeave).filter(model.StudyLeave.id == study_leave_id).first()
        if db_study_leave:
            db_study_leave.salary_cost = response_data.salary_cost
            db_study_leave.accountant_name = response_data.accountant_name
            db_study_leave.accountant_post = response_data.accountant_post
            db_study_leave.account_date = response_data.account_date
            db_study_leave.accountant_signature = response_data.accountant_signature
            db.commit()
        else:
            raise ValueError("Study leave not found")
    except Exception as e:
        raise e

def update_study_leave_hr_response(db: Session, study_leave_id: int, response_data: schema.StudyLeaveHR):
    try:
        db_study_leave = db.query(model.StudyLeave).filter(model.StudyLeave.id == study_leave_id).first()
        if db_study_leave:
            db_study_leave.approval_grant = response_data.approval_grant
            db_study_leave.grant_with_pay = response_data.grant_with_pay
            db_study_leave.granted_program = response_data.granted_program
            db_study_leave.years_after_resumption = response_data.years_after_resumption
            db_study_leave.certificate_upgrade = response_data.certificate_upgrade
            db_study_leave.beneficiary_number = response_data.beneficiary_number
            db_study_leave.applicant_not_supported = response_data.applicant_not_supported
            db_study_leave.hr_name = response_data.hr_name
            db_study_leave.hr_post = response_data.hr_post
            db_study_leave.hr_date = response_data.hr_date
            db_study_leave.hr_signature = response_data.hr_signature
            db.commit()
        else:
            raise ValueError("Study leave not found")
    except Exception as e:
        raise e

def update_study_leave_director_response(db: Session, study_leave_id: int, response_data: schema.StudyLeaveDirector):
    try:
        db_study_leave = db.query(model.StudyLeave).filter(model.StudyLeave.id == study_leave_id).first()
        if db_study_leave:
            db_study_leave.approval_status = response_data.approval_status
            db_study_leave.director_date = response_data.director_date
            db_study_leave.director_signature = response_data.director_signature
            db.commit()
        else:
            raise ValueError("Study leave not found")
    except Exception as e:
        raise e