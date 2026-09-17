# Project Progress

**Last reviewed:** 17 September 2026  
**Overall status:** Map foundation is in place; account, gameplay, and viewport persistence remain in progress.

## Snapshot

| Area | Status | Notes |
| --- | --- | --- |
| Next.js application shell | Complete | App Router entry point and global styling are present. |
| Interactive map | Complete | MapLibre map, fullscreen, and navigation controls are configured. |
| Geolocation fallback | Complete | Uses browser coordinates when available, otherwise starts on a world view. |
| Map-style delivery | Complete | Next.js route proxies the request to the backend map service. |
| Error classes | Complete | Shared application, validation, authorization, and not-found error types exist. |
| Viewport capture | In progress | Client captures zoom and bounding box after `moveend`. |
| Viewport backend integration | Blocked / pending | Frontend route expects `/api/v1/map/viewport`; the backend map module currently exposes only `/tiles`. |
| Authentication screens | Not started | Login, registration, and reset components are empty placeholders. |
| Protected-route enforcement | Not started | Protected layout contains planning comments only. |
| Profile | Not started | Profile component is empty. |
| Product/game mechanics | Not started | No player, task, scoring, or game-state behavior is implemented in this app. |
| Automated tests | Not started | No test files are currently present in the frontend. |

## Completed work

- Created the Next.js/TypeScript application structure.
- Added MapLibre GL as the interactive map renderer.
- Built a map component that prevents duplicate initialization and removes the map instance on cleanup.
- Added browser geolocation with high-accuracy, timeout, and fallback behavior.
- Added `GET /routes/get-tiles` to proxy the backend map-style response.
- Kept MapTiler configuration in the backend flow rather than placing its key in client-side code.
- Added reusable error types and a basic universal-button component.

## Work in progress

- Connecting map viewport updates to a working backend endpoint.
- Converting raw console errors into visible loading and error states.
- Refining the landing/dashboard component structure around the map.
- Documenting the evolving product experience in [Desgin.md](./Desgin.md).

## Next milestones

1. Implement `POST /api/v1/map/viewport` in the backend, then forward the request body from the Next.js `send-view` route.
2. Add client-side validation and `Content-Type: application/json` for viewport submissions.
3. Add a loading, permission-denied, and map-style-error state to the map screen.
4. Implement authentication UI, session handling, and protected-route redirects.
5. Build the profile experience.
6. Define and implement the first game loop and its map overlays.
7. Add unit/integration tests for route handlers and map utility functions.

## Known gaps and technical notes

- The current `send-view` route reads `zoom` and `bbox`, but its upstream fetch does not yet forward them to the backend.
- The backend route referenced by the frontend (`/api/v1/map/viewport`) is not present in the current backend map router.
- Map initialization errors are logged to the browser console; they are not yet surfaced in the UI.
- Auth and profile files are scaffolds, not functional screens.

## Definition of done for the current map milestone

- [x] Render an interactive map.
- [x] Obtain map style without exposing the MapTiler key in the browser.
- [x] Use current location when permission is granted.
- [x] Provide a usable fallback when location is unavailable.
- [ ] Persist or meaningfully consume viewport updates.
- [ ] Show clear user-facing loading and failure feedback.
- [ ] Cover primary map and proxy-route behavior with tests.
