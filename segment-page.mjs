import ExecutionEnvironment from "@docusaurus/ExecutionEnvironment";

export default (function () {
  if (!ExecutionEnvironment.canUseDOM) {
    return null;
  }

  return {
    onRouteDidUpdate({ location, previousLocation }) {
      if (previousLocation && location.pathname !== previousLocation.pathname) {
        if (!window.analytics) return;
        setTimeout(() => {
          window.analytics.page();
        }, 0);
      }
    },
  };
})();