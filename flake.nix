{
  description = "Python bindings for Niri";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;
      in
      {
        packages = {
          niripy = python.pkgs.buildPythonPackage {
            pname = "niripy";
            version = "0.2.6";
            pyproject = true;

            src = ./.;

            # Swap the backend to hatchling before building
            postPatch = ''
              substituteInPlace pyproject.toml \
                --replace-fail 'requires = ["uv_build"]' \
                               'requires = ["hatchling"]' \
                --replace-fail 'build-backend = "uv_build"' \
                               'build-backend = "hatchling.build"' \
            '';

            nativeBuildInputs = [
              python.pkgs.hatchling
            ];

            dependencies = [
              python.pkgs.pydantic
            ];

            doCheck = false;

            meta = with pkgs.lib; {
              description = "Python bindings for Niri";
              homepage = "https://github.com/kjmcnamara1/niripy";
              license = licenses.mit;
              maintainers = [
                {
                  name = "Kevin McNamara";
                  email = "kevin.j.mcnamara+tech@proton.me";
                }
              ];
              platforms = platforms.linux;
            };
          };

          default = self.packages.${system}.niripy;
        };

        # Use `nix develop` to enter the dev shell
        devShells.default = pkgs.mkShell {
          inputsFrom = [ self.packages.${system}.default ];
          buildInputs = [
            pkgs.pyright
            python.pkgs.pytest
            python.pkgs.pytest-cov
          ];

          shellHook = ''
            # Adds the src directory to Python's search path
            export PYTHONPATH="$PWD/src:$PYTHONPATH"
            echo "Niripy development environment loaded"
          '';
        };
      }
    );
}
