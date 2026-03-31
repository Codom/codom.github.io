{
  description = "Node.js development environment";

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
          # The packages you want available in your shell
          buildInputs = with pkgs; [
            nodejs_22          # Specific Node version
            nodePackages.npm   # Latest npm
            nodePackages.typescript-language-server
            python3
            (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
              # select Python packages here
              markdown
            ]))
            git
            # Add other tools like pkgs.git, pkgs.gh, etc.
          ];

          # Environment variables and startup commands
          shellHook = ''
            echo "Node.js dev environment loaded!"
            echo "Node version: $(node --version)"
            
            # Optional: Add local node_modules binaries to PATH
            export PATH="$PWD/node_modules/.bin:$PATH"
          '';
        };
      });
}
