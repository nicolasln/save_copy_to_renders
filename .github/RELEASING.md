# Publishing a release

1. Update `version` in `blender_manifest.toml` and push the changes to `main`.
2. Create a matching version tag and push it, for example:

   ```sh
   git tag v1.4.0
   git push origin v1.4.0
   ```

The **Release add-on** workflow checks that the tag matches the manifest, builds
the install ZIP, and publishes a GitHub release with the ZIP attached. It uses
GitHub's built-in token; no additional secrets or local packaging are required.
