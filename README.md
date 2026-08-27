 DeliFood — Full-Stack On-Demand Logistics & Food Platform



DeliFood is a multi-tenant food delivery and logistics web application engineered with Python, Django, and modern frontend technologies. The system isolates business logic across eight specialized domain applications to achieve high transaction speeds, strict server-to-server security verification, and smooth multi-role access control.

---

 Key Features & Highlights

- **Multi-Role User Ecosystem: Role-based access control (RBAC) isolating Customers, Restaurant Managers, and Courier Drivers.
- **Asynchronous Shopping Cart: Dynamic cart updates driven by background JavaScript `fetch()` operations without full page reloads.
- **Server-Verified Paystack Integration: Secure payment flow using Paystack Inline API with server-to-server transaction reference validation before clearing orders.
- **8-App Modular Architecture: Completely decoupled business components ensuring clean domain isolation and maintainability.
- **Automated State Cleanup: Smart post-payment hooks that transition order states to pending for kitchens while cleanly clearing customer shopping baskets.

---

 Project Architecture (8-App Ecosystem)


deliFood/
├── users/          # Custom User auth, role permissions, profiles, addresses
├── restaurant/     # Merchant management, operating hours, kitchen queue
├── menu/           # Categorized food catalog, dish items, pricing, media
├── cart/           # Shopping cart sessions, subtotals, item modification
├── orders/         # Transaction ledger, tracking numbers, status pipeline
├── payments/       # Paystack API integration, verify_payment backend logic
├── driver/         # Courier tracking, vehicle types, wallet payouts
└── delivery/       # Dispatching orchestrator, route assignment, handshakes


🛠️ Tech StackBackend:
Python 3.13, Django 6.x
Database: SQLite (Development) / PostgreSQL (Production)
Payment Gateway: Paystack Inline API
Frontend: HTML5, CSS3, Bootstrap 5, ES6 JavaScript (Fetch API)
Environment Management: python-dotenv


Installation and setup
git clone https://github.com/gift355/deliFood.git
cd deliFood

# Windows
python -m venv .deli
.deli\Scripts\activate

# macOS/Linux
python3 -m venv .deli
.deli/bin/activate

Install dependencies
pip install -r requirements.txt

Enviroment Configuration

Create a .env file in the root project directory and populate it with your environment keys
Code snippet
SECRET_KEY=your_django_secret_key_here
DEBUG=True
PAYSTACK_SECRET_KEY=sk_test_your_paystack_secret_key
PAYSTACK_PUBLIC_KEY=pk_test_your_paystack_public_key

Run Database Migration
python manage.py makemigrations
python manage.py migrate

Create a super user
python manage.py createsuperuser

Start the development server
python manage.py runserver
