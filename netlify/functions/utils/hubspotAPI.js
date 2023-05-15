const fetch = require("node-fetch");

// "https://api.hsforms.com/submissions/v3/integration/submit/:portalId/:formGuid"

function submitFormDataToHubspot(event, formName) {
  const formData = JSON.parse(event.body);
  let processedData = null;
  const basePayload = {
    fields: [
      {
        name: "firstname",
        value: formData.firstName ? formData.firstName : "",
      },
      {
        name: "lastname",
        value: formData.lastName ? formData.lastName : "",
      },
      {
        name: "email",
        value: formData.email ? formData.email : "",
      },
      {
        name: "company",
        value: formData.company ? formData.company : "",
      },
      {
        name: "anonymousid",
        value: formData.anonId ? formData.anonId : "",
      },
      {
        name: "recent_form_submission_date",
        value: formData.submissionDate ? formData.submissionDate : "",
      },
      {
        name: "recent_form_submission_datetime",
        value: formData.dateTime ? formData.dateTime : "",
      },
      {
        name: "recent_form_submission",
        value: `${formName} Form processed by API`,
      },
      {
        name: "utm_campaign",
        value: formData.campaign ? formData.campaign : "",
      },
      {
        name: "utm_medium",
        value: formData.medium ? formData.medium : "",
      },
      {
        name: "utm_source",
        value: formData.source ? formData.source : "",
      },
      {
        name: "utm_term",
        value: formData.term ? formData.term : "",
      },
      {
        name: "gclid",
        value: formData.gclid ? formData.gclid : "",
      },
      {
        name: "stage",
        value: "0) Inquiry",
      },
      {
        name: "tracking_blocked",
        value: formData.trackingBlocked ? formData.trackingBlocked : ""
      }
    ],
    context: {
      pageUri: formData.pageURI ? formData.pageURI : "",
      pageName: formData.pageName ? formData.pageName : "",
      ipAddress: formData.ip || "123.123.123.123",
    },
  };

  if (formData.hubSpotCookie !== "") {
    basePayload.context.hutk = formData.hubSpotCookie;
  }

  processedData = basePayload;

  const finalData = JSON.stringify(processedData);
  const url = `https://api.hsforms.com/submissions/v3/integration/submit/9491775/${formData.hubspotFormID}`;

  console.log(finalData);

  const response = fetch(url, {
    headers: {
      'Authorization': process.env.HUBSPOT_API_KEY,
      "Content-Type": "application/json",
    },
    method: "POST",
    body: finalData,
  }).then(res => res.json())
    .then(json => console.log(json))
    .catch(err => {
      console.log(err)
      console.log(finalData);
      Sentry.captureException(err);
    });

  console.log(response);

  return response;
}

module.exports = {
  submitFormDataToHubspot
};
