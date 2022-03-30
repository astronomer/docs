---
sidebar_label: 'Secrets Management'
title: "Secrets Management"
id: secrets-management
description: Learn how Astronomer secures your sensitive information and supports secrets management integration
---

## Overview

As the modern data orchestration service, Astro has been built and deployed with security as a guiding architectural principle. This same principle extends into how your sensitive information and credentials are stored and secured. Astro offers a managed secrets backend for encryption and storage of [secret environment variables](environment-variables.md#set-environment-variables-via-the-astronomer-ui), as well as [integration with popular secrets management](secrets-backend.md) tools.

All secrets management configuration performed in the Astronomer UI is [securely transmitted and stored](data-protection.md), is [resilient](resilience.md) to in-region cloud failures, and can be [recovered](disaster-recovery.md) in the case of a full Control and/or Data Plane disaster. For more information about how secret values are stored on Astro, see [How environment variables are stored on Astro](environment-variables.md#how-environment-variables-are-stored-on-astro).
