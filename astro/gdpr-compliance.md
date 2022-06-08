---
sidebar_label: 'GDPR Compliance'
title: "GDPR Compliance"
id: gdpr-compliance
description: Learn how Astronomer and Astro are GDPR compliant.
---

## What is the GDPR?

The [General Data Protection Regulation](https://gdpr-info.eu/) (GDPR) is a legal framework that sets guidelines for the collection and processing of personal information from individuals who live in the [European Economic Area](https://www.gov.uk/eu-eea) (EEA). The European privacy law became enforceable on May 25, 2018, and replaces the EU’s [Data Protection Directive](http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:31995L0046:en:HTML), which went into effect in 1995. The GDPR is intended to harmonize national data privacy laws throughout the EEA and enhance the protection of all EEA residents with respect to their personal data.

## Who is impacted by GDPR?

The GDPR applies to companies that are established within and outside of the EU that offer goods or services to EEA residents, or monitor their behavior. In essence, it impacts and applies to all companies processing and holding the personal data of data subjects located in the EEA.
The GDPR defines personal data to include any information relating to an identified or identifiable natural person.

## Is Astronomer subject to GDPR?

Yes Astronomer is subject to GDPR, given we process and store personal data of EEA residents, through consumption of our services.

## Is my company subject to GDPR?

Most likely if there is a possibility that your company collects or processes personal data of individuals located in the EEA. Confirm with your privacy and legal counsel.

## How does using Astro help me comply with the GDPR?

Simply using Astro does not ensure compliance with GDPR, but the combination of a Data Processing Agreement (DPA), Astro architecture, and various controls, features, and modules available in Astro, Astro Runtime, and Astronomer Registry may help you with your GDPR compliance.

Astro is designed and architected with security and privacy by default. Astro boasts a hybrid deployment model founded on a Control Plane hosted by Astronomer and a Data Plane that is hosted in your cloud environment. Both are fully managed by Astronomer. This model offers the self-service convenience of a fully managed service while respecting the need to keep data private, secure, and within corporate boundaries.

All customer business data never leaves your environment (eg. cloud database) or is required to be uploaded to Astronomer. The customer (the Data Controller) maintains full control over how their data is accessed by their Data Plane through a combination of network, authentication and authorization controls. Running a current and supported version of [Astronomer Runtime](upgrade-runtime.md) ensures the latest security and bug fixes are in effect, while the [Astronomer Registry](https://registry.astronomer.io/) provides a suite of [modules](https://registry.astronomer.io/modules/?page=1) to leverage in your data pipelines running in your Data Plane, to consume or interact with your data. At no point is customer business data required to be copied or uploaded to Astronomer, thus reducing any concerns that Astronomer may not properly respond to a GDPR request in the allotted time as prescribed by GDPR requirements.

Some basic personal information (email, name, ip address) about Astro users and data pipeline metadata (eg. deployments metrics, scheduler logs, lineage) is required to be collected and processed by Astronomer (the Data Processor) in the Control Plane, for the purposes of providing Astro services (eg. user management, deployment management, observability, etc.). Customers may [exercise their data protection rights](https://www.astronomer.io/privacy#exercising-of-your-gdpr-data-protection-rights) if they have concerns about the management of this personal data.
 
## Does Astronomer offer a Data Processing Agreement (DPA)?

Yes, Astronomer offers a Data Processing Agreement, which complies with the requirements of the current GDPR legal framework in relation to data processing. If your company requires a DPA with Astronomer to satisfy the requirements the GDPR imposes on data controllers with respect to data processors, and you do not have once in place with us, reach out to us at [privacy@astronomer.io](mailto:privacy@astronomer.io)

Please note that if you have previously executed a DPA with Astronomer, it is likely that the DPA already contains sufficient provisions to satisfy the requirements the GDPR imposes on data controllers with respect to data processors. If you believe a new DPA is required, reach out to us at [privacy@astronomer.io](mailto:privacy@astronomer.io) with any questions or concerns.

## How does Astronomer perform transfer of personal data outside of the EEA?

The [European Commission](https://ec.europa.eu/info/index_en) (EC) issued modernized [Standard Contractual Clauses](https://ec.europa.eu/info/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en) (SCCs) on June 4, 2021, under the GDPR (Article 46) for data transfers from controllers or processors in the EU/EEA (or otherwise subject to the GDPR) to controllers or processors established outside the EU/EEA (and not subject to the GDPR).

Astronomer is subject to the new SCCs to transfer personal data to countries outside of the EEA where necessary, and has incorporated them into our standard Data Processing Agreement for the purposes of providing our Services (inclusive of support). 

:::info

This page is for informational purposes only. Customers should not consider the information or recommendations presented here to constitute legal advice. Customers should engage their own legal and privacy counsel to properly evaluate their use of Astronomer services, with respect to their legal and compliance requirements and objectives.

::
