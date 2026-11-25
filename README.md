# Computer Upcycler v1.0.0

Give your old computer a new life. An independent browser-based installation companion for Ubuntu Desktop 24.04 LTS. Built by Buildiful®.

## Run / publish

No build step or dependencies. From this directory run `python3 -m http.server 8000` and open `http://localhost:8000/`. For GitHub Pages, put these files at the root of the `computer-upcycler` repository and enable Pages from the main branch root. The public header points to `https://buildiful.github.io/computer-upcycler/`.

## Scope

- Windows, conventional x86-64 Linux PCs, and non-T2 Intel Macs (try or replace only on Macs). Browser hints must be confirmed manually. ARM, Apple Silicon, T2, unknown/32-bit systems and unsupported dual-boot situations stop at the compatibility screen.
- Image writer links and instructions only; never writes a disk or downloads an ISO itself. The bootable USB is not a persistent external installation target.
- Local, dependency-free PNG and paginated PDF exports; take a copy to another device before restarting. The guide is not a substitute for model-specific firmware instructions, backups or verified hardware support.
- The pinned release page is Ubuntu Desktop 24.04.5.1 LTS. Review links, hardware requirements and installer changes on future releases.
- Settings are held in memory, not persisted. No system information is sent as analytics parameters.

## Branding and analytics deployment

Uses Buildiful Tool Shell v1.0 and the exact supplied Analytics v2.1.0 module with the supplied GA4 ID, configured in both HTML pages. The approved white logo and favicon files are included. GA4 is restricted to buildiful.github.io, respects supported privacy signals, and requires an affirmative choice where required or where region detection fails. Only basic action names are tracked; no guide selections are sent as custom parameters. See ANALYTICS.md and privacy.html. Verify GA4 property settings and regional requirements before publication.

Raspberry Pi is a separate board-specific installation path, not supported by this wizard. The start screen links to Raspberry Pi Imager for users who prefer experimenting on a spare board.

## Official references

- https://ubuntu.com/desktop/docs/en/24.04/tutorial/install-ubuntu-desktop/
- https://ubuntu.com/desktop/docs/en/24.04/how-to/create-a-bootable-usb-stick/
- https://releases.ubuntu.com/24.04.5.1/
- https://canonical.com/legal/intellectual-property-policy
- https://wiki.t2linux.org/distributions/ubuntu/installation/

Ubuntu is a trademark of Canonical Ltd. Computer Upcycler is independent and not endorsed by Canonical. Application source is MIT-licensed; Buildiful brand assets are excluded (see LICENSE and TRADEMARKS.md).
