---
sidebar_label: 'GDPR compliance'
title: "GDPR compliance"
id: gdpr-compliance
description: Learn how Astronomer and Astro are GDPR compliant.
---

## What is the GDPR?

The [General Data Protection Regulation](https://gdpr-info.eu/) (GDPR) is a legal framework that sets guidelines for the collection and processing of personal information from individuals who live in the [European Economic Area](https://www.gov.uk/eu-eea) (EEA). The European privacy law became enforceable on May 25, 2018, and replaces the EU’s [Data Protection Directive](http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:31995L0046:en:HTML), which went into effect in 1995. The GDPR is intended to harmonize national data privacy laws throughout the EEA and enhance the protection of all EEA residents with respect to their personal data.

The European Commission provides official definitions about the legislation [here](https://ec.europa.eu/info/law/law-topic/data-protection/data-protection-eu_en).

## Who is impacted by GDPR?

The GDPR applies to companies that are established within and outside of the EU that offer goods or services to EEA residents, or monitor their behavior. In essence, it impacts and applies to all companies processing and holding the personal data of data subjects located in the EEA. The GDPR defines "[personal data](https://gdpr-info.eu/issues/personal-data/)" to be "any information which are related to an identified or identifiable natural person".

## Is Astronomer subject to GDPR?

Astronomer is subject to GDPR because the personal data of EEA residents is processed and stored through consumption of Astronomer services.

## Is my company subject to GDPR?

If there is a possibility that your company collects or processes personal data of individuals located in the EEA, you are most likely subject to GDPR. Confirm with your privacy and legal counsel.

## How does using Astro help me comply with the GDPR?

Simply using Astro does not ensure compliance with GDPR, but the combination of a Data Processing Agreement (DPA), Astro architecture, and various controls, features, and modules available in Astro, Astro Runtime, and Astronomer Registry can help you with your GDPR compliance.

Astro is designed and architected with security and privacy by default. Astro boasts a hybrid deployment model founded on a control plane hosted by Astronomer and a data plane that is hosted in your cloud environment. Both are fully managed by Astronomer. This model offers the self-service convenience of a fully managed service while respecting the need to keep data private, secure, and within corporate boundaries.

All customer business data never leaves your environment (for example, a cloud database) or is required to be uploaded to Astronomer's own cloud service, thus reducing any concerns that Astronomer may not properly respond to a GDPR request in the allotted time as prescribed by GDPR requirements.

The customer (the [data controller](https://gdpr-info.eu/art-4-gdpr/)) maintains full control over how their data is accessed by their data plane through a combination of network, authentication and authorization controls. Running a current and supported version of [Astro Runtime](upgrade-runtime.md) ensures the latest security and bug fixes are in effect, while the [Astronomer Registry](https://registry.astronomer.io/) provides a suite of [provider-maintained modules](https://registry.astronomer.io/modules/?page=1) that you can use to interact with your data in a secure and standard way.

Some basic personal information about Astro users, such as email addresses, names, and IP addresses, as well as data pipeline metadata, such as deployments metrics, scheduler logs, and lineage, is collected and processed by Astronomer (the [data processor](https://gdpr-info.eu/art-4-gdpr/)) in the control plane to provide Astro services like user management, deployment management, and observability. Customers may [exercise their data protection rights](https://www.astronomer.io/privacy#exercising-of-your-gdpr-data-protection-rights) if they have concerns about the management of this personal data.

## Does Astronomer offer a Data Processing Agreement (DPA)?

Yes, Astronomer offers a Data Processing Agreement which complies with the requirements of the current GDPR legal framework in relation to data processing. If your company requires a DPA with Astronomer to satisfy the requirements the GDPR imposes on data controllers with respect to data processors, contact [privacy@astronomer.io](mailto:privacy@astronomer.io).

Please note that if you have previously executed a DPA with Astronomer, it is likely that the DPA already contains sufficient provisions to satisfy the requirements the GDPR imposes on data controllers with respect to data processors. If you believe a new DPA is required, contact [privacy@astronomer.io](mailto:privacy@astronomer.io) with any questions or concerns.

## How does Astronomer perform transfer of personal data outside of the EEA?

The [European Commission](https://ec.europa.eu/info/index_en) (EC) issued modernized [Standard Contractual Clauses](https://ec.europa.eu/info/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en) (SCCs) on June 4, 2021, under the GDPR (Article 46) for data transfers from controllers or processors in the EU/EEA (or otherwise subject to the GDPR) to controllers or processors established outside the EU/EEA (and not subject to the GDPR).

Astronomer is subject to the new SCCs to transfer personal data to countries outside of the EEA where necessary, and has incorporated them into a standard Data Processing Agreement for the purposes of providing our Services (inclusive of support).

:::info

This page is for informational purposes only. Customers should not consider the information or recommendations presented here to constitute legal advice. Customers should engage their own legal and privacy counsel to properly evaluate their use of Astronomer services, with respect to their legal and compliance requirements and objectives.

:::
