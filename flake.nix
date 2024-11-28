# Copyright 2024 TII (SSRC) and the Ghaf contributors
# SPDX-License-Identifier: Apache-2.0
{
  description = "Flake for the SRTA LDPI Project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ self, flake-parts, nixpkgs, ... }:
    flake-parts.lib.mkFlake { inherit self inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
      ];

      perSystem = { system, pkgs, lib, ... }: {
        # Package definitions
        packages = {
          srta-ldpi = pkgs.callPackage ./nixos/packages/ldpi/srta-ldpi.nix { inherit pkgs; };
        };
      };

      flake = {
        # NixOS Module definitions
        nixosModules = {
          ldpi = { config, lib, pkgs, ... }: 
          import ./nixos/modules/ldpi/ldpi.nix {
            pkgs = pkgs;             
            lib = lib;                
          };
        };
      };
    };
}
