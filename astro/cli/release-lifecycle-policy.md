---
sidebar_label: 'Release and lifecycle policy'
title: 'Astro CLI release and lifecycle policy'
id: release-lifecycle-policy
---

Astronomer regularly releases new versions of the Astro CLI that include new integrations with Astronomer products and local development features. To encourage users to regularly update the Astro CLI and to ensure stability across Astronomer products, the Astro CLI has a maintenance release lifecycle policy.

## Versioning and release channels

The Astro CLI uses semantic versioning, where each version of the CLI includes a major, minor, and patch number. The format of an Astro CLI version is `major.minor.patch`.

Each version of the Astro CLI belongs to one of two release channels:

- **Stable**: Releases in the stable channel are up to date and compatible with all current Astro and Astronomer Software functionality. The Astronomer team tests all new features against all stable Astro CLI releases.
- **Deprecated**: Releases in the deprecated channel are not guaranteed to work with all Astro and Astronomer Software functionality.

Go to [updates.astronomer.io](https://updates.astronomer.io/astro-cli) to see which versions are currently stable and deprecated.

Specifically, when a release is in the stable channel, the following is true:

- The version is tested regularly against new versions of Astronomer APIs.
- All Astro, Astronomer Software, and local use cases are supported.
- The release includes `stable` metadata in `https://updates.astronomer.io/astro-cli`.
- The release's binary is available on GitHub.
- The release can be installed from [install.astronomer.io](http://install.astronomer.io), `brew install astro` and, `winget install astro`.

When a release is in the deprecated channel, the following is true:

- Astro and Astronomer Software functionality can still work, but is not guaranteed to work. 
- If you're an Astronomer customer and reach out to support while using a deprecated version of the Astro CLI, Astronomer support will recommend that you upgrade the CLI as a first step.
- The release includes `deprecated` metadata in `https://updates.astronomer.io/astro-cli`.
- The release's binary is available on GitHub.
- The release can be installed from [install.astronomer.io](http://install.astronomer.io), `brew install astro` and, `winget install astro`.

## Astro CLI maintenance policy

The stable release channel contains only the latest patches of the three most recent minor versions of the Astro CLI. 

For example, consider a circumstance where the three most recent minor versions of the Astro CLI are 1.18, 1.19, and 1.20. Based on this maintenance policy:

- The latest patch versions for 1.18, 1.19, and 1.20 are all stable. These would be the only available stable releases for the Astro CLI.
- Say 1.20.1 is the current stable version and Astronomer releases version 1.20.2. This means 1.20.2 becomes the new stable version and version 1.20.1 becomes deprecated. This release has no impact on the stable 1.18 and 1.19 releases.
- If 1.21 releases, all versions of 1.18 are marked as deprecated. This release would have no impact on the channels of 1.19 and 1.20 releases. 

