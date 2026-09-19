# typed: false
# frozen_string_literal: true

# Homebrew Formula for The Ferryman Project
# To install locally from this formula:
#   brew install --formula Formula/ferryman.rb
#
# To distribute via tap:
#   1. Create repository: homebrew-ferryman
#   2. Place this file in Formula/ferryman.rb
#   3. Update url and sha256 with the release tarball hash
#   4. Users install with:
#        brew tap the-ferryman-project/ferryman
#        brew install ferryman

class Ferryman < Formula
  desc "Anti-engagement lifeline for grounded consciousness"
  homepage "https://github.com/the-ferryman-project/ferryman"
  url "https://github.com/the-ferryman-project/ferryman/archive/refs/tags/v0.2.0.tar.gz"
  # Replace with actual SHA256 checksum when creating a GitHub release:
  # curl -sL https://github.com/the-ferryman-project/ferryman/archive/refs/tags/v0.2.0.tar.gz | sha256sum
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "AGPL-3.0-or-later"
  head "https://github.com/the-ferryman-project/ferryman.git", branch: "main"

  depends_on "python@3.12"

  def install
    # Zero external dependencies: install library files into libexec and wrap executable
    libexec.install "ferryman"

    python3 = formula_opt_bin("python@3.12")/"python3.12"
    (bin/"ferryman").write <<~EOS
      #!/usr/bin/env sh
      if [ -n "$PYTHONPATH" ]; then
        export PYTHONPATH="#{libexec}:${PYTHONPATH}"
      else
        export PYTHONPATH="#{libexec}"
      fi
      exec "#{python3}" -m ferryman "$@"
    EOS
    (bin/"ferryman").chmod 0755
  end

  test do
    output = shell_output("#{bin}/ferryman --version")
    assert_match "The Ferryman Project v#{version}", output
    help_output = shell_output("#{bin}/ferryman --help")
    assert_match "Usage:", help_output
  end
end
