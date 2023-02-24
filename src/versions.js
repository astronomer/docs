export const siteVariables = {
  // version-specific
  cliVersion: '1.11.0',
  runtimeVersion: '7.3.0',
  jenkinsenv: '${env.GIT_BRANCH}',
  jenkinsenv1: '${files[*]}',
  jenkinsenv2: '${#files[@]}',
  deploymentid: '${ASTRONOMER_DEPLOYMENT_ID}',
};
