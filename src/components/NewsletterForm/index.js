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
    buttonText,
    successMessage,
    errorMessage
  }
) {
  const [email, setEmail] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(false);
  const [disableButton, setDisableButton] = useState(false);

  const content = useNewsletterFormConfig();

  const hubspotFormID = "e9ef5932-da7d-4129-8111-472977ea943a";

  function getSegmentUser() {
    if (window && window.analytics && window.analytics.user) {
      const { analytics } = window;
      return analytics.user().anonymousId();
    }
    return null;
  };

  function getCookie(cname) {
    if (window) {
      const name = `${cname}=`;
      const decodedCookie = decodeURIComponent(window.document.cookie);
      const ca = decodedCookie.split(';');
      for (let i = 0; i < ca.length; i++) { //eslint-disable-line
        let c = ca[i];
        while (c.charAt(0) === ' ') {
          c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
          return c.substring(name.length, c.length);
        }
      }
    }
    return '';
  };

  function getUTMField(name) {
    if (window) {
      const sanitizedName = name.replace(/[\[]/, '\[').replace(/[\]]/, '\]');
      const regex = new RegExp("[\?&]" + sanitizedName + "=([^&#]*)");
      const results = regex.exec(window.location.search);

      // if results === null first check if stored locally
      // Otherwise if we really have nothing then return nothing
      if (results === null) {
        return localStorage.getItem(name) ? localStorage.getItem(name) : '';
      } else {
        // But always use what's in the URL if present
        const decodeVal = decodeURIComponent(results[1].replace(/\+/g, ' '));
        // And if we have a value, save it to localStorage for future use
        decodeVal && localStorage.setItem(name, decodeVal);
        return decodeVal;
      }
    }
  };

  async function handleSubmit(e) {
    e.preventDefault();

    setSubmitting(true);
    setDisableButton(true);

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
      formName: "Developer Updates",
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
      spottedCompany,
      hubspotFormID
    };

    window.analytics.track(`Submitted Developer Updates Sign Up Form`, body);

    if (window && window.plausible) {
      window.plausible("Form Submission", {
        props: {
          formName: "Developer Updates",
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
      .then((res) => {
        setSubmitting(false);
        setSuccess(true);
      })
      .catch((err) => {
        setSubmitting(false);
        setError(true);
        console.log(err);
      });
  }

  return (
    <form
      autoComplete="on"
      onSubmit={handleSubmit}
      className={styles.newsletterForm}
      id="newsletterForm"
    >
      <h2>{title || content.title}</h2>
      <p className={styles.newsletterForm__description}>Get a summary of our release notes from us once a month.</p>
      {!submitting && !success && !error && (
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
      )
      }
      {submitting &&
        <img src="/img/spinner.gif" alt="Sending your email address to our servers..." className={styles.newsletterForm__spinner} width="20" height="20" />
      }
      {success &&
        <p className={styles.newsletterForm__success}>{successMessage || content.successMessage}</p>
      }
      {error &&
        <p className={styles.newsletterForm__error}>{errorMessage || content.errorMessage}</p>
      }
      <p className={styles.newsletterForm__disclaimer}>You can unsubscribe at any time. <br />By proceeding you agree to our <a href="https://www.astronomer.io/privacy/" target="_blank">Privacy Policy</a>, our <a href="https://www.astronomer.io/legal/terms-of-service/" target="_blank">Website Terms</a> and to receive emails from Astronomer.</p>
    </form>
  )
}
