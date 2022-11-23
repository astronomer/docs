---
title: 'Astronomer Software v0.31 release notes'
sidebar_label: 'Astronomer Software'
id: release-notes
description: Astronomer Software release notes.
---

<!--- Version-specific -->

0.31 is the latest stable version of Astronomer Software, while 0.30 remains the latest long-term support (LTS) release. To upgrade to 0.31, see [Upgrade Astronomer](upgrade-astronomer.md). For more information about Software release channels, see [Release and lifecycle policies](release-lifecycle-policy.md). To read release notes specifically for the Astro CLI, see [Astro CLI release notes](cli-release-notes.md).

## 0.31.0

### New root user persona

### Support for SCIM integration 

### Invite users only through teams

### View and export task usage metrics

### Additional improvements 

- You can now set a custom security context for `es-client` setting `elasticsearch.client.securityContext.capabilities.add={}` in the ElasticSearch Helm chart.
- Deployment users are now paginated in the Software UI.
- You can now set `astronomer.registry.logLevel` to filter which types of logs appear in your Docker registry.
- Changed the default Git sync interval from 0 to 1.
- You can now configure a Deployment to have 0 triggerer components.
- You can now set `astronomer.houston.config.useAutoCompleteForSensativeFields=false` to disable autocomplete on sensitive fields in the Software UI.
- You can now set `astronomer.houston.config.shouldLogUsername=true` to include user email addresses in audit logs for logins through the Houston API.

  
### Bug fixes

- Fixed an issue where the Software UI would occasionally show an incorrect **Extra AU** number for Deployments. 
- Fixed the following vulnerabilities:

    - [CVE-2022-37601](https://security.snyk.io/vuln/SNYK-JS-LOADERUTILS-3043105)
    - [CVE-2022-43680](https://nvd.nist.gov/vuln/detail/CVE-2022-43680)
    - [CVE-2022-40674](https://nvd.nist.gov/vuln/detail/CVE-2022-40674)
  
- Fixed an issue where you could not access Astronomer Software's Docker registry if you had access to more than 100 Deployments. 
- Fixed an issue where the configuration in `astronomer.houston.updateRuntimeCheck.url` was ignored if not all supported Deployment image versions are present in the destination URL. 