# Laser-LAN

# Code Name: Valor Strike

## Contents
- web ( site and API )
- app ( react native mobile app )

## Android release signing

The Android app includes a repo-local development release keystore for non-production builds:

- Keystore: `app/android/app/laserlan-dev-release.keystore`
- Config: `app/android/keystore.properties`

Build a signed release from `app/android` with:

```bash
./gradlew assembleRelease
```

For Play Store or other production distribution, replace this keystore with a private one that is not committed to the repo.

