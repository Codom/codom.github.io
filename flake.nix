{
  description = "codom.github.io dev env flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            nodejs_22
            nodePackages.npm
            git
            python3
            (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
              markdown
              pyyaml
            ]))
          ];

          # Environment variables and startup commands
          shellHook = ''
            echo "Node.js + python dev environment loaded!"
            echo "Node version: $(node --version)"
            
            # Add local node_modules binaries to PATH
            export PATH="$PWD/node_modules/.bin:$PATH"
          '';
        };
      });
}
