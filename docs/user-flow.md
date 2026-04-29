# User Flows

Three core journeys define Sanad. Each flow shows the step-by-step path a user takes from start to finish.

---

## Flow 1: Seeker Requests Help 

```
Landing page
   ↓
Click "Sign up as Seeker"
   ↓
Enter email, password, name, phone
   ↓
Complete profile: select disability type (permanent/temporary)
   and category (mobility/visual/hearing/cognitive/temporary injury)
   ↓
Land on Seeker Dashboard
   ↓
Click "Create New Request"
   ↓
Fill form: task type, date, time, location, estimated hours, notes
   ↓
Submit → Request status: OPEN
   ↓
Wait for helpers to offer
   ↓
View list of helpers who offered
   (each card shows: rating, specializations, hourly rate, total estimated cost)
   ↓
Click "Choose this helper" on one
   ↓
Redirected to Checkout Page
   ↓
Review payment summary:
   • Helper name + rate
   • Estimated hours
   • Total amount (SAR)
   ↓
Enter payment details (mock card form)
   ↓
Click "Pay Now" → Mock processing (2 sec spinner)
   ↓
Payment confirmed → Request status: ACCEPTED + PAID
   ↓
Receive confirmation page with transaction ID
   ↓
On scheduled date → Request status: ACTIVE
   ↓
Helper completes task in person
   ↓
Click "Mark as completed" → Request status: COMPLETED
   ↓
Payment released to helper (status: PAID OUT)
   ↓
Rate helper (1–5 stars + optional comment)
   ↓
Return to dashboard, see request in history with receipt
```

### Cancellation Sub-Flow

```
Seeker on accepted/paid request
   ↓
Click "Cancel Request"
   ↓
Confirm cancellation in modal
   ↓
Request status: CANCELLED
   ↓
Refund triggered automatically
   ↓
Payment status: REFUNDED
   ↓
Seeker sees confirmation of refund
```

---

## Flow 2: Helper Onboarding & Verification

```
Landing page
   ↓
Click "Sign up as Helper"
   ↓
Enter email, password, name, phone
   ↓
Land on Helper Onboarding screen
   ↓
Upload documents:
   • National ID (front + back)
   • MoH authorization certificate
   • Training certificates (optional but recommended)
   ↓
Submit application → Status: PENDING
   ↓
See "Your application is under review" screen
   ↓
[Admin reviews — see Flow 3]
   ↓
Receive notification of decision:
   • If APPROVED → Continue to specialization setup
   • If REJECTED → See rejection reason, option to re-submit
   ↓
(If approved) Select specialization areas
   (mobility, visual, hearing, cognitive, temporary injury)
   ↓
Land on Helper Dashboard → Status: ACTIVE
   ↓
Browse open requests filtered by specialization and location
   ↓
Click a request → View details → Click "Offer to help"
   ↓
Wait for seeker to accept
   ↓
If accepted → Request appears in "My Active Tasks"
   ↓
Complete task in person → Click "Mark as completed"
   ↓
Wait for seeker to confirm + rate
   ↓
View rating in profile
```

---

## Flow 3: Admin Verifies a Helper

```
Admin login page
   ↓
Enter admin credentials
   ↓
Land on Admin Dashboard
   ↓
See pending applications count → Click "Review Applications"
   ↓
View queue of pending helpers (sorted by submission date)
   ↓
Click a helper's row → Open application detail page
   ↓
Review:
   • Personal info (name, email, phone)
   • Uploaded documents (view/download each)
   • Specialization claims
   ↓
Decision:
   ├── Click "Approve" → Helper status: APPROVED
   │      ↓
   │   Helper receives notification, can now accept requests
   │
   └── Click "Reject" → Enter reason in text field → Confirm
          ↓
       Helper status: REJECTED
          ↓
       Helper receives notification with rejection reason
   ↓
Return to queue → Process next application
```

---

## Status Reference

### Help Request Statuses
- **OPEN** — created, waiting for helper offers
- **ACCEPTED** — seeker has chosen a helper AND paid; scheduled
- **ACTIVE** — task is currently happening
- **COMPLETED** — task finished, payment released, rated
- **CANCELLED** — seeker or helper cancelled; refund processed

### Helper Verification Statuses
- **PENDING** — application submitted, awaiting admin review
- **APPROVED** — verified, can accept requests
- **REJECTED** — declined, can re-submit with corrections
- **SUSPENDED** — previously approved but suspended due to issues

### Payment Statuses
- **PENDING** — checkout in progress
- **PAID** — payment captured, held in escrow
- **PAID_OUT** — released to helper after task completion
- **REFUNDED** — returned to seeker (cancellation)
- **FAILED** — checkout failed