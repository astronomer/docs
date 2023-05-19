---
sidebar_label: 'Allowlist Astro IP addresses'
title: 'Allowlist Astro IP addresses'
id: 'astro-ips'
---

Each Astro cluster has a group of IP addresses that Deployments on your cluster use to connect with external systems. To connect Astro with external services, you might need to allowlist Astro IPs in those services. 

A cluster's IP addresses are the same for as for all Deployments in the cluster.

## Retrieve external IP addresses for a Deployment

Retrieve external IP addresses for an individual Deployment if you are using standard clusters or otherwise don't have access to your Organization's **Clusters** page.

1. In the Cloud UI, select a Deployment, then click **Details**.
2. Copy the IP addresses under **External IPs**
3. Optional. Add the IP addresses to the allowlist of any external services that need to interact with Astro. 

## Retrieve external IP addresses for a cluster

Retrieve external IP addresses for an individual Deployment if you are using standard clusters or otherwise don't have access to your Organization's **Clusters** page.

1. In the Cloud UI, click the Astronomer logo in the upper left corner to open your Organization.
2. Click **Clusters**, then select a cluster.
3. In the **Details** page, copy the IP addresses listed under **External IPs**.
