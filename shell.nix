let pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  buildInputs = [
    pkgs.pipenv
    pkgs.python35
  ];
}
