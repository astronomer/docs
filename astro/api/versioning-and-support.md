---
title: Astro API versioning, maintenance, and support
sidebar_label: Support
id: versioning-and-support
---

The Astro API is currently in beta. The following policies apply to all beta versions of the Astro API.

## Releases and versioning

All API endpoints include a release name in their URL that determines which release of the API you use.

Each Astro API release name includes both a major version number and a release number, formatted as `<major-version>beta<release-number>`. For example, `v2beta3` is the third release of the second major version.

For a given release, Astronomer can make non-breaking changes in place without incrementing the release name. Astronomer can make breaking changes, also known as backward-incompatible changes, only between new releases. See [Version upgrades and breaking changes](#version-upgrades-and-breaking-changes).

## Deprecations

Astronomer reserves the right to mark specific API endpoints or features as deprecated within a given release. When an API endpoint is marked as deprecated, you will receive a notification and have 90 days to migrate away from the endpoint. After 90 days, Astronomer can make breaking changes to the endpoint, even within the same release. 

## Version upgrades and breaking changes

Any upgrade between versioned API releases can include breaking changes, including for non-deprecated endpoints. For example, an upgrade from `v1beta1` to `v1beta2` can include breaking changes. However, another release of `v1beta1` can include a breaking change to an endpoint only if the endpoint has been marked as deprecated for at least 90 days.

## API support

Astronomer offers support only for the two most recent releases at any given time. If you are on an earlier version that's out of support, you must upgrade to one of the two most recent versions to receive support. Support cases for beta releases of the Astro API are treated with lower priority than other generally available Astro features.

Astronomer reserves the right to shut down endpoints for a given beta release one year after all of its endpoints have equivalent functionality in a stable version.

