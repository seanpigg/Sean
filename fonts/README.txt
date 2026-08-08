OPTIONAL — Bundle the Inter font for the most polished look
===========================================================
The app already looks sharp WITHOUT this (it falls back to Segoe UI / system
fonts automatically). To activate Inter, drop these 4 files into THIS folder
(static/fonts/), exact names:

    Inter-Regular.woff2
    Inter-Medium.woff2
    Inter-SemiBold.woff2
    Inter-Bold.woff2

Where to get them (free, OFL license):
  - https://rsms.me/inter/   (Download → the "web" woff2 files), or
  - https://fonts.google.com/specimen/Inter

If your machine blocks those, grab the 4 files on any unfiltered device and
copy them over. No code change needed — the app picks them up on next refresh.
If the files aren't here, nothing breaks; it uses the system font stack.
