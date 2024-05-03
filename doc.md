Staff:
- Logs in: (Done via the `user\login` endpoint)
- Receive documents from offices (Done via the `messages/inbox` endpoint)
- Get Feedback on appraisals ??
- Upload a document and send to: (Done via the `messages/upload-document` endpoint)
    an office: head teacher, admin etc 
    they can get a comment on a document (Done. View comments from `messages/inbox` endpoint)
- Request for leave - a file can be attached with the request: (Done via the `messages/request-leave` endpoint)
    requests can be shared with an office
    leaves can be accepted, rejected or accepted without pay 
    staff can see leave request status (Done. view status via the `messages/inbox` endpoint)
    
Head of Sections:
- Make comments documents shared (Done. Send comment via the `messages/comment` endpoint)
- Make comments on leave requests (Done. Send comment via the `messages/comment` endpoint)
- They can share leave requests with the next office (Done. Share Leave Request via the `messages/share-leave-request` endpoint)
- Perform appraisal on a staff ??

Admin:
- Share documents with staff (Done via the `messages/upload-document` endpoint)
- Perform Appraisals on a staff ??
- Approve, Disapprove leave requests (Done via the `messages/respond-to-leave-request` endpoint)
- Registers All Users (Done via the `user/signup` enpoint)
- Define Work Hours for each staff (Done via the `user/set-working-period` endpoint)
- Register Offices (Done via the `offices/register-office` endpoint)
- Assign Head of Offices (Done via the `offices/assign-hofo` endpoint)
- Has access to all generated reports (Done via the `generate-report/` endpoint)

HR:
- Registers All Users (Done via the `user/signup` enpoint)
- Define Work Hours for each staff (Done via the `user/set-working-period` endpoint)
- Register Offices (Done via the `offices/register-office` endpoint)
- Assign Head of Offices (Done via the `offices/assign-hofo` endpoint)
- HR has access to all leave requests (Done via the `messages/view-all-leave-requests` enpoint)
- Generate Report on: (Done via the `generate-report/` endpoint)
    - Leave of Absence
    - Informed late arrival
    - Early Closure
    - Movement
- Generate annual report on cummulative leaves ??
