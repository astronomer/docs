export const siteVariables = {
  // version-specific
  cliVersion: '1.10.0',
  runtimeVersion: '7.2.0',
  jenkinsenv: '${env.GIT_BRANCH}',
  jenkinsenv1: '${files[*]}',
  jenkinsenv2: '${#files[@]}',
  deploymentid: '${ASTRONOMER_DEPLOYMENT_ID}',
};
