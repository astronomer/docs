---
sidebar_label: "Security & Data Governance"
title: Security & Data Governance
id: security
---

## Security

The Cloud IDE is a fully managed service that runs in an Astronomer-managed private cluster. This means that all of the infrastructure is managed by Astronomer, and you don't have to worry about managing the underlying infrastructure. Infrastructure is tightly scoped to organizations, so your code and data will never be exposed to other organizations.

## Data Governance

Because the Cloud IDE allows for cell execution at any time, results from each cell must be stored somewhere. By default, the Cloud IDE stores Python cell outputs in an encrypted S3 bucket. SQL cell outputs are stored in the corresponding connection database under the schema you configure.

If you would like to provide your own S3 bucket for storing Python cell outputs, please reach out to the Astronomer team.

Data is never persisted in the Astronomer control plane. When a user executes a cell, the request is sent through the Astronomer control plane to a Kubernetes pod running the Cloud IDE. The request is then sent to the appropriate database or S3 bucket. The response is then sent back through the control plane to the user.
