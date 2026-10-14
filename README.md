# Calisthenics course booking MVP — client

**A visual walkthrough of discovering a training plan, paying for it, and reserving a session.**

React · TypeScript · Vite · Responsive UI · Separate Express API

This client is a prototype for an online and onsite calisthenics coaching service. Visitors can compare plans and inspect an order summary. A real API supports account registration, role-based sign-in, trainer account creation, and service status. Booking, payment, dashboard balances, and skill progress are interactive **demo flows with client-side sample data**; they are not connected to a booking or payment backend.

![Landing page with the calisthenics hero and training options](docs/01-home.webp)

## Get started

1. Install Node.js and npm. This snapshot was built with Node.js 24.
2. Start the [server](../server/README.md) with a MongoDB connection and its environment variables.
3. In `client/`, install dependencies and set the API base URL:

   ```sh
   npm ci
   ```

   Create `client/.env.local`:

   ```dotenv
   VITE_API_URL=http://localhost:5000/api
   ```

4. Start the client and open the URL printed by Vite (normally [http://localhost:5173](http://localhost:5173)):

   ```sh
   npm run dev
   ```

The landing page, plan comparison, and public skill tree render without the server. Registration, sign-in, admin trainer creation, and the status page require the API. `VITE_API_URL` is compiled into the client; rebuild after changing it for deployment. Do not place secrets in a `VITE_` variable.

## Use cases

The screenshots below come from the current built client, captured with Playwright at a 1440 × 900 viewport and 2× pixel density. Signed-in screenshots use a browser-only demo session with `/auth/me` mocked; no production account, booking, or payment was changed. The data shown in those pages is already hard-coded in the client.

### Compare online and onsite training

Open **Plans** from the landing page. Compare online and onsite offerings, their sample prices, durations, advantages, and considerations. Each **Select Plan** button opens an order summary. The prices and plan descriptions currently live in `src/pages/Plans.tsx`.

![Online and onsite training plan cards](docs/02-plans.webp)

### Review an order

Choose a plan, adjust the number of packages with **−** and **+**, and optionally enter an injury or allergy note. The total changes in the modal. **Proceed to Payment** sends a guest to user sign-in, then opens the visual payment flow. The selected package and note are not saved by an API.

![Order summary with package quantity, health note, and total](docs/03-order-summary.webp)

### Create an account or sign in

Open **Login** and choose **Create account** to register a user. Email and password sign-in uses separate user, trainer, and admin portals. Trainer accounts are created by an admin; an admin account can be bootstrapped from server environment variables. On successful sign-in, the client stores the token and user in browser local storage and checks `/auth/me` when the page reloads.

![User sign-in portal](docs/04-user-login.webp)

The visible **Forgot password?** and **Continue with Google** controls have no working backend flow in this MVP.

### Explore the trainee dashboard

The dashboard presents example upcoming training sessions, a schedule change, a coach contact dialog, and plan balances. These entries are fixed sample data and do not update when someone makes a booking or completes the payment demo.

![Trainee dashboard with sample sessions, coach contact, and balances](docs/05-dashboard.webp)

### Walk through a payment

The payment page lists sample transactions. Open one to inspect its details, view the draft agreement, confirm its terms, then see a **mock PromptPay QR** and choose an image file as a slip. Completing the flow changes the transaction status only in current page state. It does not charge money, upload the file, verify a transfer, or persist a transaction.

![Payment page with sample transactions and statuses](docs/06-payment.webp)

![Payment dialog showing the mock PromptPay QR and slip picker](docs/06-payment-qr.webp)

### Try the booking calendar

From a signed-in user or trainer session, open **Booking**. Select a trainer, click an available time, choose a sample plan, move the proposed slot if needed, and review the booking summary. The calendar shows seeded occupied slots for today and tomorrow, lunch blocking, and sample package balances. **Save Booking** shows a brief saved state only; refreshing resets the selection. No server-side reservation or conflict lock exists.

![Booking calendar with sample occupied times and trainer selection](docs/07-booking.webp)

![Booking summary with date, trainer, plan, and remaining sample balance](docs/07-booking-summary.webp)

### Browse the skill tree

The public `/skilltree` and `/skilltree/evaluate` routes show movement progress and evaluation views. Switch branches and open a skill to inspect details. Skill status, level, and XP are fixed in `src/components/skill-tree/data/skills.ts`; there is no account progress persistence.

![Skill tree branch and progress display](docs/08-skill-tree.webp)

## What is connected to the server?

| Flow | Current source of truth |
| --- | --- |
| Register, sign in, session check | Express API and MongoDB |
| Admin creates trainer account | Express API and MongoDB |
| Server/database/environment status | Express API |
| Plans and displayed prices | Client constants |
| Dashboard, payments, booking slots and balances | Client demo data |
| Skill tree and XP | Client demo data |

See the [server README](../server/README.md) for API routes and setup. The frontend sends the JWT as `Authorization: Bearer <token>`. The browser keeps it under the Zustand `auth-storage` key in local storage.

## Develop and hand off

```sh
npm run dev      # Vite development server
npm run build    # TypeScript check and production build into dist/
npm run preview  # Preview the production build
npm run lint     # ESLint
```

| Location | Purpose |
| --- | --- |
| `src/App.tsx` | Routes and role gates |
| `src/pages/` | Landing, plans, auth, dashboard, booking, payment, and status screens |
| `src/components/` | Navigation, order modal, skill tree, shared UI |
| `src/stores/auth.store.ts` | Auth API calls and persisted session |
| `src/stores/status.store.ts` | Status API state |
| `src/lib/axios.ts` | API base URL and bearer token interceptor |
| `docs/` | README screenshots and their capture script |

### Repository hierarchy

```text
client/
├── docs/                     # README screenshots and Playwright capture script
├── public/                   # Public SVG assets
├── src/
│   ├── assets/               # Imported images
│   ├── components/           # Navigation, modals, route guards, shared UI
│   │   └── skill-tree/       # Skill views, sample data, and visual components
│   ├── lib/                  # Axios client and utilities
│   ├── pages/                # Route-level screens
│   ├── stores/               # Auth and status state
│   ├── App.tsx               # Router and access rules
│   ├── index.css             # Global styles
│   └── main.tsx              # React entry point
├── AGENTS.md                 # Guidance for future coding agents
├── README.md                 # Setup, use cases, and MVP boundaries
├── package.json              # Scripts and dependencies
├── vite.config.ts            # Vite configuration
└── vercel.json               # SPA rewrite configuration
```

For a full booking product, the next team needs to define persistent plans, availability and time zones, reservation locking, package balance accounting, payment provider or slip review, coach workflows, notification policy, and privacy handling for health notes. The current UI supplies a concrete starting point for that work, not those production guarantees.

To recapture the screenshots after changing the UI, build the client, serve `dist/` at port 4173, then run `docs/capture_screenshots.py` with Python Playwright and Pillow installed. The script mocks a signed-in browser session for demo-only screens and writes the WebP files in `docs/`.

## License

Original code and documentation authored by Jakkarin Promsee are licensed under the [MIT License](LICENSE). Third-party code, assets, datasets, and other materials are not covered by this license; their original terms apply.
