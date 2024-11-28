# Copyright 2022-2024 TII (SSRC) and the Ghaf contributors
# SPDX-License-Identifier: Apache-2.0
{
  lib,
  pkgs,
  ...
}: 
let
  ldpiPythonEnv = pkgs.callPackage ../../packages/ldpi/srta-ldpi.nix { };

  # Create the PYTHONPATH from propagated build inputs
  pythonPath = builtins.concatStringsSep ":" (
    map (x: 
        "${x}/lib/python3.11/site-packages"
    ) (lib.splitString " " (builtins.readFile (ldpiPythonEnv + "/nix-support/propagated-build-inputs")))
  );
in
{
  config = {
    # Configuring a systemd service for LDPI
    systemd.services.ldpi = {
      description = "Secure Runtime Assurance LDPI Service";
      wantedBy = [ "multi-user.target" ];
      after = [ "network-online.target" ];
      requires = [ "network-online.target" ];

      serviceConfig = {
        Type = "simple";
        User = "root";

        Environment = [
          "PYTHONPATH=${ldpiPythonEnv}/lib/python3.11/site-packages:${pythonPath}"
        ];     
        
        ExecStart = "${pkgs.python311}/bin/python ${ldpiPythonEnv}/lib/python3.11/site-packages/main.py";
        Restart = "on-failure";
        RestartSec = "2";
        RestartForceExitStatus = 1; 
      };
    };
  };
}
