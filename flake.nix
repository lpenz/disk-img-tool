{
  description =
    ''
    Resize, list/get/put files and shell into raw disk images
    '';
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages."${system}";
        disk-img-tool = pkgs.python3Packages.buildPythonApplication {
          pname = "disk-img-tool";
          version = "0.1.2";
          src = self;
        };
      in
      rec {
        packages.default = disk-img-tool;
        apps.default = {
          disk-img-tool = {
            type = "app";
            program = "${disk-img-tool}/bin/disk-img-tool";
          };
        };
      }
    );
}
