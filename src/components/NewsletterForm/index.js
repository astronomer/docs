import React, { useState, useEffect } from "react";
import styles from './styles.module.css';
import { useThemeConfig } from '@docusaurus/theme-common';

function useNewsletterFormConfig() {
  // TODO temporary casting until ThemeConfig type is improved
  return useThemeConfig().newsletterForm;
}

export default function NewsletterForm(
  {
    title,
    buttonText
  }
) {
  const [email, setEmail] = useState("");
  const [disableButton, setDisableButton] = useState(false);

  const content = useNewsletterFormConfig();

  async function handleSubmit(e) {
    e.preventDefault();

    setDisableButton(true);

    async function checkEmail(emailToValidate) {
      return fetch(
        `https://api.mailgun.net/v4/address/validate?address=${emailToValidate}`,
        {
          // eslint-disable-line
          method: "GET",
          headers: {
            Authorization: `Basic ${btoa(
              "api:key-396a07e6abdaf2e224a06518d7e89c26"
            )}`,
          },
        }
      )
        .then((res) => res.json())
        .then((json) => json.result !== "undeliverable");
    }

    const referrer = (window && window.previousPath) || "";
    const spottedCompany = (window && window.spottedCompany) || "";
    const hubSpotCookie = getCookie("hubspotutk");
    const source = getUTMField("utm_source");
    const medium = getUTMField("utm_medium");
    const campaign = getUTMField("utm_campaign");
    const content = getUTMField("utm_content");
    const term = getUTMField("utm_term");
    const gclid = JSON.parse(localStorage.getItem("gclid"));

    const gaSessionId =
      (getCookie("_ga_DKTB1B78FV") &&
        getCookie("_ga_DKTB1B78FV").match("(?:GS[0-9].[0-9].):*([0-9]+)")[1]) ||
      "";
    const gaClientId =
      (getCookie("_ga") &&
        getCookie("_ga").match("(?:GA[0-9].[0-9].):*(.+)")[1]) ||
      "";

    const pageName = window && window.document.title;
    const pageURI = window && window.location.href;
    const dateTime = new Date();
    const submissionDate = new Date().toLocaleString("en-US", {
      timeZone: "America/New_York",
    });
    const submissionHour = new Date()
      .getHours()
      .toLocaleString("en-US", { timeZone: "America/New_York" });
    const userPath = window.locations && window.locations.join(",");

    const body = {
      email,
      referrer,
      hubSpotCookie,
      source,
      medium,
      campaign,
      content,
      term,
      gclid: gclid ? gclid.value : "",
      gaSessionId,
      gaClientId,
      pageName,
      pageURI,
      dateTime,
      submissionDate,
      submissionHour,
      userPath,
      ip,
      spottedCompany
    };

    const isEmailDeliverable = await checkEmail(email);

    if (isEmailDeliverable) {
      track(`Submitted Developer Updates Sign Up Form`, body);

      if (isWindow && window.plausible) {
        window.plausible("Form Submission", {
          props: {
            formName,
            referrer,
            pageName,
            pageURI,
            hubspotFormID,
            source,
            medium,
            campaign,
            content,
            term,
          },
        });
      }

      body.anonId = getSegmentUser() || email;

      fetch(`/.netlify/functions/submit-form`, {
        // eslint-disable-line
        method: "POST",
        body: JSON.stringify(body),
      })
        .then((res) => res.json())
        .catch((err) => {
          console.log(err);
        });

      setTimeout(() => {
        window.location = successURL;
      }, 1500);
    } else {
      setEmail("");
      setDisableButton(false);
      isWindow && window.alert("Please provide a valid email address.");
    }
  }

  return (
    <form
      autoComplete="on"
      onSubmit={handleSubmit}
      className={styles.newsletterForm}
      id="newsletterForm"
    >
      <h2>{title || content.title}</h2>
      <div className={styles.newsletterForm__inputWrapper}>
        <input
          aria-label="Email Address"
          type="email"
          name="email"
          placeholder="you@company.com"
          value={email}
          autoComplete="email"
          onChange={(e) => setEmail(e.target.value.trim().toLowerCase())}
          pattern="^.+@.+\..+$"
          required
          title="you@company.com"
        />
        <button type="submit" disabled={disableButton}>{buttonText || content.buttonText}</button>
      </div>
      <p>You can unsubscribe at any time. <br />By proceeding you agree to our <a href="https://www.astronomer.io/privacy/" target="_blank">Privacy Policy</a>, our <a href="https://www.astronomer.io/legal/terms-of-service/" target="_blank">Website Terms</a> and to receive emails from Astronomer.</p>
    </form>
  )
}
