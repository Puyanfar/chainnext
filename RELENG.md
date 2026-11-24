# Release Engineering Instructions

This document outlines the steps for maintainers to create a new release of the project.

The PyPI package name is **`chainnext`**. The version file still lives at
`backend/chainlit/version.py` because the import package is `chainlit`.
Publishing uploads to https://pypi.org/project/chainnext.

Releases publish only that Python package, via `.github/workflows/publish.yaml`.
Frontend and copilot assets are built into the wheel; they are not separate
downloads. JS packages (`@chainlit/react-client`, `@chainlit/copilot`) are
**not** published to npm. `.github/workflows/publish-libs.yaml` is kept from
upstream but npm publishing is skipped (no `release` trigger; the job only
builds and prints a skip message). Re-enable that workflow only if we start
publishing JS packages to npm.

## Prerequisites

- You must have maintainer permissions on the repo to create a new release.

## Steps

1. **Determine the new version number**:
   - We use semantic versioning (major.minor.patch).
   - Increment the major version for breaking changes, minor version for new features, patch version for bug fixes only.
   - If unsure, discuss with the maintainers to determine if it should be a major/minor version bump or new patch version.

2. **Bump the package version**:
   - Update `version` in `backend/chainlit/version.py`.
   - Update `version` in `libs/*/package.json` only if you are publishing that JS package. The JS packages are currently not published to npm.

3. **Update the changelog**:
   - Create a pull request to update the CHANGELOG.md file with the changes for the new release.
   - Mark any breaking changes clearly.
   - Get the changelog update PR reviewed and merged.

4. **Create a new release**:
   - In the GitHub repo, go to the "Releases" page and click "Draft a new release".
   - Input the new version number as the tag with a `v` prefix (for example `v2.13.0`).
   - Use the "Generate release notes" button to auto-populate the release notes.
   - Review the release notes, make any needed edits for clarity.
   - If this is a full release after an RC, remove any "-rc" suffix from the version number.
   - Publish the release. Publishing the GitHub Release triggers
     `.github/workflows/publish.yaml`, which runs CI, builds the wheel, and
     publishes with PyPI Trusted Publishing (OIDC); no API tokens are required.

   To dry-run a release first, run the **Publish** workflow manually with
   `use_testpypi` enabled (the default for `workflow_dispatch`). Only `main` or a
   published release may publish to PyPI.

5. **Update any associated documentation and examples**:
   - If needed, create PRs to update the version referenced in the docs and example code to match the newly released version.
   - Especially important for documented breaking changes.

## RC (Release Candidate) Releases

- We create RC releases to allow testing before a full stable release
- Append "-rc" to the version number (e.g. 4.0.4-rc)
- Normally only bug fixes, no new features, between an RC and the final release version

Happy releasing!
