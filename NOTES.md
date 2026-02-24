# Notes

## Bump Version

1. Increase version in [pyproject.toml](pyproject.toml) and [uv.lock](uv.lock)
   ```sh
   uv version --bump major/minor/patch
   ```
2. Increase packages.version in [flake.nix](flake.nix) (~line 25)
3. Increase pkver in [PKGBUILD](PKGBUILD) (~line 6)
4. Add section to [CHANGELOG.md](CHANGELOG.md) with version, date, and
   Added/Changed/Deprecated/Removed/Fixed/Security
5. Commit changes
   ```sh
   git add .
   git commit -m "build(release): bump version to {version}"
   ```
6. Tag (annotated) commit with version
   ```sh
   git tag -a v{version} -m "Release version {version}"
   ```
7. Push commits and tag
   ```sh
   git push --follow-tags
   ```
8. CI/CD should run checks, publish release, push to PyPI and AUR, and update the website

## Nix Flake

```sh
# 1. Check if the flake is valid
nix flake check

# 2. See what outputs are available
nix flake show

# 3. Enter the dev shell
nix develop
python --version
python -c "import pydantic; print(pydantic.__version__)"
python -c "import niripy"

# 4. Build the package
nix build

# 5. Or run it directly without installing
nix run

```

## AUR Submission

### Steps for initial publish to AUR

#### [Authentication](https://wiki.archlinux.org/title/AUR_submission_guidelines#Authentication)

1. Add to **~/.ssh/config**

   ```sshconfig
   Host aur.archlinux.org
     User aur
     IdentityFile ~/.ssh/aur
     IdentitiesOnly yes
     AddKeysToAgent yes
   ```

2. Generate ssh key for AUR

   ```sh
   ssh-keygen -f ~/.ssh/aur
   ```

3. Add key to <https://aur.archlinux.org/account/kjmcnamara1/edit> -> **SSH Public Key**

#### Create Package Repository

1. Clone AUR repo (must be _master_ branch)

   ```sh
   git -c init.defaultBranch=master clone ssh://aur@aur.archlinux.org/python-niripy.git
   ```

2. Copy **PKGBUILD** from source repo to local AUR repo

#### Prepare Repository

1. Update _sha256sums_ for **PKGBUILD** in AUR repo (_pacman-contrib_ package required)

   ```sh
   updpkgsums
   ```

2. Test the build locally

   ```sh
   makepkg -si
   ```

3. Generate the **.SRCINFO**

   ```sh
   makepkg --printsrcinfo > .SRCINFO
   ```

4. Generate **.gitignore** that excludes all files and force-adds necessary files

   ```gitignore
   *
   !PKGBUILD
   !.SRCINFO
   !.gitignore
   ```

#### Submit to AUR

1. Commit changes

   ```sh
   git add .
   git commit -m "Initial release {version}"
   ```

2. Push to AUR

   ```sh
   git push origin master
   ```

### Update package on AUR

1. Clone AUR repo

   ```sh
   git clone ssh://aur@aur.archlinux.org/python-niripy.git
   ```

2. Update **PKGBUILD** with new version
3. Update _sha256sums_ with `updpkgsums`
4. Test the build locally with `makepkg -si`
5. Regenerate the **.SRCINFO** with `makepkg --printsrcinfo > .SRCINFO`
6. Commit changes with message `Update to {version}`
7. Push to AUR with `git push origin master`
