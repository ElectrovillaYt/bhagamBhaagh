# Bhagam Bhaagh — Design (Under Progress)

**Document status:** Working design. This records the intended direction and the functionality that exists today; it is not a final product specification.

## Product intent

Bhagam Bhaagh is being built as a map-first, location-aware experience. A player should be able to open the app, understand their position in the world, and eventually use location and game state to participate in nearby activity.

The first delivered slice is the map foundation: reliable style delivery, safe key handling, browser-location centering, and viewport awareness.

## Design principles

- **Map first:** the map occupies the available viewport and is the primary interaction surface.
- **Privacy conscious:** location is requested by the browser, only used after permission, and falls back gracefully.
- **Secrets stay server-side:** third-party map credentials remain in the backend.
- **Progressive enhancement:** the application still renders a global map when geolocation is denied or unavailable.
- **Clear boundaries:** UI, Next.js proxy routes, and backend services each have focused responsibilities.

## Current experience

1. The visitor opens the root page.
2. The dashboard renders a full-screen map container.
3. The client requests a map style through `GET /routes/get-tiles`.
4. The client requests browser geolocation.
5. MapLibre initializes at the visitor's coordinates and zoom level 15 when available; otherwise it starts at `[0, 0]` and zoom level 2.
6. The user can pan, zoom, or use fullscreen/navigation controls.
7. After a movement ends, the client captures the zoom and visible bounding box for future game or analytics use.

## Architecture

```text
┌───────────────┐     same-origin proxy      ┌─────────────────┐
│ Next.js UI    │ ─────────────────────────► │ Next.js routes  │
│ MapLibre map  │                            │ /routes/*       │
└──────┬────────┘                            └────────┬────────┘
       │ browser geolocation                            │ BACKEND_URL
       ▼                                                 ▼
┌───────────────┐                            ┌─────────────────┐
│ User browser  │                            │ FastAPI backend │
└───────────────┘                            │ /api/v1/map     │
                                                 └────────┬────────┘
                                                          ▼
                                                    ┌──────────┐
                                                    │ MapTiler │
                                                    └──────────┘
```

### Responsibilities

| Layer | Responsibility |
| --- | --- |
| `src/components/MapView/Map.tsx` | Creates and configures the client-side MapLibre instance. |
| `src/utils/Map/LocationFetcher` | Requests and normalizes browser coordinates. |
| `src/utils/Map/Tiler` | Fetches map-style data through the Next.js route handler. |
| `src/utils/Map/ViewStats` | Sends zoom and bounding-box state after map movement. |
| `src/app/routes/*` | Proxies frontend requests to the backend and keeps upstream details server-side. |
| FastAPI map module | Retrieves the MapTiler style using a server-held key. |

## Proposed screen model

| Screen | Purpose | State |
| --- | --- | --- |
| Home / dashboard | Primary full-screen map view. | Implemented foundation |
| Login | Sign-in entry point. | Placeholder |
| Register | Account creation. | Placeholder |
| Password reset | Account recovery. | Placeholder |
| Profile | Player identity and settings. | Placeholder |

## Interaction and state design

- **Location permission granted:** center on the coordinates returned by the browser.
- **Location permission denied, timeout, or unavailable:** show the global fallback map without blocking use.
- **Map style request fails:** report a client error and avoid rendering a broken map state; a user-facing error treatment is still needed.
- **Map movement ends:** capture `{ zoom, bbox }`, where `bbox` is `[west, south, east, north]`.
- **Viewport persistence:** intended for a future backend endpoint. It is not currently persisted.

## Accessibility and responsive direction

- Preserve a full-viewport map on desktop and mobile.
- Keep map controls reachable at narrow widths and when fullscreen is active.
- Add keyboard-accessible application controls, text alternatives, focus states, and status messages as account/game UI is introduced.
- Avoid making geolocation permission a prerequisite for accessing the product.

## Open design decisions

- What is the player’s primary map action: discovery, check-in, race/task participation, or social play?
- Which viewport events should be stored, and for how long?
- What information belongs as persistent map overlays versus temporary panels?
- How should location consent, precision, and retention be explained to players?
- What are the loading, empty, and failure states for map style and game data?
