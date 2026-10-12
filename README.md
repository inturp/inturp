# Inturp website

Published with GitHub Pages at https://inturp.com/.

- `/`: Inturp home
- `/about/`: About and founders
- `/vet-charted/`: Vet Charted product website (maintained separately)
- `/vetcharted/`: Inturp product overview

The Inturp React/TanStack source is in `website-source/`.
To rebuild from that directory:

```sh
npm ci
npm run build
python3 publish-local.py
```

Commit the generated root files with source updates. Preserve `CNAME`, `.nojekyll`, and `vet-charted/` when publishing. HTTPS is enforced in repository Pages settings.
