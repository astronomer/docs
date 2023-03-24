const { track, identify } = require("./utils/analytics");
const { submitFormDataToHubspot } = require("./utils/hubspotAPI");

exports.handler = (event, context, callback) => {
  if (event.httpMethod === "POST" && event.body) {
    try {
      const body = JSON.parse(event.body);
      const {
        anonId,
        email,
        referrer,
        hubSpotCookie,
        intercomCookie,
        intercomSessionCookie,
        source,
        medium,
        campaign,
        content,
        term,
        ip,
        spottedCompany,
        pageName,
        pageURI,
        gclid,
        gaSessionId,
        gaClientId,
        hubspotFormID
      } = body;

      identify(anonId, { email, companyDomain: spottedCompany && spottedCompany.domain || "", leadMagicId: spottedCompany && spottedCompany.id || "", spottedCompany: spottedCompany || "", gaSessionId, gaClientId });

      track(anonId,
        "Docs - Developer Updates Form Submission processed by server",
        {
          email,
          referrer,
          hubSpotCookie,
          intercomCookie,
          intercomSessionCookie,
          source,
          medium,
          campaign,
          content,
          term,
          ip,
          companyDomain: spottedCompany.domain || "",
          leadMagicId: spottedCompany.id || "",
          spottedCompany,
          pageName,
          pageURI,
          gclid,
          gaSessionId,
          gaClientId,
          hubspotFormID
        });

      // submit form to hubspotAPI
      submitFormDataToHubspot(event, "Developer Updates");

      callback(null,
        {
          statusCode: 200,
          body: JSON.stringify({
            success: true,
            data: { ...body }
          })
        });
    } catch (err) {
      Sentry.captureException(err);
      callback(null,
        {
          statusCode: 200,
          body: JSON.stringify({
            success: false,
            error: err
          })
        });
    }
  }
};
