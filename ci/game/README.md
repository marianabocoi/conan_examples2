# Conan Diamond dependency exploration

Given a couple of packages that depend on eachother in the following graph dependency, we want to explore deeper the diamond dependency issue and how we can solve it.

![Dependency Graph](docs/dependency_graph.png)

## Dependency conflict

We can create a dependency conflict by having two separate versions for `mathlib`.

![Dependency Conflict](docs/dependency_conflict.png)

## Running setup locally

1. Make sure you have conan2 installed

    ```sh
    brew install conan@2
    ```

2. Make sure you have a conan profile

    ```sh
    conan profile detect
    ```

3. Set up local C++ artifactory by following the instructions from [here](https://docs.conan.io/2.11/tutorial/conan_repositories/setting_up_conan_remotes/artifactory/artifactory_ce_cpp.html#running-artifactory-ce).
   - Note, you might have the port `8082` if `8081` is already in use.

4. Run the script to upload the packages to the local artifactory

    ```sh
    python build_and_upload.py
    ```

### Cleanup

```sh
# Remove local packages
conan remove -c "*/*@proj/stable"
# Remove remote packages
conan remove -c "*/*@proj/stable" -r conan-local
# Clean ignored or untracked build artefacts
git clean -fdx
```
