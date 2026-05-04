# Sanad (سند)

> A trusted platform connecting people with disabilities to verified, government-authorized helpers — because asking for help shouldn't be hard.

## roblem Statement

People with permanent or temporary disabilities often need help with everyday tasks — getting groceries, moving between rooms, attending medical appointments, or running errands — but lack a reliable way to find trained, trustworthy helpers on demand. Family isn't always nearby, friends can't always come, and existing platforms aren't trained for disability-specific needs or vetted by health authorities.

Sanad was inspired by a real experience: a sprained ankle, a week of being unable to walk, and the awkwardness of repeatedly asking friends for help while living alone in a city far from family. That gap — between needing help and finding the *right* help — is what Sanad fills.

Sanad connects seekers (people needing help) with helpers who are authorized and verified by the Ministry of Health, ensuring every helper is trained, accountable, and equipped to support disability-specific needs.


## Features

### For Seekers (People with Disabilities)
- Create a profile with disability type (permanent or temporary) and category
- Browse all approved helpers, with helpers matching their disability category marked as "Recommended for you"
- Filter helpers by service type, city, hourly rate, and rating
- View any helper's full profile: services offered, weekly availability, ratings, reviews, hourly rate
- Book a specific helper for a specific service at a specific date/time within that helper's availability
- Pay upfront via secure checkout (held by platform until task completion)
- Receive automatic refund if the booking is cancelled before the scheduled time
- Track booking status (booked → active → completed)
- Rate helpers after task completion
- View booking history and download receipts

### For Helpers (Authorized Caregivers)
- Sign up and submit verification documents (national ID, training certifications, MoH authorization)
- Wait for admin verification before going active
- Set specialization areas (which disability categories they're trained to support)
- Choose which services they offer from a fixed list (Groceries, Mobility, Medical Appointments, Household, Other)
- Set personal hourly rate (one rate, applied to all services)
- Set recurring weekly availability (e.g. Mon–Wed 9am–5pm, Sat 2pm–8pm)
- View incoming bookings and confirm/cancel
- View earnings dashboard and completed task history
- Receive ratings from seekers

### For Admins (Ministry of Health Representatives)
- Review pending helper applications
- Verify uploaded documents
- Approve or reject helper accounts with feedback notes
- Suspend helpers based on poor ratings or complaints
- View platform-wide analytics

## Booking & Payment Model

Sanad uses a **direct booking** model with **upfront payment**:

1. Seeker browses approved helpers, filtered by what they need
2. Seeker views a helper's profile and picks a service + date + time slot from the helper's availability
3. Seeker pays upfront — funds held by the platform (escrow)
4. Helper sees the confirmed booking on their dashboard
5. After the scheduled task is completed, payment is released to the helper
6. If the seeker cancels before the scheduled time, the payment is fully refunded

**For the MVP:** Payment is simulated with a realistic checkout flow. Production would integrate Moyasar (Saudi-based payment gateway).

## Project Structure

```
sanad/
├── accounts/         # User authentication, profiles, role management (seeker/helper/admin)
├── verification/     # Helper document upload, MoH approval workflow
├── helpers/          # Helper profiles, services, availability, search & filtering
├── bookings/         # Booking creation, status tracking, cancellations
├── payments/         # Mock payment processing, escrow, refunds, transaction history
├── ratings/          # Ratings after booking completion
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

- **[Rimas]** — Backend (accounts, verification, payments, notifications)
- **[Ghadi]** — Backend (helpers, bookings, ratings, shared templates)


## Inspiration

Sanad was born from a personal moment of vulnerability — a sprained ankle, a week without mobility, and the realization that there's no easy way to ask for help when you're alone. We built this for everyone who has ever hesitated to ask.

