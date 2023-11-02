export const siteVariables = {
  // version-specific
  runtimeVersion: '9.4.0',
  cliVersion: '1.19.4',
  jenkinsenv: '${env.GIT_BRANCH}',
  jenkinsenv1: '${files[*]}',
  jenkinsenv2: '${#files[@]}',
  jenkinsenv3: '$(date +%Y%m%d%H%M%S)',
  jenkinsenv4: '$astro_id',
  deploymentid: '${ASTRONOMER_DEPLOYMENT_ID}',
};
