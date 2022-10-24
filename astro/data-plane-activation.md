---
sidebar_label: 'Data plane activation'
title: 'Data plane activation'
id: 'data-plane-activation'
description: Prepare for the activation of your Astro data plane.
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Astro is a modern data orchestration platform, powered by Apache Airflow, that enables your entire data team to build, run, and observe data pipelines. The Astro architecture includes a single-tenant data plane in your cloud and a multi-tenant control plane in the Astronomer cloud. The data plane provides a reliable and seamless connection to all of your data services.

Your data plane is deployed into a clean, dedicated AWS account, GCP project, or Microsoft Azure subscription. Astronomer is responsibile for the operations of this account. See [Shared responsibility model](shared-responsibility-model.md).

By default, the Astronomer account can't access your data services. Astronomer support will work with you to ensure your peering VPC or direct connections are secure.

![High level overview of Astro's architecture](/img/docs/architecture-overview.png)

### What to expect

An assigned Astronomer engineer will work with you to activate your data plane. The activation process typically takes and hour and when it's complete you'll have your first pipeline deployed in your Astro environment. In addition, you'll have hands-on experience with Astronomer data orchestration.

### Prerequisites

<Tabs
    defaultValue="aws"
    groupId= "prerequisites"
    values={[
        {label: 'AWS', value: 'aws'},
        {label: 'Azure', value: 'azure'},
        {label: 'GCP', value: 'gcp'},
    ]}>
<TabItem value="aws">

The following are required when activating your AWS data plane:
- [ ] [Astro CLI](cli/overview.md) installed for any users who will develop pipelines
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

<TabItem value="azure">

The following are required when activating your Azure data plane:
- [ ] [Astro CLI](cli/overview.md) installed for any users who are developing pipelines.
- [ ] A clean Azure subscription. For security reasons, Azure subscriptions with existing tooling running aren't supported. Also, the subscription must be included in an Azure management group that doesn't apply Azure policies. See [What are Azure management groups?](https://docs.microsoft.com/en-us/azure/governance/management-groups/overview).
- [ ] An Azure Active Directory (AD) user with the following role assignments:
    - `Application Administrator`. See [Understand roles in Azure Active Directory](https://docs.microsoft.com/en-us/azure/active-directory/roles/concept-understand-roles).
    - `Owner`with permission to create and manage subscription resources of all types. See [Azure built-in roles](https://docs.microsoft.com/en-us/azure/active-directory/roles/concept-understand-roles).
- [ ] The Microsoft Azure CLI or Azure Az PowerShell module.  See [How to install the Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) and [Install the Azure Az PowerShell module](https://docs.microsoft.com/en-us/powershell/azure/install-az-ps).
- [ ] Desired region for Astro cluster deployment identified, from the list of [supported regions](resource-reference-azure.md#supported-regions).

</TabItem>

<TabItem value="gcp">

The following are required when activating your GCP data plane:
- [ ] [Astro CLI](cli/overview.md) installed for any users who will develop pipelines
- [ ] A clean GCP project
- [ ] A user with [Owner access](https://cloud.google.com/iam/docs/understanding-roles#basic-definitions) to your project
- [ ] A desired region for your Astro cluster, from the list of [supported regions](resource-reference-gcp.md#gcp-region)
- [ ] _If peering VPCs_, preferred subnet CIDR range identified (no smaller than a /19 range)

</TabItem>
</Tabs>

### What’s next

After your data plane is activated, you can spin up new Airflow environments, deploy pipelines through the Astro CLI, and experience an improved Airflow powered by Astro Runtime.

Our engineers want to help you get started quickly and get back to focusing on your pipelines. We’ll reach out in a few days to see how you’re doing, but don’t hesitate to reach out in the interim using Slack or e-mail.
