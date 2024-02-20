---
sidebar_label: "astro deployment wake-up"
title: "astro deployment wake-up"
id: astro-deployment-wake-up
description: Wake up a Deployment.
hide_table_of_contents: true
sidebar_custom_props: { icon: 'img/term-icon.png' }
---

Wake up an Astro development Deployment from hibernation. Overrides any existing hibernation schedule and sets the Deployment to run for a specific duration or until a specific time. 

## Usage

```sh
astro deployment hibernate [one of --until/ --for/ --resume-schedule]
```

## Options

| Option                   | Description                                                         | Possible Values                                      |
| ------------------------ | ------------------------------------------------------------------- | ---------------------------------------------------- |
| `-n`,`--deployment-name` | The name of the development Deployment to wake up.                  | Any valid Deployment name                            |
| `-u, --until`            | Specify the awake period using an end date and time.                | Any future date in the format `YYYY-MM-DDT00:00:00Z` |
| `-d, --for`              | Specify the awake period using a duration.                          | Any amount of time in the format `YhZm`            |
| `-r, --resume-schedule`  | Remove any overrides and resume regular hibernation schedule.       | None                                                 |
| `-f, --force`            | The CLI will not prompt to confirm before waking up the Deployment. | None                                                 |

## Related commands 

- [`astro deployment hibernate`](astro-deployment-hibernate.md)