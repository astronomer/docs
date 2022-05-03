---
sidebar_label: 'Data Plane Activation'
title: 'Data Plane Activation'
id: 'data-plane-activation'
description: Prepare for the activation of your Astro Data Plane.
---

## Overview

Welcome to Astro! Astro is a modern data orchestration platform, powered by Apache Airflow, that enables your data team to build, run, and observe data pipelines. Astro includes a single-tenant Data Plane in your cloud and a multi-tenant Control Plane in Astronomer's cloud.

This document provides information about what to expect and prepare for when onboarding with our team.

<div class="text--center">
  <img src="/img/docs/architecture-overview.png" alt="High level overview of Astro's architecture" />
</div>

### What to Expect

We’re excited for you to get started with Astro. The first step is to activate your Data Plane, which follows a simple process that allows you to see our modern data orchestration infrastructure in action. Once complete, you'll be able to create Deployments, run tasks, and explore our suite of data observability features.

When you meet with one of our engineers to activate your Data Plane, you can expect it to take about an hour. By the end of the session, you'll have your first pipeline deployed in your own Astro environment.

### What to Bring and Know

Your Data Plane will be deployed into a clean AWS Account in accordance with [Amazon's recommendation](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/benefits-of-using-multiple-aws-accounts.html) for account segregation. With our fully managed service, our team takes complete responsibility for the operations of this account as described in the [Shared Responsibility Model](shared-responsibility-model.md).

This model enables us to get you started quickly and provides you with cloud-grade reliability and seamless connection to all of your data services.  If you decide to not proceed with Astro, this AWS account and all infrastructure running within it can be deleted in its entirety.

By default, your AWS account for the Astro Data Plane has no direct access to your data services. We’ll guide you on how to make these connections securely either through a VPC peering process or direct connections.

### Pre-Flight Checklist

Before your data plane activation meeting, please ensure that you have:

[] The [Astro CLI](install-cli.md) installed for any users who will develop pipelines.
[] A clean AWS Account
[] A user with the following permissions on that account:
   - `cloudformation:*`
   - `GetRole`
   - `GetRolePolicy`
   - `CreateRole`
   - `DeleteRolePolicy`
   - `PutRolePolicy`
   - `ListRoles`
   - `UpdateAssumeRolePolicy`
[] A desired AWS region for your Astro Cluster selected from the list of [supported regions](resource-reference-aws.md#aws-region).
[] _If peering VPCs_, a preferred subnet CIDR range identified that is no smaller than `/19`.

### What’s Next

Once your Data Plane is activated, you’ll be able to create new Deployments, deploy DAGs via the Astro CLI, and experience the differentiated Apache Airflow experience that is powered by Astro Runtime.

Our team at Astronomer is committed to helping you get started with Astro as quickly as possible and let your team focus their efforts on developing, testing, and running data pipelines. We’ll keep in touch following the Data Plane activation meeting to see how you’re doing, but don’t hesitate to reach out to us via Slack or email!
