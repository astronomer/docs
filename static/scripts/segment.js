!function () {
  var analytics = window.analytics = window.analytics || []; if (!analytics.initialize) if (analytics.invoked) window.console && console.error && console.error("Segment snippet included twice."); else {
    analytics.invoked = !0; analytics.methods = ["trackSubmit", "trackClick", "trackLink", "trackForm", "pageview", "identify", "reset", "group", "track", "ready", "alias", "debug", "page", "once", "off", "on", "addSourceMiddleware", "addIntegrationMiddleware", "setAnonymousId", "addDestinationMiddleware"]; analytics.factory = function (e) { return function () { var t = Array.prototype.slice.call(arguments); t.unshift(e); analytics.push(t); return analytics } }; for (var e = 0; e < analytics.methods.length; e++) { var key = analytics.methods[e]; analytics[key] = analytics.factory(key) } analytics.load = function (key, e) { var t = document.createElement("script"); t.type = "text/javascript"; t.async = !0; t.src = "https://cdn.segment.com/analytics.js/v1/" + key + "/analytics.min.js"; var n = document.getElementsByTagName("script")[0]; n.parentNode.insertBefore(t, n); analytics._loadOptions = e }; analytics._writeKey = "D2wC7j10rVFq4PPQOGqGPHpyujDhtbjM";; analytics.SNIPPET_VERSION = "4.15.3"; analytics.page();
  }
  var elemDiv = document.createElement('div');
  elemDiv.style.cssText = 'position:fixed;width:100%;left:0;right:0;bottom:0;z-index:100;';
  elemDiv.id = 'consentManager';
  document.body.appendChild(elemDiv);

  window.addEventListener("load", function () {
    let cookiePrefLink = document.getElementById('cookiePref');
    cookiePrefLink.addEventListener("click", function (e) {
      e.stopPropagation();
      window.consentManager.openConsentManager();
    })
  })
}();