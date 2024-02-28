import ExecutionEnvironment from "@docusaurus/ExecutionEnvironment";

export default (function () {
  if (!ExecutionEnvironment.canUseDOM) {
    return null;
  }

  return {
    onRouteDidUpdate() {
      if (!window.analytics) return;
      window.analytics.page();
    },
  };
})();