# Sanad (سند)

> A trusted platform connecting people with disabilities to verified, government-authorized helpers — because asking for help shouldn't be hard.

## roblem Statement

People with permanent or temporary disabilities often need help with everyday tasks — getting groceries, moving between rooms, attending medical appointments, or running errands — but lack a reliable way to find trained, trustworthy helpers on demand. Family isn't always nearby, friends can't always come, and existing platforms aren't trained for disability-specific needs or vetted by health authorities.

Sanad was inspired by a real experience: a sprained ankle, a week of being unable to walk, and the awkwardness of repeatedly asking friends for help while living alone in a city far from family. That gap — between needing help and finding the *right* help — is what Sanad fills.

Sanad connects seekers (people needing help) with helpers who are authorized and verified by the Ministry of Health, ensuring every helper is trained, accountable, and equipped to support disability-specific needs.


##  Features

### For Seekers (People with Disabilities)
- Create a profile with disability type (permanent or temporary) and specific needs
- Post help requests with task type, date/time, location, estimated hours, and notes
- Browse and filter approved helpers by specialization and hourly rate
- View helper offers with their hourly rate and total estimated cost
- Pay upfront via secure checkout when accepting a helper
- Receive automatic refund if request is cancelled before the task starts
- Track request status (open → accepted → paid → active → completed)
- Rate helpers after task completion
- View payment history and download receipts
- Receive in-app notifications for status and payment updates

### For Helpers (Authorized Caregivers)
- Sign up and submit verification documents (national ID, training certifications, MoH authorization)
- Wait for admin verification before going active
- Set specialization areas (which disabilities they're trained to support)
- Set personal hourly rate (adjustable anytime)
- Browse open help requests by location and type
- See estimated earnings per request before offering
- Accept requests; receive payment after task completion
- View earnings dashboard, completed task history, and payouts
- Receive ratings from seekers

### For Admins (Ministry of Health Representatives)
- Review pending helper applications
- Verify uploaded documents
- Approve or reject helper accounts with feedback notes
- Suspend helpers based on poor ratings or complaints
- View platform-wide analytics: active users, completed requests, total transaction volume, average ratings
- Process refund disputes when needed

## Payment Model

Sanad uses an **upfront payment with refund** model:

1. Seeker creates a request and reviews helper offers
2. When seeker accepts a helper, payment is processed for the estimated hours × hourly rate
3. Funds are held by the platform (escrow) until task completion
4. After completion, payment is released to the helper
5. If the seeker cancels before the task starts, the payment is refunded automatically
6. If the helper cancels, full refund + the helper's reliability score is impacted

**For the MVP:** Payment is simulated with a realistic checkout flow. Production deployment would integrate **Moyasar** (Saudi-based payment gateway supporting Mada, Visa, Mastercard, and Apple Pay).


## Project Structure

```
sanad/
├── accounts/         # User authentication, profiles, role management (seeker/helper/admin)
├── verification/     # Helper document upload, MoH approval workflow
├── requests/         # Help request creation, acceptance, status tracking
├── payments/         # Mock payment processing, escrow, refunds, transaction history
├── ratings/          # Two-way ratings after task completion
├── notifications/    # In-app notifications for status changes
├── templates/        # Shared base templates
├── static/           # CSS, JS, images
├── media/            # User-uploaded files (verification docs, profile photos)
└── sanad/            # Project settings
```


## Documentation

- **User Stories:** [docs/user-stories.md](docs/user-stories.md)
- **User Personas:** [docs/personas.md](docs/personas.md)
- **User Flow:** [docs/user-flow.md](docs/user-flow.md)
- **UML Diagram:** [docs/uml.png](docs/uml.png)
- **Wireframes:** [docs/wireframes/](docs/wireframes/)

## Team

- **[Ghadi]** — Backend (accounts, verification, payments, notifications)
- **[Rimas]** — Backend (requests, ratings, shared templates)


## Inspiration

Sanad was born from a personal moment of vulnerability — a sprained ankle, a week without mobility, and the realization that there's no easy way to ask for help when you're alone. We built this for everyone who has ever hesitated to ask.

