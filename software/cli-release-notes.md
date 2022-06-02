---
sidebar_label: 'Astro CLI'
title: 'Astro CLI Release Notes'
id: cli-release-notes
description: Release notes for the Astro CLI.
---

## Overview

This document provides a summary of all changes made to the [Astro CLI](install-cli.md) for the v0.28.x series of Astronomer Software. For general product release notes, see [Astronomer Software Release Notes](release-notes.md).

If you have any questions or a bug to report, reach out to us via [Astronomer Support](https://support.astronomer.io).

## Astro CLI v0.29

Release date: June 1, 2022

### Create New Projects With Astro Runtime Images

`astro dev init` now initializes Astro projects with Astro Runtime images by default. By default, your project initializes with the latest available Runtime version. To use a specific Runtime version, you can run: 

```sh
astro dev init --runtime-version <runtime-version>
```

If you want to continue using Astronomer Certified images in your new Astro projects

```sh
astro dev init --use astronomer-certified
```
