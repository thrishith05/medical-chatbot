#!/bin/bash
set -e

echo "Installing Rust..."
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$HOME/.cargo/bin:$PATH"
export CARGO_HOME="$HOME/.cargo"
export RUSTUP_HOME="$HOME/.rustup"

echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build complete!"

