import fs from "fs-extra";
import xml from "xml";
import { JSDOM } from 'jsdom';
import MarkdownIt from 'markdown-it'
const md = new MarkdownIt();


// Get all the markdown files for release notes
let astro = await fs.readFile('./astro/release-notes.md', 'utf8');
let astroRuntime = await fs.readFile('./astro/runtime-release-notes.md', 'utf8');
let astroCLI = await fs.readFile('./astro/cli/release-notes.md', 'utf8');
let software = await fs.readFile('./software/release-notes.md', 'utf8');
let softwareRuntime = await fs.readFile('./astro/runtime-release-notes.md', 'utf8');

let currentDate = new Date();

// function to get all elements between two elements
function nextUntil(elem, selector, filter) {
  let siblings = [];
  elem = elem.nextElementSibling;
  while (elem) {
    if (elem.matches(selector)) break;
    if (filter && !elem.matches(filter)) {
      elem = elem.nextElementSibling;
      continue;
    }
    siblings.push(elem.outerHTML);
    elem = elem.nextElementSibling;
  }
  return siblings.join('').toString();
};

// this function takes a markdown file imported above, renders to markdown,
// then parses that markdown for the "posts" for our release notes
function getPosts(content) {
  // take md file and use JSDOM to get an HTML fragment we can work with
  const contentRender = JSDOM.fragment(md.render(content));

  // get all of the h2s which are also our post titles
  const H2s = [...contentRender.querySelectorAll("h2")].slice(1);

  // empty array to stick our posts in
  let posts = [];

  // for each h2 create post with title, slug,
  // and get all the content between this h2 until the next h2
  H2s.map((h2) => {
    const postContent = nextUntil(h2, 'h2');
    const postDate = postContent.match(/(?<=Release date: ).*?(?=<.)/sg) || h2.textContent;
    const post = {
      "title": h2.textContent,
      "slug": h2.textContent.toLowerCase().replace(/ /g, '-').replace(',', ''),
      "content": postContent,
      "pubDate": postDate
    };
    posts.push(post);
  })
  return posts;
}

async function createRssFeed(feedTitle, feedDescription, feedPageURL, content) {
  function buildFeed(posts, pageURL) {
    const feedItems = [];
    posts.map((post) => {
      const item = {
        item: [
          { title: post.title },
          {
            link: `${pageURL}#${post.slug.replace(/\./g, '')}`
          },
          {
            guid: `${pageURL}#${post.slug.replace(/\./g, '')}`
          },
          {
            description: {
              _cdata: post.content,
            },
          },
        ]
      };
      feedItems.push(item);
    })
    return feedItems;
  }

  const posts = getPosts(content);

  const websiteURL = "https://docs.astronomer.io/";
  const feedSlug = feedTitle.replace(/ /g, "-",).toLowerCase();
  const feedRSSLink = websiteURL + feedSlug + '.xml';

  console.log(`📡 Creating ${feedTitle} RSS feed`);

  const feedObject = {
    rss: [
      {
        _attr: {
          version: "2.0",
          "xmlns:atom": "http://www.w3.org/2005/Atom",
        },
      },
      {
        channel: [
          {
            "atom:link": {
              _attr: {
                href: feedRSSLink,
                rel: "self",
                type: "application/rss+xml",
              },
            },
          },
          {
            title: feedTitle,
          },
          {
            link: feedPageURL,
          },
          {
            pubDate: currentDate.toUTCString()
          },
          { description: feedDescription },
          { language: "en-US" },
          ...buildFeed(posts, feedPageURL),
        ],
      },
    ],
  };

  const feed = '<?xml version="1.0" encoding="UTF-8"?>' + xml(feedObject);

  await fs.writeFile(`./static/${feedTitle.toLowerCase().replace(/ /g, '-').replace(',', '')}.xml`, feed, "utf8");
};

createRssFeed("Astro Release Notes", "Astronomer is committed to continuous delivery of both features and bug fixes to Astro. To keep your team up to date on what's new, this document will provide a regular summary of all changes released to Astro.", "https://docs.astronomer.io/astro/release-notes", astro);

createRssFeed("Astro Runtime Release Notes", "Astronomer is committed to continuous delivery of both features and bug fixes to Astro. To keep your team up to date on what's new, this document will provide a regular summary of all changes released to Astro Runtime.", "https://docs.astronomer.io/astro/runtime-release-notes", astroRuntime);

createRssFeed("Astro CLI Release Notes", "Astronomer is committed to continuous delivery of both features and bug fixes to Astro. To keep your team up to date on what's new, this document will provide a regular summary of all changes released to Astro CLI.", "https://docs.astronomer.io/astro/cli/release-notes", astroCLI);

createRssFeed("Astro Software Release Notes", "Astronomer is committed to continuous delivery of both features and bug fixes to Astro. To keep your team up to date on what's new, this document will provide a regular summary of all changes released to Astro Software.", "https://docs.astronomer.io/software/release-notes", software);

createRssFeed("Astro Software Runtime Release Notes", "Astronomer is committed to continuous delivery of both features and bug fixes to Astro. To keep your team up to date on what's new, this document will provide a regular summary of all changes released to Astro Software.", "https://docs.astronomer.io/software/runtime-release-notes", softwareRuntime);