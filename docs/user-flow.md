# User Flows

Three core journeys define Sanad. Each shows the path a user takes from start to finish.

---

## Flow 1: Seeker Books a Helper

```
Landing page
   ↓
Click "Sign up as Seeker"
   ↓
Enter email, password, name, phone
   ↓
Complete profile: disability type (permanent/temporary)
   and category (mobility/visual/hearing/cognitive/temporary injury)
   ↓
Land on Seeker Dashboard
   ↓
Click "Find a helper"
   ↓
Browse helpers list
   (Helpers matching seeker's disability category are marked "Recommended for you")
   (Filters available: service type, city, hourly rate, rating)
   ↓
Click a helper to view their profile
   (Profile shows: photo, bio, services, hourly rate, weekly availability,
    rating, reviews, completed task count)
   ↓
Click "Book this helper"
   ↓
Booking flow:
   • Select service from helper's offered services
   • Select date (calendar shows only days helper is available)
   • Select time slot (only times within helper's availability for that day)
   • Specify number of hours
   • Add notes (optional)
   ↓
See booking summary with total cost (hours × hourly rate)
   ↓
Click "Continue to payment"
   ↓
Checkout page:
   • Review summary
   • Enter mock payment details
   • Click "Pay now"
   ↓
Mock payment processing (2 sec spinner)
   ↓
Booking confirmed → Status: BOOKED + PAID
   ↓
See confirmation page with transaction ID and booking details
   ↓
On scheduled date → Status: ACTIVE
   ↓
Helper completes task in person
   ↓
Helper marks booking as completed → Status: COMPLETED
   ↓
Payment released to helper → Status: PAID OUT
   ↓
Seeker rates helper (1–5 stars + optional comment)
   ↓
Booking moves to history with receipt
```

### Cancellation Sub-Flow

```
Seeker views upcoming booking
   ↓
Click "Cancel booking"
   ↓
Confirm cancellation in modal
   ↓
Booking status: CANCELLED
   ↓
Refund triggered automatically
   ↓
Payment status: REFUNDED
   ↓
Confirmation shown to seeker
```

---

## Flow 2: Helper Onboarding & Setup

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
   • National ID
   • MoH authorization
   • Training certificates (optional)
   ↓
Submit application → Status: PENDING
   ↓
See "Your application is under review" screen
   ↓
[Admin reviews — see Flow 3]
   ↓
Receive notification of decision:
   • If APPROVED → Continue to profile setup
   • If REJECTED → See rejection reason, option to re-submit
   ↓
(If approved) Profile setup wizard:
   • Step 1: Select specialization areas (which disability categories)
   • Step 2: Select services offered (Groceries, Mobility, Medical, Household, Other)
   • Step 3: Set hourly rate (in SAR)
   • Step 4: Set weekly availability
       (Pick days of week + start/end time per day)
   • Step 5: Profile bio + photo (optional)
   ↓
Profile goes live → Status: ACTIVE
   ↓
Land on Helper Dashboard
   ↓
Wait for bookings to come in
   ↓
When booking arrives → Shows in "Upcoming bookings"
   ↓
On scheduled date → Booking status: ACTIVE
   ↓
Complete task in person → Click "Mark as completed"
   ↓
Payment released → Earnings updated
   ↓
Wait for seeker rating → View in profile
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
   • Personal info
   • Uploaded documents
   • Specialization claims
   ↓
Decision:
   ├── Click "Approve" → Helper status: APPROVED
   │     ↓
   │   Helper notified, can complete profile setup
   │
   └── Click "Reject" → Enter reason → Confirm
         ↓
       Helper status: REJECTED
         ↓
       Helper notified with rejection reason
   ↓
Return to queue → Process next application
```

---

## Status Reference

### Booking Statuses
- **BOOKED** — seeker has paid; helper sees it on dashboard
- **ACTIVE** — task is currently happening (scheduled time has arrived)
- **COMPLETED** — task finished, payment released, rated
- **CANCELLED** — seeker cancelled before scheduled time; refund processed

### Helper Verification Statuses
- **PENDING** — application submitted, awaiting admin review
- **APPROVED** — verified, can offer services and accept bookings
- **REJECTED** — declined, can re-submit
- **SUSPENDED** — previously approved but suspended

### Payment Statuses
- **PENDING** — checkout in progress
- **PAID** — payment captured, held in escrow
- **PAID_OUT** — released to helper after completion
- **REFUNDED** — returned to seeker (cancellation)
- **FAILED** — checkout failed