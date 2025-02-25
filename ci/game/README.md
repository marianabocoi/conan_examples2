# Conan Diamond dependency exploration

Given a couple of packages that depend on eachother we weant to explore how the conan cli requests and responses towards artifactory look like for more complex dependency graphs. The graph is at the bottom of the readme.

## Running setup locally

1. Make sure you have conan2 installed

    ```sh
    brew install conan@2
    ```

2. Make sure you have a default conan profile

    ```sh
    conan profile detect
    ```

3. We set up a custom profile that has some [custom settings](https://docs.conan.io/1/extending/custom_settings.html).

    Copy the `default` profile and create a custom profile called `custom_and_env`.

    ```sh
    cp ~/.conan/profiles/default ~/.conan/profiles/custom_and_env
    ```

    Add the custom setting definition to `~/.conan/settings.yml`

    ```sh
    echo 'foo: [None, bar]' >> ~/.conan/settings.yml
    ```

    Add the following to the `custom_and_env` profile:

    ```ini
    ...
    [settings]
        ...
        foo=bar
    ...
    ```

    The setting needs to be added to the game `conanfile.py` package but that is already done in this branch

4. Set up local C++ artifactory by following the instructions from [here](https://docs.conan.io/2.11/tutorial/conan_repositories/setting_up_conan_remotes/artifactory/artifactory_ce_cpp.html#running-artifactory-ce).
   - Note, you might have the port `8082` if `8081` is already in use.
   - Note, the script has hardcoded remote repo name `conan-local`

5. Run the script to upload the packages to the local artifactory (note: the script has hardcoded profile, remote repo name etc.)

    ```sh
    python build_and_upload.py
    ```

1. Run the search command to inspect the requests and responses towards artifactory with [mittdump](https://mitmproxy.org/)

    To configure conan cli to use HTTP proxy edit `~/.conan/conan.conf` and add the proxy address as following:

    ```sh
    vi ~/.conan/conan.conf
    ```

    Under `[proxies]` section add:

    ```ini
    [proxies]
    http = http://0.0.0.0:8080
    https = http://0.0.0.0:8080
    ```

    Run the search command with mitmproxy to capture the requests and responses

    ```sh
    conan search "game/1.0@proj/stable:*" -r conan-local
    ```

### Cleanup

```sh
# Remove local packages
rm -rf ~/.conan/data
# Remove remote packages from artifactory manually
# Clean ignored or untracked build artefacts
git clean -fdx
```

## Dependency graph

![Dependency Graph](docs/dependency_graph.png)
