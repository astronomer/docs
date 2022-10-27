import React from "react";
import { MDXProvider } from "@mdx-js/react";
import MDXComponents from "@theme/MDXComponents";
import Admonition from "@theme/Admonition";
export default function MDXContent({ children }) {
  const isCloudIdePage =
    window.location.pathname.startsWith("/astro/cloud-ide");

  // if we're on the public preview cloud ide page, no need to also show the banner
  if (window.location.pathname === "/astro/cloud-ide/public-preview") {
    return <MDXProvider components={MDXComponents}>{children}</MDXProvider>;
  }

  // otherwise, conditionally show the banner if we're on a cloud ide page
  return (
    <MDXProvider components={MDXComponents}>
      {isCloudIdePage && (
        <Admonition type="caution">
          The Cloud IDE is currently in public preview and features are subject
          to change. Click <a href="/astro/cloud-ide/public-preview">here</a>{" "}
          for more info.
        </Admonition>
      )}

      {children}
    </MDXProvider>
  );
}
