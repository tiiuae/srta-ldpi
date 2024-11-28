# Copyright 2022-2024 TII (SSRC) and the Ghaf contributors
# SPDX-License-Identifier: Apache-2.0
{
  pkgs,
  fetchFromGitHub,
  lib,
  src,
}:
let
  inherit (lib) licenses;
in

pkgs.python311Packages.buildPythonApplication {
  pname = "srta-ldpi";
  version = "1.0";
  src = ../../../.;

  propagatedBuildInputs = with pkgs.python311Packages; [
    numpy
    pandas
    scipy
    scikit-learn
    pytorch.out
    matplotlib
    dpkt
    tqdm
    cycler
    netifaces
    systemd
    joblib
    threadpoolctl
    typing-extensions
    (import ./custom_pypcap.nix {
      inherit lib fetchFromGitHub libpcap;
      inherit buildPythonPackage dpkt pytestCheckHook;
    })
  ];

  doCheck = false;

  meta = with lib; {
    description = "SRTA LDPI for Ghaf";
    homepage = "https://github.com/tiiuae/srta-ldpi";
  };
}

