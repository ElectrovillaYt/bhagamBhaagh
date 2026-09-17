# Bhagam Bhaagh — Next.js App

The web client for **Bhagam Bhaagh**, a location-aware map experience. It renders an interactive MapLibre map, centers it on the visitor when location access is granted, and retrieves its map style through the project's backend.

> Project status: under active development. See [Desgin.md](./Desgin.md) for the working design and [PROJECT_PROGRESS.md](./PROJECT_PROGRESS.md) for the implementation tracker.

## Current features

- Full-screen interactive map powered by MapLibre GL.
- Browser geolocation on initial load, with a world-map fallback when permission is unavailable.
- Map style fetched from the backend instead of exposing the MapTiler key in the browser.
- Zoom, fullscreen, and navigation controls.
- Viewport data collection on map movement (zoom and bounding box).
- Next.js route handlers that proxy map requests to the backend.

Authentication, profiles, gameplay, and persistent viewport handling are scaffolded but not yet implemented.

## Tech stack

- Next.js 16, React 19, TypeScript
- Tailwind CSS 4
- MapLibre GL
- FastAPI backend (in the sibling `../backend` directory)

## Prerequisites

- Node.js 20.9 or later
- npm
- A running Bhagam Bhaagh backend with a configured MapTiler API key

## Local setup

1. Install frontend dependencies:

   ```bash
   npm install
   ```

2. Create a `.env.local` file in this directory:

   ```env
   BACKEND_URL=http://localhost:8000/api/v1
   ```

   `BACKEND_URL` must include the backend API prefix. The current backend map router is mounted at `/api/v1/map`.

3. Start the backend from `../backend` (see its README). Ensure its MapTiler key is configured.

4. Start the frontend:

   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000). Allow location access to start near your current position.

## Available scripts

| Command | Purpose |
| --- | --- |
| `npm run dev` | Start the development server. |
| `npm run build` | Create a production build. |
| `npm run start` | Run the production server after building. |
| `npm run lint` | Run ESLint. |

## Request flow

```text
Browser → Next.js /routes/get-tiles → FastAPI /api/v1/map/tiles → MapTiler style JSON
Browser → MapLibre GL → rendered interactive map
Browser → Next.js /routes/send-view → backend viewport endpoint (in progress)
```

The browser never calls MapTiler directly; the backend owns the API key and returns the style payload.

## Project structure

```text
src/
├── app/                 # App Router entry points and server route handlers
├── components/          # Reusable UI and map components
├── lib/                 # Shared error classes
├── pages/               # Feature-level page components
└── utils/Map/           # Geolocation, tile, and viewport client helpers
```

## API integration

| Frontend route | Upstream backend route | State |
| --- | --- | --- |
| `GET /routes/get-tiles` | `GET /api/v1/map/tiles` | Implemented |
| `POST /routes/send-view` | `POST /api/v1/map/viewport` | Frontend scaffolded; backend route pending |

## Notes for contributors

- Keep credentials in environment files; do not commit `.env.local` or MapTiler keys.
- Map rendering is a client-side concern because it requires the browser DOM and geolocation API.
- Update [PROJECT_PROGRESS.md](./PROJECT_PROGRESS.md) as work moves between planned, in-progress, and complete.
