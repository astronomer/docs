---
title: "Upgrading Astro Runtime"
sidebar_label: "Upgrading Astro"
description: "How to upgrade your version of Astro Runtime safely and rollback if necessary."
id: upgrading-astro
---

Astro includes features that make upgrading to the latest version of Astro Runtime easy and, more importantly, safe. There are a few best practices to keep in mind when taking advantage of these features to ensure that your deployments remain stable and current with the latest fixes and improvements.

## Feature overview

In this guide, you'll learn:

- How to use the [Astro CLI](https://docs.astronomer.io/cli/overview.md) to test an Astro project against a higher version of Astro Runtime for dependency conflicts and import errors prior to upgrading. 
- How to use the Astro UI to perform a rollback to an earlier deployment and Runtime version in an emergency.

## Best practice guidance

Keeping the version of Astro Runtime in your projects up to date is highly recommended as new versions are released regularly to apply bug fixes, security fixes, and improvements not only to Astro but also the underlying Airflow package.

Upgrades can apply breaking changes, especially in the case of new major versions. The Astro CLI has built-in functionality to identify and help resolve negative impacts of breaking changes. Using this feature prior to upgrades is highly recommended.

In the case of emergencies, the Astro UI supports rollbacks to previous deployments including automatic version downgrading. Astro's rollback functionality is akin to Git's `revert` feature and makes use of the UI's deploy history. Rollbacks revert project code only, keeping environment variables and other configuration unchanged. Also, any data related to newer features is erased when downgrading. For these reasons, we recommend viewing rollbacks as a measure of last resort only. 

## Assumed knowledge

To get the most out of this guide, you have a basic understanding of:

- The [Astro CLI](https://docs.astronomer.io/cli/overview.md).
- Creating and managing [Deployment](https://docs.astronomer.io/astro/create-deployment)s on Astro.

## Testing upgrades using the Astro CLI



## Rolling back deployments in the case of emergencies

