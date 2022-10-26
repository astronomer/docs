// this wraps the cloud ide docs with a "public preview" banner
// we can remove this when we go GA

import React from "react";
import { HtmlClassNameProvider } from "@docusaurus/theme-common";
import { DocProvider } from "@docusaurus/theme-common/internal";
import DocItemMetadata from "@theme/DocItem/Metadata";
import DocItemLayout from "@theme/DocItem/Layout";
import Admonition from "@theme/Admonition";

export default function DocItem(props) {
  const docHtmlClassName = `docs-doc-id-${props.content.metadata.unversionedId}`;
  const MDXComponent = props.content;
  return (
    <DocProvider content={props.content}>
      <HtmlClassNameProvider className={docHtmlClassName}>
        <Admonition type="caution">
          The Cloud IDE is currently in public preview and features are subject
          to change. If you have feedback or discover bugs, please reach out to
          the Astronomer team.
        </Admonition>

        <br />

        <DocItemMetadata />
        <DocItemLayout>
          <MDXComponent />
        </DocItemLayout>
      </HtmlClassNameProvider>
    </DocProvider>
  );
}
