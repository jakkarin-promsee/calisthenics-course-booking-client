# Client agent guide

This directory is the React + TypeScript/Vite frontend for the calisthenics course booking MVP. Read `README.md` first for user flows and current limits. The server is a separate Git repository in `../server/`.

## Ground rules

- Keep the distinction between real API behavior and demo-only UI explicit. Auth, trainer creation, and status use the API. Plans, payment, booking, dashboard, and skill progress currently use local constants/state.
- Do not describe the mock QR or slip picker as a real payment. Do not describe **Save Booking** as persistent until a booking API exists.
- Do not put credentials, JWT secrets, health notes from real people, or production URLs in screenshots, source constants, or committed environment files.
- `VITE_API_URL` must be the server's `/api` base, for example `http://localhost:5000/api`. Browser-exposed `VITE_` values are never secret.
- Preserve the existing route gates in `src/App.tsx` and the role check in `ProtectedRoute.tsx` when adding screens.

## Where to work

- Pages: `src/pages/`; navigation and shared UI: `src/components/`.
- HTTP client and bearer token: `src/lib/axios.ts`.
- Auth persistence and `/auth/me` revalidation: `src/stores/auth.store.ts`.
- Status polling: `src/stores/status.store.ts`.
- Skill tree sample data: `src/components/skill-tree/data/skills.ts`.
- README images: `docs/*.webp`; recapture with `docs/capture_screenshots.py` after visible changes.

## Before finishing a change

Run `npm run build` and `npm run lint` from this directory. Inspect the affected route in a browser when the change is visual. Keep README screenshots synchronized with visible UI. The current snapshot builds, while lint reports five existing errors in `button.tsx`, `AdminManageAccount.tsx`, `Login.tsx`, and `status.store.ts`; do not claim lint is clean without resolving them.

Use `npm ci` to reproduce the lockfile. Avoid adding dependencies for a documentation-only change. If extending the MVP into a real service, specify the API contract and persistence behavior with the server before removing the demo data.
