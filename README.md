# Astronomer Documentation

This repository contains all of the code and content that powers Astro and Astronomer Software [documentation](http://docs.astronomer.io).

## Suggest a Change

If you notice something in our documentation that is wrong, misleading, or could use additional context, the easiest way to make an impact is to create a GitHub issue in this repository. To do so,

1. Go to [Issues](https://github.com/astronomer/docs/issues)
2. Select **New Issue**
3. Depending on the change you have in mind, select a GitHub issue template.
4. Tell us what you think we can do better by answering the questions in the template.

GitHub issues are triaged by the Astronomer team and addressed promptly. Once you create a GitHub issue, our team may follow up with you with additional questions or comments. Once our team has addressed it, you'll get a notification via GitHub that the issue has been closed and that a change is now live.

## Contribute

If you'd like to contribute to Astronomer Docs directly, you are welcome to create a Pull Request (PR) to this repository with your suggested changes. To do so:

1. Fork or clone this repository
2. Create a branch off of `main`
3. Make your changes in that branch.
4. Submit a PR for review.

Once you have submitted a PR for your changes, Netlify will add a comment to your PR that includes a link to a staging website with your changes.

Small edits and typo fixes don't need to be linked to an issue and should be merged quickly. To get a timely review on a larger contribution, we recommend first creating a detailed GitHub issue describing the problem and linking that within your PR.

Every update to the `main` branch of this repository will trigger a rebuild of our production documentation page at https://www.docs.astronomer.io. It might take a few moments for your merged changes to appear.

### Docs Structure

There are two core documentation folders: `astro` and `software`. These folders contain the primary Astronomer docsets that you see by default on Astronomer's documentation site. More specifically, `software `is equivalent **Latest** version of the Astronomer Software docset, which is the docset that users see by default when accesssing `docs.astronomer.io/software`.

![Screen Shot 2022-01-04 at 11 22 19 AM](https://user-images.githubusercontent.com/74574233/148051957-b739ba42-2fc7-4344-b0a0-4f78881fd68c.png)

An additional `software_versioned_docs` folder contains docsets for previous versions of Software. Whenever there's a new release of Astronomer Software, a new versioned docset is copied from `software` and added to this folder, with all links and sidebars updated automatically by Docusuaurs.

If you're working on a change in Software docs, you should work primarily in `software`. Make changes to `software_versioned_docs` only if your change is version-specific or a critical fix (e.g. incorrect/ out-of-date information).

### Build Astronomer Docs Locally

If you want to submit a screenshot, GIF, or a new documentation file, we recommend building and testing your documentation change locally. Astronomer docs are built with [Docusaurus](https://docusaurus.io/), which is our static site generator. Read the following sections for instructions on how to build and test your documentation changes locally with Docusaurus.

#### Installation
To build docs locally, you need to install both Node and Yarn. While Yarn is included in Node, starting in 2020, the Yarn binaries are bundled within [Corepack](https://nodejs.org/api/corepack.html). If you're installing Node for the first time, you need to manually enable Corepacks before you can use Yarn.

1.  Follow the instructions on [Nodejs](https://nodejs.org/en/download/) to install Node, then confirm that you successfully installed Node by running the following command:


    ```sh
    node -version
    ```

2. Run the following command to enable `corepacks` and make Yarn available:

    ```sh
    corepack enable
    ```
After you install Node and enable Yarn with Corepacks, Docusaurus commands are available when you open the `docs` directory from your terminal. 

Please read the [Docusaurus documentation](https://docusaurus.io/docs/installation#requirements) for information on installing other tools you'll need to work with Docusaurus locally.

If you used an alternative package manager to install Node, such as `npm` or `homebrew`, you might need to troubleshoot your install.

#### Troubleshoot Yarn installations

1. Run the following command to check your Node version:

    ```sh
    node --version
    ```
    
2. Adjust your installation based on the output of the command: 

    - **Node and yarn are installed, but need to be updated**: Use a package manager like [npm or nvm](https://www.freecodecamp.org/news/how-to-update-node-and-npm-to-the-latest-version/) to update your version, or download the installer from the [Node.js](https://nodejs.org/en/) site.
    - **Node is installed, but you cannot enable Corepack**: If you installed Node using a package manager, and it's above version 16.10, but Corepack isn't available, follow the instructions for installing [Corepack with npm](https://github.com/nodejs/corepack#manual-installs) or installing [Corepack with Homebrew or nvm](https://stackoverflow.com/questions/70082424/command-not-found-corepack-when-installing-yarn-on-node-v17-0-1), then run the following command to enable Corepack:

    ```sh
    corepack enable
    ```


#### Local Development

To serve a local version of the docs site with your changes, run:

```sh
yarn start
```

You might also need to install `fs-extra` before you can build the site locally. To install it, run:

```sh
yarn add fs-extra
```

This command both builds and serves your local changes. By default, your local build is accessible at `localhost:3000`. From here, any changes you save in your text editor will render on this local site in real time.
