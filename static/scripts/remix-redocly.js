(function () {
  /** Find all of the "Responses" headers above the responses schema section */
  let h3s = [...document.querySelectorAll('h3')].filter((h3) => { return h3.innerText === "Responses" });
  /** Then rewrite it to "Response schema" and add the response-title class so it's much easier to target */
  h3s.forEach((h3) => { h3.innerText = "Response schema"; h3.classList.add('response-title') });

  /** Next find all of our 200 OK Response sections */
  let res200OK = document.querySelectorAll('.response-title + div');
  /** Then add the response-200-ok class so they're much easier to target */
  res200OK.forEach((item) => { item.classList.add('response-200-ok') })

  /** These classes have been added to the src/css/custom.css file to apply styles, such as hiding "error" responses */
})();