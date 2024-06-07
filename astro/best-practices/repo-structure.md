---
title: 'Setting up your code repository and CI/CD'
sidebar_label: 'Repository Structure and CI/CD'
id: repo-structure
---

On Astro, you have options when it comes to organizing your code repository and setting up CI/CD. It's important to keep in mind the benefits and limitations of each option, along with the needs of your team and structure of your organization, when adopting a deployment and CI/CD strategy.

## Feature overview

Astro supports a variety of deployment and CI/CD strategies. For example, you can keep your DAG code and your project configuration in separate repositories, and you can deploy from multiple repositories to a single Astro Deployment. But each approach Astro supports has benefits as well as limitations depending on your team's needs and other factors. The guidance offered here is intended to help you choose the best deployment and CI/CD strategy for your team. 

## Best practice guidance

Regardless of your particular use case, Astronomer strongly recommends employing a version control tool such as [GitHub](https://github.com/) or [GitLab](https://about.gitlab.com/). Utilizing version control tools is a longstanding software development best practice that offers teams enhanced collaboration and improved workflows for testing new features and fixes, among many other benefits.

Astronomer also recommends utilizing Continuous Integration and Continuous Delivery (CI/CD) pipelines. CI/CD pipelines are programmatic pipelines for automating key parts of the development lifecycle, including code changes, builds, and testing. CI/CD helps your organization develop faster, more securely, and more reliably.

With a version control system in place, you can easily set up automated deployment of your latest changes to Astro. On Astro, you have a number of options when it comes to setting this up. How you choose to organize the code in your shared repository and deploy it to Astro should reflect the size and needs of your team. 

### Option 1: one repo to one Deployment

### Option 2: one repo with multiple projects to multiple Deployments with CI/CD

### Option 3: multiple repos to one Deployment

