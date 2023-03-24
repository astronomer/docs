const Analytics = require("analytics-node");

const apiKey = process.env.SEGMENT_WRITE_KEY;
const analytics = new Analytics(apiKey, { flushAt: 1 });

function track(anonymousId, event, properties) {
  if (analytics) {
    analytics.track({ anonymousId, event, properties });
  }
}

function identify(userId, traits) {
  if (analytics) {
    analytics.identify({ userId, traits });
  }
}

module.exports = {
  identify,
  track,
};
