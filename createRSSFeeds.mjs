import fs from "fs-extra";
import xml from "xml";

const posts = [
  {
    title: "December 6, 2022",
    slug: "#December 6, 2022".toLowerCase().replace(/ /g, '-').replace(',', ''),
    content: "<h3 class=\"anchor anchorWithStickyNavbar_LWe7\" id=\"additional-improvements\">Additional improvements<a class=\"hash-link\" href=\"#additional-improvements\" title=\"Direct link to heading\">​</a></h3><ul class=\"\"><li>The maximum possible <strong>Worker Count</strong> for worker queues has been increased from 30 to 100.</li></ul>"
  }
];

async function createRssFeed(websiteURL, feedTitle, feedDescription, feedPageURL, posts) {
  function buildFeed(posts, pageURL) {
    const feedItems = [];
    posts.map((post) => {
      const item = {
        item: [
          { title: post.title },
          {
            link: `${pageURL}/${post.slug}`
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

  const feedSlug = feedTitle.replace(/ /g, "-",).toLowerCase();
  const feedRSSLink = websiteURL + feedSlug + '.rss';

  console.log("Creating XML files for RSS feeds 📡");

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
          { description: feedDescription },
          { language: "en-US" },
          ...buildFeed(posts, feedPageURL),
        ],
      },
    ],
  };

  const feed = '<?xml version="1.0" encoding="UTF-8"?>' + xml(feedObject);

  await fs.writeFile("./static/feed.rss", feed, "utf8");
};

let astroReleaseNotes = '';
fs.readFile('./astro/release-notes.md', 'utf8', (err, data) => {
  astroReleaseNotes = data;
});

console.log(astroReleaseNotes)

createRssFeed("https://docs.astronomer.io/", "Astro Release Notes", "Astronomer is committed to continuous delivery of both features and bug fixes to Astro. To keep your team up to date on what's new, this document will provide a regular summary of all changes released to Astro.", "https://docs.astronomer.io/astro/release-notes", posts)