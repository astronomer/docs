---
title: 'Export Astro audit logs'
id: audit-logs
sidebar_label: Export audit logs
---

:::caution

This feature is in [Public Preview](https://docs.astronomer.io/astro/feature-previews).

:::

Astro audit logs record Astro control plane administrative activities and events. You can use the audit logs to determine who did what, where, and when. You can also use audit logs to ensure your Organization is meeting its security and regulatory requirements. For example, you can use audit logs to determine when users were added to your Organization or to individual Workspaces.

See [Reference: Astro audit log fields](audit-logs-reference.md) for a complete list of available fields in audit logs.

## Export audit logs

Audit logs are retained for 90 days. Organization Owner permissions are required to export audit logs. 

1. In the Cloud UI, click Astronomer logo in the upper left corner to open your Organization page. Then, click **Settings** > **General**.

2. In **Audit Logs**, select the number days of audit data to export and then click **Export**.

    The extracted audit log data is saved as a JSON file in your `downloads` directory with the default filename `<astro-organization-name>-logs-<number-of-days>-days-<date>.json`.

:::cli

You can also export logs using the Astro CLI.

1. Run the following command to enable the feature:

    ```sh
    astro config set -g beta.audit_logs true
    ```

2. Run the following command to export audit logs as a GZIP file to your current directory:

    ```sh
    astro organization audit-logs export --organization-name="<your-organization-name>"
    ```

:::
