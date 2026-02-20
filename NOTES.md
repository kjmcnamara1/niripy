# Notes

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

   ```bash
   ssh-keygen -f ~/.ssh/aur
   ```

3. Add key to <https://aur.archlinux.org/account/kjmcnamara1/edit> -> **SSH Public Key**

#### Create Package Repository

1. Clone AUR repo (must be _master_ branch)

   ```bash
   git -c init.defaultBranch=master clone ssh://aur@aur.archlinux.org/python-niripy.git
   ```

2. Copy **PKGBUILD** from source repo to local AUR repo

#### Prepare Repository

1. Update _sha256sums_ for **PKGBUILD** in AUR repo (_pacman-contrib_ package required)

   ```bash
   updpkgsums
   ```

2. Test the build locally

   ```bash
   makepkg -si
   ```

3. Generate the **.SRCINFO**

   ```bash
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

   ```bash
   git add .
   git commit -m "Initial release {version}"
   ```

2. Push to AUR

   ```bash
   git push origin master
   ```

### Update package on AUR

1. Clone AUR repo

   ```bash
   git clone ssh://aur@aur.archlinux.org/python-niripy.git
   ```

2. Update **PKGBUILD** with new version
3. Update _sha256sums_ with `updpkgsums`
4. Test the build locally with `makepkg -si`
5. Regenerate the **.SRCINFO** with `makepkg --printsrcinfo > .SRCINFO`
6. Commit changes with message `Update to {version}`
7. Push to AUR with `git push origin master`
