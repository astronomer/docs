---
sidebar_label: 'Data plane activation'
title: 'Data plane activation'
id: 'data-plane-activation'
description: Prepare for the activation of your Astro data plane.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Astro is a modern data orchestration platform, powered by Apache Airflow, that enables the entire data team to build, run, and observe data pipelines. The architecture of Astro includes a single-tenant data plane in your cloud and a multi-tenant control plane in Astronomer’s cloud.

![High level overview of Astro's architecture](/img/docs/architecture-overview.png)

### What to expect

We’re excited to get you started with Astro! The first step is to **activate your data plane**, which allows you to see our modern data orchestration experience hands-on.

When you meet with one of our engineers to activate your data plane, **expect it to take about an hour**. By the end of the session, you should have your first pipeline deployed in your own Astro environment!

### What to bring and know

Your data plane is deployed into a clean, dedicated AWS account or GCP project. Astronomer takes complete responsibility for the operations of this account as described in our [Shared responsibility model](shared-responsibility-model.md).

This model allows us to get you started quickly, providing cloud-grade reliability and seamless connection to all of your data services. If you decide not to proceed with Astro, this account can be deleted in its entirety.

By default, the Astronomer account has no access to your data services. We’ll guide you through how to make these connections securely, whether through peering VPCs or making direct connections.

### Pre-flight checklist

<Tabs
    defaultValue="aws"
    values={[
        {label: 'AWS', value: 'aws'},
        {label: 'GCP', value: 'gcp'},
    ]}>
<TabItem value="aws">

When you arrive at your data plane activation appointment, please ensure that you have:
- [ ] [Astro CLI](cli/get-started.md) installed for any users who will develop pipelines
- [ ] A clean AWS Account
- [ ] The following permissions to that AWS account:
  - `cloudformation:*`
  - `GetRole`
  - `GetRolePolicy`
  - `CreateRole`
  - `DeleteRolePolicy`
  - `PutRolePolicy`
  - `ListRoles`
  - `UpdateAssumeRolePolicy`
- [ ] A desired region for your Astro cluster, from the list of [supported regions](resource-reference-aws.md#aws-region)
- [ ] _If peering VPCs_, preferred subnet CIDR range identified (no smaller than a /19 range)

</TabItem>
<TabItem value="gcp">

When you arrive at your data plane activation appointment, please ensure you have:
- [ ] [Astro CLI](cli/get-started.md) installed for any users who will develop pipelines
- [ ] A clean GCP project
- [ ] A user with [Owner access](https://cloud.google.com/iam/docs/understanding-roles#basic-definitions) to your project
- [ ] A desired region for your Astro cluster, from the list of [supported regions](resource-reference-gcp.md#gcp-region)
- [ ] _If peering VPCs_, preferred subnet CIDR range identified (no smaller than a /19 range)

</TabItem>
</Tabs>

### What’s next

After your data plane is activated, you can spin up new Airflow environments, deploy pipelines through the Astro CLI, and experience an improved Airflow powered by Astro Runtime.

Our engineers want to help you get started quickly and get back to focusing on your pipelines. We’ll reach out in a few days to see how you’re doing, but don’t hesitate to reach out in the interim using Slack or e-mail.
