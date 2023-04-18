export const siteVariables = {
  // version-specific
  cliVersion: '1.13.2',
  runtimeVersion: '8.0.0',
  jenkinsenv: '${env.GIT_BRANCH}',
  jenkinsenv1: '${files[*]}',
  jenkinsenv2: '${#files[@]}',
  deploymentid: '${ASTRONOMER_DEPLOYMENT_ID}',
};
