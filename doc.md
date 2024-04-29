Staff:
- Logs in: (Done via `user\login` endpoint)
- Receive documents from offices (Done via `messages/inbox` endpoint)
- Get Feedback on appraisals ??
- Upload a document and send to: (Done via `messages/upload-document` endpoint)
    an office: head teacher, admin etc 
    they can get a comment on a document (Done. View comments from `messages/inbox` endpoint)
- Request for leave - a file can be attached with the request: (Done via `messages/request-leave` endpoint)
    requests can be shared with an office
    leaves can be accepted, rejected or accepted without pay 
    staff can see leave request status (Done. view status via `messages/inbox` endpoint)
    
Head of Sections:
- Make comments documents shared (Done. Send comment via `messages/comment` endpoint)
- Make comments on leave requests (Done. Send comment via `messages/comment` endpoint)
- They can share leave requests with the next office ??
- Perform appraisal on a staff ??

Admin:
- Share documents with staff (Done via `messages/upload-document` endpoint)
- Perform Appraisals on a staff ??
- Approve, Disapprove leave requests (Done via `messages/respond-to-leave-request` endpoint)
- Registers All Users (Done via `user/signup` enpoint)
- Define Work Hours for each staff (Done via `user/set-working-period` endpoint)
- Register Offices ??
- Assign Head of Offices ??
- Has access to all generated reports ??

HR:
- Registers All Users (Done via `user/signup` enpoint)
- Define Work Hours for each staff (Done via `user/set-working-period` endpoint)
- Register Offices ??
- Assign Head of Offices ??
- HR has access to all leave requests (Done via `messages/view-all-leave-requests` enpoint)
- Generate Report on: ??
    - Leave of Absence
    - Informed late arrival
    - Early Closure
    - Movement
- Generate annual report on cummulative leaves ??
