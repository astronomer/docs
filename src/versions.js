export const siteVariables = {
  cliVersion: '1.3.3',
  runtimeVersion: '4.2.4',
  // Hacky variable so that we can use env var fromatting in CI/CD templates
  deploymentid: '${ASTRONOMER_DEPLOYMENT_ID}',
  keyid: '${ASTRONOMER_KEY_ID}',
  keysecret: '${ASTRONOMER_KEY_SECRET}',
};
