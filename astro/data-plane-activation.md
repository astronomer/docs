---
sidebar_label: 'Data Plane Activation'
title: 'Data Plane Activation'
id: 'data-plane-activation'
description: Prepare for the activation of your data plane
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';


Astro is a modern data orchestration platform, powered by Apache Airflow, that enables the entire data team to build, run, and observe data pipelines. The **architecture of Astro** includes a single-tenant Data Plane in your cloud and a multi-tenant control plane in Astronomer’s cloud.

<div class="text--center">
  <img src="/img/docs/architecture-overview.png" alt="High level overview of Astro's architecture" />
</div>

### What to Expect
We’re excited to get you started with Astro! Getting your data plane activated is simple and will allow you to see our modern data orchestration experience hands-on.
When you meet with one of our engineers to activate your data plane, **expect it to take about an hour**. By the end of the session, you should have your **first pipeline deployed in your own Astro environment**!

### What to Bring and Know
Your data plane will be deployed into a clean, dedicated AWS account or GCP project. With our fully managed service, we’ll take complete responsibility for the operations of this account, as described in our [Shared Responsibility Model](shared-responsibility-model.md).
This model allows us to get you started quickly, providing cloud-grade reliability and seamless connection to all of your data services. If you decide not to proceed with Astro, this account can be deleted in its entirety.
By default, the Astronomer account has no access to your data services. We’ll guide you through how to make these connections securely, whether peering VPCs or making direct connections.

### Pre-Flight Checklist

<Tabs
    defaultValue="aws"
    values={[
        {label: 'AWS', value: 'aws'},
        {label: 'GCP', value: 'gcp'},
    ]}>
<TabItem value="aws">

When you arrive at your data plane activation appointment, please ensure you have:
- [ ] [Astro CLI](install-cli.md) installed for any users who will develop pipelines
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
- [ ] Desired region for Astro Cluster deployment identified, from the list of [supported regions](resource-reference-aws.md#aws-region)
- [ ] _If peering VPCs_, preferred subnet CIDR range identified (no smaller than a /19 range)

</TabItem>
<TabItem value="gcp">

When you arrive at your data plane activation appointment, please ensure you have:
- [ ] [Astro CLI](install-cli.md) installed for any users who will develop pipelines
- [ ] A clean GCP project
- [ ] A user with [Owner access](https://cloud.google.com/iam/docs/understanding-roles#basic-definitions) to your project
- [ ] Desired region for Astro Cluster deployment identified, from the list of [supported regions](resource-reference-gcp.md#gcp-region)
- [ ] _If peering VPCs_, preferred subnet CIDR range identified (no smaller than a /19 range)

</TabItem>
</Tabs>

### What’s Next
After your data plane is activated, you’ll be able to spin up new Airflow environments, deploy pipelines through Astro CLI, and witness the power of Astro Runtime.
Our engineers want to help you get started quickly, and get back to focusing on your pipelines. We’ll reach out in a few days to see how you’re doing, but don’t hesitate to reach out in the interim via Slack or e-mail!
