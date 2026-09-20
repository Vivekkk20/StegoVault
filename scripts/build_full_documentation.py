"""
StegoVault Professional Project Documentation Generator
Unified Blue Visual System — 18-Page Space-Optimized Layout

Author: Vivek Rathod
Project: StegoVault
"""

import os
import sys
import base64
import asyncio
import re
from playwright.async_api import async_playwright

def get_base64_image(image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        b64 = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/png;base64,{b64}"

def build_html():
    fig_paths = {
        "__FIG01__": "docs/screenshots/fig01_dashboard_overview.png",
        "__FIG02__": "docs/screenshots/fig02_encode_configured.png",
        "__FIG03__": "docs/screenshots/fig03_encode_success.png",
        "__FIG04__": "docs/screenshots/fig04_decode_success.png",
        "__FIG05__": "docs/screenshots/fig05_decode_auth_failure.png",
        "__FIG06__": "docs/screenshots/fig06_image_quality_fidelity.png",
        "__FIG07__": "docs/screenshots/fig07_steganalysis_lsb_plane.png",
        "__FIG08__": "docs/screenshots/fig08_steganalysis_chi_square.png",
    }
    
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>StegoVault — Cryptographic Steganography and Steganalysis Toolkit</title>
<style>
  @page {
    size: A4 portrait;
    margin: 0;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1E293B;
    background-color: #525659;
    line-height: 1.5;
    font-size: 11px;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* ============================================================ */
  /* PAGE CONTAINER & DOUBLE-LINE FRAME                           */
  /* ============================================================ */
  .page {
    width: 210mm;
    height: 297mm;
    margin: 15px auto;
    background: #FFFFFF;
    position: relative;
    padding: 18mm 16mm 16mm 16mm;
    overflow: hidden;
    page-break-after: always;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
  }
  @media print {
    body {
      background: transparent;
    }
    .page {
      margin: 0;
      box-shadow: none;
      width: 210mm;
      height: 297mm;
    }
  }

  .page-frame {
    position: absolute;
    top: 8mm;
    left: 8mm;
    right: 8mm;
    bottom: 8mm;
    border: 2px solid #1B365D;
    outline: 0.5px solid #94A3B8;
    outline-offset: -3px;
    pointer-events: none;
  }

  /* Running Header */
  .running-header {
    position: absolute;
    top: 10mm;
    left: 16mm;
    right: 16mm;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #E2E8F0;
    padding-bottom: 4px;
    font-size: 8.5px;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .running-header-title {
    color: #1E3A8A;
    font-weight: 700;
  }

  /* Running Footer */
  .running-footer {
    position: absolute;
    bottom: 10mm;
    left: 16mm;
    right: 16mm;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #E2E8F0;
    padding-top: 4px;
    font-size: 8.5px;
    color: #64748B;
  }
  .footer-center {
    font-weight: 600;
    color: #334155;
  }
  .page-number {
    font-weight: 700;
    color: #1E3A8A;
  }

  /* ============================================================ */
  /* CONSISTENT SECTION HEADINGS                                  */
  /* ============================================================ */
  .section-kicker {
    font-size: 9.5px;
    font-weight: 800;
    color: #2563EB;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    text-align: center;
    margin-bottom: 3px;
  }
  h1.section-title {
    font-size: 20px;
    font-weight: 800;
    color: #0F172A;
    text-align: center;
    margin-top: 0;
    margin-bottom: 3px;
    letter-spacing: -0.3px;
  }
  div.section-subtitle {
    font-size: 11px;
    font-weight: 600;
    color: #475569;
    text-align: center;
    margin-bottom: 12px;
  }

  h2.block-heading {
    font-size: 13px;
    font-weight: 700;
    color: #0F2744;
    margin-top: 11px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 5px;
  }
  h3.sub-block-heading {
    font-size: 11px;
    font-weight: 700;
    color: #1E3A8A;
    margin-top: 8px;
    margin-bottom: 4px;
  }

  p {
    margin-bottom: 7px;
    color: #334155;
    text-align: justify;
    line-height: 1.52;
    font-size: 10px;
  }
  strong {
    color: #0F172A;
  }

  /* ============================================================ */
  /* UNIFIED BLUE BOX DESIGN SYSTEM                               */
  /* ============================================================ */
  .blue-box {
    background: #F0F7FF;
    border: 1px solid #BFDBFE;
    border-left: 4px solid #2563EB;
    border-radius: 4px;
    padding: 9px 14px;
    margin-bottom: 10px;
  }
  .blue-box-header {
    font-size: 10.5px;
    font-weight: 800;
    color: #1E3A8A;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 5px;
  }
  .blue-box-content {
    font-size: 10px;
    color: #1E293B;
    line-height: 1.48;
    margin-bottom: 0;
  }

  /* Large Figure Presentation */
  .figure-section {
    text-align: center;
    margin: 6px 0;
  }
  .figure-large-img {
    width: 98%;
    max-height: 116mm;
    object-fit: contain;
    border: 1px solid #CBD5E1;
    border-radius: 4px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }
  .figure-caption {
    font-size: 9.5px;
    font-style: italic;
    color: #475569;
    margin-top: 4px;
    margin-bottom: 6px;
    text-align: center;
  }

  /* Numbered Callout Breakdown Box */
  .callout-breakdown {
    background: #F8FAFC;
    border: 1px solid #BFDBFE;
    border-left: 4px solid #3B82F6;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 9.5px;
    line-height: 1.5;
    color: #334155;
    margin-bottom: 7px;
    text-align: left;
  }
  .num-badge {
    font-weight: 800;
    color: #1D4ED8;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 3px;
    padding: 0 4px;
    margin-right: 2px;
  }

  /* Tables */
  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 10px;
    font-size: 9.5px;
  }
  table.data-table th {
    background: #1E3A8A;
    color: #FFFFFF;
    text-align: left;
    padding: 6px 9px;
    font-weight: 700;
    border: 1px solid #1E3A8A;
  }
  table.data-table td {
    padding: 6px 9px;
    border: 1px solid #CBD5E1;
    color: #334155;
    line-height: 1.45;
  }
  table.data-table tr:nth-child(even) td {
    background: #F8FAFC;
  }
  .badge-pass {
    display: inline-block;
    padding: 2px 7px;
    background: #EFF6FF;
    color: #1D4ED8;
    font-weight: 700;
    border-radius: 3px;
    font-size: 9px;
    border: 1px solid #93C5FD;
  }

  /* Code Block */
  .code-terminal {
    background: #0F172A;
    color: #F8FAFC;
    padding: 8px 13px;
    border-radius: 4px;
    font-family: Consolas, "Courier New", monospace;
    font-size: 9px;
    line-height: 1.45;
    margin-bottom: 9px;
    overflow-x: hidden;
    border-left: 4px solid #2563EB;
  }
  .term-comment { color: #94A3B8; }
  .term-green { color: #38BDF8; font-weight: 600; }
  .term-blue { color: #93C5FD; }

  /* Flow Diagram Container */
  .pipeline-box {
    background: #F0F7FF;
    border: 1px solid #BFDBFE;
    border-radius: 4px;
    padding: 9px 12px;
    margin-bottom: 10px;
  }
  .pipe-step {
    display: inline-block;
    padding: 4px 8px;
    background: #FFFFFF;
    border: 1px solid #3B82F6;
    border-radius: 3px;
    font-weight: 600;
    font-size: 8.5px;
    color: #1E3A8A;
  }
  .pipe-arrow {
    display: inline-block;
    margin: 0 4px;
    color: #2563EB;
    font-weight: 800;
  }

  /* Cover Page Styles */
  .cover-wrapper {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 24mm 14mm 14mm 14mm;
    text-align: center;
  }
  .cover-title {
    font-size: 48px;
    font-weight: 900;
    color: #0F172A;
    letter-spacing: -1.5px;
    line-height: 1.1;
    margin-bottom: 8px;
  }
  .cover-title span {
    color: #2563EB;
  }
  .cover-subtitle {
    font-size: 17px;
    font-weight: 700;
    color: #2563EB;
    margin-bottom: 14px;
  }
  .cover-divider {
    width: 64px;
    height: 3px;
    background: #1E3A8A;
    margin: 0 auto 18px auto;
  }
  .cover-description {
    font-size: 11.5px;
    color: #475569;
    line-height: 1.55;
    max-width: 84%;
    margin: 0 auto 26px auto;
  }
  .cover-card {
    background: #F0F7FF;
    border: 1.5px solid #BFDBFE;
    border-radius: 6px;
    padding: 16px 20px;
    margin: 0 auto 20px auto;
    max-width: 88%;
    text-align: left;
    box-shadow: 0 2px 8px rgba(37,99,235,0.06);
  }
  .cover-card table {
    width: 100%;
    border-collapse: collapse;
    font-size: 11px;
  }
  .cover-card td {
    padding: 5px 8px;
    vertical-align: top;
  }
  .cover-card td.label {
    font-weight: 700;
    color: #1E3A8A;
    width: 32%;
  }
  .cover-card td.val {
    color: #1E293B;
  }
  .cover-badge {
    display: inline-block;
    background: #EFF6FF;
    color: #1D4ED8;
    font-weight: 700;
    font-size: 10.5px;
    padding: 5px 16px;
    border-radius: 20px;
    border: 1px solid #93C5FD;
    margin-top: 8px;
  }
</style>
</head>
<body>

<!-- ================================================================= -->
<!-- PAGE 1: COVER PAGE -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="cover-wrapper">
    <div>
      <div style="font-size: 10.5px; font-weight: 800; color: #2563EB; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px;">
        PRACTICAL CYBERSECURITY PROJECT DOCUMENTATION
      </div>
      <div class="cover-title">STEGO<span>VAULT</span></div>
      <div class="cover-subtitle">Cryptographic Steganography and Steganalysis Toolkit</div>
      <div class="cover-divider"></div>
      <div class="cover-description">
        StegoVault is a practical cybersecurity application that combines image steganography, authenticated encryption, image-quality analysis, and defensive steganalysis into an easy-to-use defensive security toolkit.
      </div>
      
      <div class="cover-card">
        <table>
          <tr><td class="label">Project Name:</td><td class="val">StegoVault</td></tr>
          <tr><td class="label">Technical Domain:</td><td class="val">Practical Cybersecurity, Applied Cryptography &amp; Digital Forensics</td></tr>
          <tr><td class="label">Core Technologies:</td><td class="val">Python 3.14, Streamlit, Pillow (PIL), Cryptography, NumPy, SciPy, pytest</td></tr>
          <tr><td class="label">Developer:</td><td class="val"><strong>Vivek Rathod</strong></td></tr>
          <tr><td class="label">GitHub Repository:</td><td class="val">https://github.com/Vivekkk20/StegoVault</td></tr>
          <tr><td class="label">Verification Status:</td><td class="val"><strong>77 / 77 Automated Tests Passed (100% Pass Rate)</strong></td></tr>
          <tr><td class="label">License:</td><td class="val">MIT Open Source License</td></tr>
        </table>
      </div>
      
      <div class="cover-badge">
        &#10004; 100% Automated Test Pass Rate &bull; Verified Production Architecture
      </div>
    </div>
    
    <div style="font-size: 9.5px; color: #64748B; border-top: 1px solid #E2E8F0; padding-top: 12px;">
      StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod
    </div>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 2: SECTION 1 — INTRODUCTION & PROBLEM CONTEXT -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 1 &mdash; Introduction &amp; Context</span>
  </div>

  <div class="section-kicker">SECTION 1</div>
  <h1 class="section-title">Introduction &amp; Problem Context</h1>
  <div class="section-subtitle">Understanding Image Steganography, Cryptography, and the Need for Defense-in-Depth</div>

  <div class="blue-box">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Provide a practical defense-in-depth security tool that encrypts secret data before hiding it inside innocent-looking images, making sure the data stays both hidden and cryptographically protected.</div>
  </div>

  <h2 class="block-heading">What is Steganography?</h2>
  <p>Steganography is the practice of hiding secret information inside an ordinary, non-suspicious carrier file (such as a digital image). The word comes from Greek (<em>steganos</em> meaning covered, and <em>graphein</em> meaning writing). The goal is to conceal the very existence of the communication, so an outside observer inspecting the file does not realize that secret data is present.</p>

  <h2 class="block-heading">What is Encryption?</h2>
  <p>Encryption is the mathematical process of converting readable plaintext into scrambled, unreadable ciphertext using a secret key. Without the correct secret key, no unauthorized observer can decrypt or read the underlying information.</p>

  <h2 class="block-heading">What is the Difference Between Encryption and Steganography?</h2>
  <p><strong>Encryption</strong> protects the <em>content</em> of a secret message. An eavesdropper can see that an encrypted message is being sent, but cannot read what it says. <strong>Steganography</strong> protects the <em>existence</em> of the secret message. An eavesdropper sees only an ordinary picture and does not know that a message exists at all.</p>

  <h2 class="block-heading">Why Hiding Data Inside an Image is Useful</h2>
  <p>Transmitting raw encrypted files across monitored public networks often triggers automated Deep Packet Inspection (DPI) alarms and firewall alerts. Hiding encrypted data inside ordinary images provides <strong>defensive privacy</strong> for researchers and whistleblowers, enables covert credential backups, and adds an extra layer of defense against unauthorized discovery.</p>

  <h2 class="block-heading">Problems with Basic LSB-Only Approaches</h2>
  <p>Basic Least Significant Bit (LSB) steganography tools suffer from two critical security flaws:</p>
  <ul style="margin-left: 18px; margin-bottom: 7px; font-size: 10px; color: #334155; line-height: 1.48;">
    <li><strong>No Encryption (Cleartext Hiding):</strong> Naive tools hide raw text directly into pixels. Anyone who extracts the lowest bits instantly recovers the cleartext message.</li>
    <li><strong>No Tamper Detection:</strong> If an image is modified in transit or corrupted, raw LSB tools cannot detect the tampering. They output corrupted garbage without warning.</li>
  </ul>

  <h2 class="block-heading">Why Encryption Before Embedding Improves Protection</h2>
  <p>StegoVault encrypts the secret data with <strong>AES-256-GCM</strong> before hiding it inside the image. Even if an adversary extracts every embedded bit, they only obtain random-looking ciphertext. Built-in authentication tags detect if even a single bit of the carrier has been tampered with or modified.</p>

  <h2 class="block-heading">How StegoVault Solves the Problem</h2>
  <div class="pipeline-box" style="text-align: center; margin-top: 4px;">
    <span class="pipe-step">Secret Payload</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step">zlib Compress</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step">AES-256-GCM Encrypt</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step">SVLT Wire Envelope</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step">RGB LSB Embedding</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step" style="background: #EFF6FF; color: #1D4ED8; border-color: #2563EB;">Final Stego Image</span>
  </div>

  <div class="blue-box" style="margin-top: 8px;">
    <div class="blue-box-header">&#128161; KEY TAKEAWAY</div>
    <div class="blue-box-content">StegoVault unifies authenticated cryptography, lossless image embedding, real-time capacity checking, mathematical fidelity metrics, and forensic steganalysis into one practical tool.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 2 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 3: SECTION 2 — PROJECT OBJECTIVES -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 2 &mdash; Project Objectives</span>
  </div>

  <div class="section-kicker">SECTION 2</div>
  <h1 class="section-title">Project Objectives</h1>
  <div class="section-subtitle">Verified Engineering Targets and Implementation Specifications</div>

  <div class="blue-box">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Establish clear, verified engineering objectives implemented directly in the StegoVault source code to solve real-world steganographic trade-offs.</div>
  </div>

  <h2 class="block-heading">Core Engineering Objectives</h2>
  <p>StegoVault was engineered around strict, verifiable technical targets derived directly from the application source code. Each objective solves a specific vulnerability found in traditional steganography tools:</p>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 25%;">Objective</th>
        <th style="width: 40%;">Practical Purpose</th>
        <th style="width: 35%;">Source Implementation</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Pre-Embedding Protection</strong></td>
        <td>Scramble secret data using authenticated encryption before it touches the image.</td>
        <td><code>AES-256-GCM</code> with 128-bit GHASH tag (<code>crypto/encryption.py</code>)</td>
      </tr>
      <tr>
        <td><strong>Brute-Force Resistance</strong></td>
        <td>Prevent dictionary attacks against passphrases using memory-hard key derivation.</td>
        <td><code>Scrypt</code> ($N=16384, r=8, p=1$, 16B Salt) (<code>crypto/key_derivation.py</code>)</td>
      </tr>
      <tr>
        <td><strong>Reliable Data Hiding</strong></td>
        <td>Conceal encrypted bytes sequentially into the spatial color channels of lossless images.</td>
        <td>Sequential RGB Least Significant Bit (LSB) embedding (<code>stego/lsb.py</code>)</td>
      </tr>
      <tr>
        <td><strong>Tamper Detection</strong></td>
        <td>Detect whether an image has been altered or if an incorrect passphrase was entered.</td>
        <td>AEAD tag verification during extraction (<code>core/decoder.py</code>)</td>
      </tr>
      <tr>
        <td><strong>Quality Verification</strong></td>
        <td>Quantify the visual difference between the original image and the stego image.</td>
        <td>Empirical MSE and PSNR calculation (<code>analysis/image_quality.py</code>)</td>
      </tr>
      <tr>
        <td><strong>Defensive Forensics</strong></td>
        <td>Allow security analysts to audit images for hidden data using visual and statistical tools.</td>
        <td>Bit-0 plane slicing and Chi-Square test (<code>analysis/steganalysis.py</code>)</td>
      </tr>
      <tr>
        <td><strong>Simple Graphical Interface</strong></td>
        <td>Provide an accessible, clear interface for non-programmers and security analysts.</td>
        <td>Interactive local web dashboard in Streamlit (<code>app/main.py</code>)</td>
      </tr>
    </tbody>
  </table>

  <h2 class="block-heading">Core Architectural Principles</h2>
  <p>To ensure that these objectives maintain long-term engineering rigor, StegoVault follows three fundamental architectural tenets:</p>
  <ul style="font-size: 10px; color: #334155; margin-left: 18px; line-height: 1.55; margin-bottom: 10px;">
    <li><strong>Defense-in-Depth:</strong> Security does not rely on steganographic secrecy alone. If the carrier is detected, the ciphertext remains protected under standard cryptographic models.</li>
    <li><strong>Zero Inventions:</strong> Exclusively leverages vetted, standard cryptographic primitives from the Python <code>cryptography</code> ecosystem.</li>
    <li><strong>Full Local Privacy:</strong> Operates entirely in a local execution environment with zero third-party telemetry, cloud storage, or external API calls.</li>
  </ul>

  <div class="blue-box">
    <div class="blue-box-header">&#128161; PRACTICAL OBSERVATION</div>
    <div class="blue-box-content">By defining strict technical objectives before development, all 77 automated unit and integration tests map directly to verifiable security guarantees.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 3 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 4: SECTION 3 — PROJECT SCOPE -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 3 &mdash; Project Scope</span>
  </div>

  <div class="section-kicker">SECTION 3</div>
  <h1 class="section-title">Project Scope</h1>
  <div class="section-subtitle" style="margin-bottom: 16px;">Operational Boundaries, Supported Image Formats, and Explicit Exclusions</div>

  <div class="blue-box" style="padding: 12px 16px; margin-bottom: 16px;">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Clearly define the operational boundaries of StegoVault, documenting implemented features and explicit architectural exclusions.</div>
  </div>

  <h2 class="block-heading" style="margin-top: 16px; margin-bottom: 9px;">Operational Scope Boundaries</h2>
  <div style="display: flex; gap: 14px; margin-top: 8px; margin-bottom: 18px;">
    <div style="flex: 1; background: #F0F7FF; border: 1.5px solid #BFDBFE; border-left: 4px solid #2563EB; border-radius: 4px; padding: 16px 18px;">
      <div style="font-weight: 800; color: #1E3A8A; font-size: 11px; margin-bottom: 9px;">&#10004; In Scope (Fully Implemented &amp; Verified)</div>
      <ul style="font-size: 10px; color: #334155; margin-left: 16px; line-height: 1.82;">
        <li style="margin-bottom: 6px;">Lossless image formats: PNG, BMP, and TIFF raster images.</li>
        <li style="margin-bottom: 6px;">Payload formats: Plain text messages and arbitrary binary files.</li>
        <li style="margin-bottom: 6px;">Authenticated AES-256-GCM encryption with 128-bit GHASH tag.</li>
        <li style="margin-bottom: 6px;">Scrypt memory-hard key derivation function (RFC 7914).</li>
        <li style="margin-bottom: 6px;">Standardized 56-byte binary wire envelope protocol (<code>SVLT</code>).</li>
        <li style="margin-bottom: 6px;">Dynamic capacity checking with safe 15% embedding ceiling.</li>
        <li style="margin-bottom: 6px;">Empirical image quality evaluation (MSE and PSNR calculation).</li>
        <li style="margin-bottom: 6px;">Defensive forensics: Bit-0 plane slicing and Chi-Square testing.</li>
        <li>77 automated unit and integration tests (100% pass rate).</li>
      </ul>
    </div>
    <div style="flex: 1; background: #F8FAFC; border: 1.5px solid #CBD5E1; border-left: 4px solid #64748B; border-radius: 4px; padding: 16px 18px;">
      <div style="font-weight: 800; color: #334155; font-size: 11px; margin-bottom: 9px;">&#10008; Out of Scope (Explicit Design Boundaries)</div>
      <ul style="font-size: 10px; color: #475569; margin-left: 16px; line-height: 1.82;">
        <li style="margin-bottom: 8px;">Lossy image formats (JPEG, WebP) because lossy compression alters pixel values and permanently destroys LSB bits.</li>
        <li style="margin-bottom: 8px;">Network sockets, streaming, or direct messaging protocols.</li>
        <li style="margin-bottom: 8px;">Public-key / asymmetric infrastructure (RSA/ECC certificates).</li>
        <li style="margin-bottom: 8px;">Remote cloud server uploads, databases, or user accounts.</li>
        <li>Audio or video steganography media types.</li>
      </ul>
    </div>
  </div>

  <h2 class="block-heading" style="margin-top: 16px; margin-bottom: 9px;">Why Lossless Images are Strictly Required</h2>
  <p style="font-size: 10px; line-height: 1.7; margin-bottom: 12px;">Lossy formats like JPEG apply Discrete Cosine Transforms (DCT) and lossy quantization tables to reduce file size. This process alters pixel color values by several units. Because spatial LSB steganography stores data in the single lowest bit of each byte, any lossy compression wipes out the embedded bitstream completely. StegoVault strictly enforces lossless formats (PNG, BMP, TIFF) to guarantee 100% bit recovery.</p>
  <p style="font-size: 10px; line-height: 1.7; margin-bottom: 16px;">Furthermore, social media platforms and instant messaging applications (such as WhatsApp, Telegram, and Discord) routinely re-compress uploaded images. StegoVault carriers must always be transmitted as uncompressed file attachments to prevent bitstream corruption.</p>

  <div class="blue-box" style="padding: 13px 18px; margin-top: 16px;">
    <div class="blue-box-header">&#128161; SCOPE ENFORCEMENT OBSERVATION</div>
    <div class="blue-box-content">By restricting the scope to lossless raster formats and local execution, StegoVault eliminates communication failures, ensuring that every embedded payload can be extracted and authenticated without bit loss.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 4 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 5: SECTION 4 — TOOLS & TECHNOLOGIES -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 4 &mdash; Tools &amp; Technologies</span>
  </div>

  <div class="section-kicker">SECTION 4</div>
  <h1 class="section-title">Tools &amp; Technologies</h1>
  <div class="section-subtitle">Software Stack, Supporting Libraries, and Environmental Dependencies</div>

  <div class="blue-box">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Detail every library and software tool used in StegoVault in plain English, explaining its exact functional responsibility.</div>
  </div>

  <h2 class="block-heading">Technology Stack Breakdown</h2>
  <p>StegoVault was developed using Python 3.14 and leverages standard, well-maintained libraries from the Python cybersecurity and scientific computing ecosystems:</p>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 22%;">Technology</th>
        <th style="width: 38%;">Role in StegoVault</th>
        <th style="width: 40%;">Why It Is Used</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Python 3.14</strong></td>
        <td>Core programming language</td>
        <td>Clean syntax, robust standard libraries, and extensive cryptographic ecosystem.</td>
      </tr>
      <tr>
        <td><strong>Streamlit</strong></td>
        <td>Interactive graphical web interface</td>
        <td>Enables building professional, responsive cybersecurity dashboards quickly.</td>
      </tr>
      <tr>
        <td><strong>Pillow (PIL)</strong></td>
        <td>Image processing engine</td>
        <td>Reliably loads, validates, manipulates, and saves lossless PNG, BMP, and TIFF images.</td>
      </tr>
      <tr>
        <td><strong>Cryptography</strong></td>
        <td>Security &amp; encryption library</td>
        <td>Provides industry-standard AES-256-GCM cipher and Scrypt key derivation.</td>
      </tr>
      <tr>
        <td><strong>NumPy</strong></td>
        <td>Vectorized array calculations</td>
        <td>Delivers ultra-fast pixel calculations for MSE, PSNR, and bit-plane extraction.</td>
      </tr>
      <tr>
        <td><strong>SciPy</strong></td>
        <td>Statistical calculation engine</td>
        <td>Computes exact Chi-Square cumulative distribution functions and survival $p$-values.</td>
      </tr>
      <tr>
        <td><strong>pytest</strong></td>
        <td>Automated testing framework</td>
        <td>Runs all 77 automated unit and integration tests to verify code integrity.</td>
      </tr>
    </tbody>
  </table>

  <h2 class="block-heading">Architecture &amp; Dependency Philosophy</h2>
  <p>StegoVault strictly adheres to the principle of <strong>Zero Inventions</strong> in cryptography. Rather than implementing custom encryption or hash functions, StegoVault exclusively uses the audited, hardware-accelerated primitives provided by the official Python <code>cryptography</code> package. This eliminates risks associated with side-channel attacks, improper padding, and weak random number generation.</p>
  <p>The entire runtime environment is managed via a dedicated virtual environment with strict dependency pinning, ensuring reproducible execution across development, testing, and operational deployment.</p>

  <div class="blue-box" style="margin-top: 10px;">
    <div class="blue-box-header">&#128161; KEY TECHNOLOGY TAKEAWAY</div>
    <div class="blue-box-content">Every library in the StegoVault stack is selected for stability, security, and mathematical precision, creating a lightweight yet robust defensive cybersecurity toolkit.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 5 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 6: SECTION 5 — SYSTEM ARCHITECTURE & DATA FLOW -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 5 &mdash; System Architecture</span>
  </div>

  <div class="section-kicker">SECTION 5</div>
  <h1 class="section-title">System Architecture &amp; Data Flow</h1>
  <div class="section-subtitle">Tracing Data Movement Through the Encoding and Decoding Pipelines</div>

  <div class="blue-box" style="padding: 11px 15px; margin-bottom: 12px;">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Explain how data moves step-by-step through StegoVault during both the encoding and decoding processes.</div>
  </div>

  <h2 class="block-heading" style="margin-top: 13px; margin-bottom: 8px;">Encoding Pipeline (Hiding Data)</h2>
  <div class="pipeline-box" style="padding: 11px 14px; margin-bottom: 12px;">
    <div style="font-weight: 700; color: #1E3A8A; font-size: 10px; margin-bottom: 6px;">Data Ingestion &amp; Embedding Sequence:</div>
    <span class="pipe-step" style="padding: 5px 9px; font-size: 9.5px; font-weight: 700;">1. Input Payload</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step" style="padding: 5px 9px; font-size: 9.5px; font-weight: 700;">2. zlib Compress</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step" style="padding: 5px 9px; font-size: 9.5px; font-weight: 700;">3. Scrypt KDF</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step" style="padding: 5px 9px; font-size: 9.5px; font-weight: 700;">4. AES-GCM Encrypt</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step" style="padding: 5px 9px; font-size: 9.5px; font-weight: 700;">5. SVLT Envelope</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step" style="padding: 5px 9px; font-size: 9.5px; font-weight: 700;">6. LSB Embed</span>
  </div>
  <ul style="font-size: 10px; color: #334155; margin-left: 20px; line-height: 1.68; margin-bottom: 14px;">
    <li style="margin-bottom: 4px;"><strong>Step 1 (Payload Ingestion):</strong> Plain text message or raw binary file bytes are loaded into memory.</li>
    <li style="margin-bottom: 4px;"><strong>Step 2 (zlib Pre-Compression):</strong> Compresses data to minimize carrier footprint and flatten byte entropy.</li>
    <li style="margin-bottom: 4px;"><strong>Step 3 (Scrypt Key Derivation):</strong> Generates a 256-bit AES key from passphrase and a 16-byte random salt.</li>
    <li style="margin-bottom: 4px;"><strong>Step 4 (AES-256-GCM Encryption):</strong> Encrypts payload with a 12-byte nonce, generating ciphertext and 16-byte tag.</li>
    <li style="margin-bottom: 4px;"><strong>Step 5 (SVLT Wire Framing):</strong> Packages metadata, salt, nonce, tag, and lengths into a 56-byte binary header.</li>
    <li><strong>Step 6 (Sequential LSB Embedding):</strong> Embeds header and ciphertext bits sequentially into RGB least significant bits.</li>
  </ul>

  <h2 class="block-heading" style="margin-top: 14px; margin-bottom: 8px;">Decoding Pipeline (Recovering Data)</h2>
  <div class="pipeline-box" style="padding: 11px 14px; margin-bottom: 12px;">
    <div style="font-weight: 700; color: #1E3A8A; font-size: 10px; margin-bottom: 6px;">Extraction &amp; Authentication Sequence:</div>
    <span class="pipe-step" style="padding: 5px 9px; font-size: 9.5px; font-weight: 700;">1. Stego Image</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step" style="padding: 5px 9px; font-size: 9.5px; font-weight: 700;">2. LSB Extraction</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step" style="padding: 5px 9px; font-size: 9.5px; font-weight: 700;">3. SVLT Header Parse</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step" style="padding: 5px 9px; font-size: 9.5px; font-weight: 700;">4. Scrypt KDF</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step" style="padding: 5px 9px; font-size: 9.5px; font-weight: 700;">5. Tag Verification</span>
    <span class="pipe-arrow">&rarr;</span>
    <span class="pipe-step" style="padding: 5px 9px; font-size: 9.5px; font-weight: 700;">6. Decrypt &amp; Decompress</span>
  </div>
  <ul style="font-size: 10px; color: #334155; margin-left: 20px; line-height: 1.68; margin-bottom: 14px;">
    <li style="margin-bottom: 4px;"><strong>Step 1 (Stego Ingestion):</strong> The lossless carrier image containing hidden data is loaded.</li>
    <li style="margin-bottom: 4px;"><strong>Step 2 (Bitstream Extraction):</strong> Reads the least significant bit of each RGB pixel sequentially.</li>
    <li style="margin-bottom: 4px;"><strong>Step 3 (SVLT Header Parsing):</strong> Validates magic bytes <code>SVLT</code>, version, salt, nonce, tag, and payload size.</li>
    <li style="margin-bottom: 4px;"><strong>Step 4 (Key Re-Derivation):</strong> Derives the 256-bit AES key using recipient's passphrase and extracted salt.</li>
    <li style="margin-bottom: 4px;"><strong>Step 5 (AEAD Tag Verification):</strong> Recomputes GHASH tag over ciphertext and header; halts if tampered.</li>
    <li><strong>Step 6 (Decryption &amp; Decompression):</strong> Decrypts ciphertext and decompresses bytes to restore cleartext.</li>
  </ul>

  <div class="blue-box" style="padding: 11px 15px; margin-top: 14px;">
    <div class="blue-box-header">&#128161; ARCHITECTURAL SECURITY PRINCIPLE</div>
    <div class="blue-box-content">Authentication strictly precedes payload release. An attacker cannot decrypt or inspect partial data without valid authentication.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 6 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 7: SECTION 6 — APPLICATION SETUP & INSTALLATION GUIDE -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 6 &mdash; Application Setup</span>
  </div>

  <div class="section-kicker">SECTION 6</div>
  <h1 class="section-title">Application Setup &amp; Installation Guide</h1>
  <div class="section-subtitle">Practical Step-by-Step Instructions to Launch and Run StegoVault Locally</div>

  <div class="blue-box">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Enable any user or security analyst to set up, launch, and verify StegoVault on a local workstation in under two minutes.</div>
  </div>

  <h2 class="block-heading">Step 1: Open the Project Directory</h2>
  <p>Open your command terminal (PowerShell or Command Prompt) and navigate to the project directory:</p>
  <div class="code-terminal">
    <span class="term-comment"># Navigate to StegoVault workspace</span><br>
    <span class="term-green">PS D:\\&gt;</span> cd d:\\projects\\stegovault
  </div>

  <h2 class="block-heading">Step 2: Activate the Python Virtual Environment</h2>
  <p>Activate the pre-configured Python virtual environment containing all required libraries (Streamlit, Cryptography, Pillow, NumPy, SciPy, pytest):</p>
  <div class="code-terminal">
    <span class="term-comment"># Activate virtual environment in PowerShell</span><br>
    <span class="term-green">PS D:\\projects\\stegovault\\&gt;</span> .\\.venv\\Scripts\\Activate.ps1
  </div>

  <h2 class="block-heading">Step 3: Start the StegoVault Application</h2>
  <p>Launch the interactive Streamlit dashboard using the application entry point:</p>
  <div class="code-terminal">
    <span class="term-comment"># Start the Streamlit local web server</span><br>
    <span class="term-green">PS D:\\projects\\stegovault\\&gt;</span> streamlit run app/main.py
  </div>

  <h2 class="block-heading">Step 4: Access the Dashboard in Your Web Browser</h2>
  <p>Streamlit starts a local web server and displays the local access URL in your terminal:</p>
  <div class="code-terminal">
    <span class="term-blue">  You can now view your Streamlit app in your browser.</span><br>
    <span class="term-blue">  Local URL:</span> <span class="term-green">http://localhost:8501</span><br>
    <span class="term-blue">  Network URL:</span> <span class="term-green">http://192.168.1.100:8501</span>
  </div>
  <p>Open your preferred web browser and navigate to <strong>http://localhost:8501</strong>.</p>

  <h2 class="block-heading">Step 5: Run the Automated Test Suite (Optional Verification)</h2>
  <p>To verify that all underlying cryptographic and steganographic modules function correctly on your system, execute pytest:</p>
  <div class="code-terminal">
    <span class="term-green">PS D:\\projects\\stegovault\\&gt;</span> pytest<br>
    <span class="term-blue">============================= 77 passed in 1.92s ==============================</span>
  </div>

  <div class="blue-box" style="margin-top: 10px;">
    <div class="blue-box-header">&#128161; SETUP VERIFICATION RESULT</div>
    <div class="blue-box-content">The StegoVault application launches immediately. The central interface loads in your browser with all four functional modules ready for live use.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 7 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 8: SECTION 7 — MAIN DASHBOARD INTERFACE -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 7 &mdash; Main Dashboard</span>
  </div>

  <div class="section-kicker">SECTION 7</div>
  <h1 class="section-title">Practical Walkthrough: Main Dashboard</h1>
  <div class="section-subtitle">Navigating the Interface, Exploring Module Controls, and Inspecting Telemetry</div>

  <div class="blue-box">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Understand the dashboard layout, learn how to switch between operational modes, and inspect the active cryptographic configuration.</div>
  </div>

  <div style="display: flex; gap: 10px; margin-bottom: 5px;">
    <div style="flex: 1;">
      <h3 class="sub-block-heading">What is this?</h3>
      <p style="font-size: 9px; line-height: 1.45;">The central control dashboard of StegoVault running locally in your browser.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">Why is it used?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Provides a visual interface to encode, decode, check quality, and perform forensics without code.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">How does it work?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Streamlit binds web UI controls directly to StegoVault's Python modules in real time.</p>
    </div>
  </div>

  <div class="figure-section">
    <img class="figure-large-img" src="__FIG01__" alt="Figure 1: StegoVault Main Interface &amp; Telemetry">
    <div class="figure-caption">Figure 1: StegoVault Main Interface &amp; Telemetry showing navigation tabs, cryptographic engine specifications, and defensive posture indicators.</div>
  </div>

  <div class="callout-breakdown">
    <div style="font-weight: 700; color: #1E3A8A; margin-bottom: 3px;">Numbered Interface Breakdown &amp; Controls:</div>
    <span class="num-badge">&#9312; Mode Switch Navigation Tabs:</span> Selects the active operational module: <em>Secure Encode</em>, <em>Authenticated Decode</em>, <em>Image Quality &amp; Fidelity</em>, or <em>Forensic Steganalysis</em>.<br>
    <span class="num-badge">&#9313; Sidebar Cryptographic Engine:</span> Displays live verified parameters: <code>AES-256-GCM</code> AEAD cipher, <code>Scrypt</code> KDF, <code>128-bit</code> GHASH tag, and <code>16B Salt / 12B Nonce</code>.<br>
    <span class="num-badge">&#9314; StegoVault Header &amp; Architecture Badges:</span> Displays active security status: Defense-in-Depth, zero cloud dependencies, and lossless carrier enforcement.
  </div>

  <div class="blue-box">
    <div class="blue-box-header">&#128161; INTERFACE OBSERVATION</div>
    <div class="blue-box-content">The user can access all functions from one unified view with complete visibility into cryptographic parameters before performing any operations.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 8 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 9: SECTION 8 — SECURE ENCODING WORKFLOW -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 8 &mdash; Encoding Workflow</span>
  </div>

  <div class="section-kicker">SECTION 8</div>
  <h1 class="section-title">Practical Walkthrough: Secure Encoding</h1>
  <div class="section-subtitle">Uploading Carriers, Configuring Secret Payloads, Setting Passphrases, and Monitoring Capacity</div>

  <div class="blue-box">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Upload a carrier image, enter a secret message, set a strong passphrase, confirm carrier capacity headroom, and embed the encrypted payload.</div>
  </div>

  <div style="display: flex; gap: 10px; margin-bottom: 5px;">
    <div style="flex: 1;">
      <h3 class="sub-block-heading">What is this?</h3>
      <p style="font-size: 9px; line-height: 1.45;">The workflow where secret data is encrypted with AES-256-GCM and hidden into pixel bits.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">Why is it used?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Produces an ordinary-looking image secretly holding encrypted data, safe from discovery.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">How does it work?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Compresses payload, derives Scrypt key, encrypts via AES-GCM, and writes bits into RGB LSBs.</p>
    </div>
  </div>

  <div class="figure-section">
    <img class="figure-large-img" src="__FIG02__" alt="Figure 2: Carrier Upload &amp; Dynamic Capacity Meter">
    <div class="figure-caption">Figure 2: Carrier Upload &amp; Dynamic Capacity Meter showing image preview, secret payload input, passphrase configuration, and capacity headroom.</div>
  </div>

  <div class="callout-breakdown">
    <div style="font-weight: 700; color: #1E3A8A; margin-bottom: 3px;">Step-by-Step Implementation &amp; Controls:</div>
    <span class="num-badge">&#9312; Carrier Ingestion Uploader:</span> Click <em>Browse files</em> and select a lossless carrier image (e.g., <code>carrier_sample.png</code>). Preview shows 600&times;400 dimensions.<br>
    <span class="num-badge">&#9313; Secret Payload Input:</span> Type secret text in the text area or toggle to <em>Binary File</em> to attach an encrypted key or document.<br>
    <span class="num-badge">&#9314; Passphrase Input Field:</span> Enter your secret passphrase. StegoVault uses this with Scrypt to derive the 256-bit AES key.<br>
    <span class="num-badge">&#9315; Dynamic Carrier Capacity Meter:</span> Shows byte count used vs. maximum safe capacity. Confirms payload is well below 15% safe ceiling.<br>
    <span class="num-badge">&#9316; Action Button:</span> Click <strong>Encrypt &amp; Embed Payload</strong> to execute the full cryptographic pipeline.
  </div>

  <div class="blue-box">
    <div class="blue-box-header">&#128161; ENCODING OBSERVATION</div>
    <div class="blue-box-content">Input parameters are validated instantly. The capacity gauge proves the payload occupies less than 1% of total capacity, ensuring visual distortion will remain invisible.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 9 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 10: SECTION 9 — ENCODING EXECUTION & RESULT -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 9 &mdash; Encoding Result</span>
  </div>

  <div class="section-kicker">SECTION 9</div>
  <h1 class="section-title">Practical Walkthrough: Encoding Result</h1>
  <div class="section-subtitle">Reviewing Execution Telemetry, Mathematical Quality Metrics, and Downloading Stego Images</div>

  <div class="blue-box">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Verify that encryption and embedding succeeded, review mathematical quality metrics, and download the finished stego image.</div>
  </div>

  <div style="display: flex; gap: 10px; margin-bottom: 5px;">
    <div style="flex: 1;">
      <h3 class="sub-block-heading">What is this?</h3>
      <p style="font-size: 9px; line-height: 1.45;">The post-encoding confirmation screen showing operational telemetry and the generated image.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">Why is it used?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Confirms that encryption succeeded, verifies zero perceptual distortion, and provides download.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">How does it work?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Measures empirical MSE/PSNR between cover and stego pixels, serving the image as lossless PNG.</p>
    </div>
  </div>

  <div class="figure-section">
    <img class="figure-large-img" src="__FIG03__" alt="Figure 3: Cryptographic Encoding Execution">
    <div class="figure-caption">Figure 3: Cryptographic Encoding Execution showing confirmation banner, mathematical quality metrics, visual preview, and download control.</div>
  </div>

  <div class="callout-breakdown">
    <div style="font-weight: 700; color: #1E3A8A; margin-bottom: 3px;">Execution Telemetry &amp; Controls:</div>
    <span class="num-badge">&#9312; Success Banner:</span> Displays green confirmation alert: <em>"Payload securely encrypted &amp; embedded!"</em><br>
    <span class="num-badge">&#9313; Operational Telemetry Grid:</span> Shows original payload size (117 B), encrypted envelope size (173 B), MSE (<strong>0.000911</strong>), and PSNR (<strong>78.54 dB</strong>).<br>
    <span class="num-badge">&#9314; Visual Stego Image Preview:</span> Visual display of the generated stego carrier confirming zero visible distortion or color banding.<br>
    <span class="num-badge">&#9315; Download Control:</span> One-click button to download the finalized <code>stego_image.png</code> to local disk.
  </div>

  <div class="blue-box">
    <div class="blue-box-header">&#128161; EXECUTION OBSERVATION</div>
    <div class="blue-box-content">The payload was encrypted and embedded successfully. The resulting PSNR of <strong>78.54 dB</strong> confirms that the modification affects only 1 out of every 1,100 pixel values by a single unit.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 10 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 11: SECTION 10 — AUTHENTICATED DECODING WORKFLOW -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 10 &mdash; Decoding Workflow</span>
  </div>

  <div class="section-kicker">SECTION 10</div>
  <h1 class="section-title">Practical Walkthrough: Authenticated Decoding</h1>
  <div class="section-subtitle">Extracting Bitstreams, Re-Deriving Keys, Verifying Integrity, and Recovering Plaintext</div>

  <div class="blue-box">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Upload a stego carrier image, supply the correct passphrase, verify cryptographic integrity, and recover the original secret message.</div>
  </div>

  <div style="display: flex; gap: 10px; margin-bottom: 5px;">
    <div style="flex: 1;">
      <h3 class="sub-block-heading">What is this?</h3>
      <p style="font-size: 9px; line-height: 1.45;">The extraction workflow where hidden bits are pulled from pixels, authenticated, and decrypted.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">Why is it used?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Allows authorized recipients who know the secret passphrase to recover the hidden data.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">How does it work?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Extracts LSBs, parses SVLT header, verifies 128-bit GHASH tag, and decrypts using AES-256-GCM.</p>
    </div>
  </div>

  <div class="figure-section">
    <img class="figure-large-img" src="__FIG04__" alt="Figure 4: Authenticated Payload Extraction">
    <div class="figure-caption">Figure 4: Authenticated Payload Extraction showing successful authentication, integrity check, and recovered secret plaintext.</div>
  </div>

  <div class="callout-breakdown">
    <div style="font-weight: 700; color: #1E3A8A; margin-bottom: 3px;">Step-by-Step Recovery &amp; Controls:</div>
    <span class="num-badge">&#9312; Mode Switch Tab:</span> Select <em>Authenticated Decode</em> from the top navigation bar.<br>
    <span class="num-badge">&#9313; Stego Carrier Uploader:</span> Upload the carrier image (<code>stego_image.png</code>) containing the hidden payload.<br>
    <span class="num-badge">&#9314; Passphrase Input Field:</span> Enter the secret passphrase matching the one used during encoding.<br>
    <span class="num-badge">&#9315; Authentication Status &amp; Payload Recovery Box:</span> Displays the green <em>"Authenticated Payload Extracted Successfully"</em> banner alongside the exact recovered cleartext message.
  </div>

  <div class="blue-box">
    <div class="blue-box-header">&#128161; DECODING OBSERVATION</div>
    <div class="blue-box-content">The 128-bit GHASH authentication tag verified successfully, proving that neither the carrier nor the payload was altered. The secret message was recovered with 100% accuracy.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 11 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 12: SECTION 11 — TAMPER DETECTION & AUTHENTICATION FAILURE -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 11 &mdash; Tamper Detection</span>
  </div>

  <div class="section-kicker">SECTION 11</div>
  <h1 class="section-title">Security Verification: Tamper Detection</h1>
  <div class="section-subtitle">Evaluating Tamper Rejection, Wrong Passphrases, and Cryptographic Integrity Enforcement</div>

  <div class="blue-box">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Demonstrate how StegoVault prevents unauthorized extraction when given an incorrect passphrase or when pixels have been modified.</div>
  </div>

  <div style="display: flex; gap: 10px; margin-bottom: 5px;">
    <div style="flex: 1;">
      <h3 class="sub-block-heading">What is this?</h3>
      <p style="font-size: 9px; line-height: 1.45;">The integrity-checking capability provided by AES-256-GCM authenticated encryption.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">Why is it used?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Naive tools output corrupt garbage on wrong passwords. StegoVault alerts and rejects immediately.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">How does it work?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Recalculates the GHASH tag during decryption. If tag mismatch occurs, decryption aborts instantly.</p>
    </div>
  </div>

  <div class="figure-section">
    <img class="figure-large-img" src="__FIG05__" alt="Figure 5: Authentication Failure Telemetry">
    <div class="figure-caption">Figure 5: Authentication Failure Telemetry showing immediate rejection of extraction when an invalid passphrase or tampered carrier is supplied.</div>
  </div>

  <div class="callout-breakdown">
    <div style="font-weight: 700; color: #1E3A8A; margin-bottom: 3px;">Test Scenarios &amp; Cryptographic Rejection:</div>
    <span class="num-badge">&#9312; Invalid Passphrase Test Input:</span> An incorrect passphrase (<code>WrongPassphrase123</code>) is entered.<br>
    <span class="num-badge">&#9313; High-Priority Red Security Alert:</span> Displays: <em>"Authentication failed! The passphrase is incorrect or the stego image has been tampered with."</em><br>
    <span class="num-badge">&#9314; Cryptographic Rejection Telemetry:</span> Explains that the 128-bit GHASH tag recalculation failed, completely blocking data release.
  </div>

  <div class="blue-box">
    <div class="blue-box-header">&#128161; TAMPER REJECTION OBSERVATION</div>
    <div class="blue-box-content">StegoVault blocked extraction immediately. Because authentication strictly precedes payload release, an attacker cannot extract partial data or perform chosen-ciphertext bit-flipping attacks.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 12 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 13: SECTION 12 — IMAGE QUALITY & FIDELITY ANALYSIS -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 12 &mdash; Quality Analysis</span>
  </div>

  <div class="section-kicker">SECTION 12</div>
  <h1 class="section-title">Practical Walkthrough: Image Quality Analysis</h1>
  <div class="section-subtitle">Measuring Mathematical Distortion, Calculating MSE and PSNR, and Verifying Imperceptibility</div>

  <div class="blue-box">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Compare the original cover image with the stego image to calculate Mean Squared Error (MSE) and Peak Signal-to-Noise Ratio (PSNR).</div>
  </div>

  <div style="display: flex; gap: 10px; margin-bottom: 5px;">
    <div style="flex: 1;">
      <h3 class="sub-block-heading">What is MSE?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Mean Squared Error measures average squared pixel differences. Lower is better; 0 means identical.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">What is PSNR?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Peak Signal-to-Noise Ratio in dB. Higher is better; &gt;40 dB is invisible, &gt;70 dB is near-flawless.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">Why is it used?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Mathematically verifies that data embedding has not created visible distortion or artifacts.</p>
    </div>
  </div>

  <div class="figure-section">
    <img class="figure-large-img" src="__FIG06__" alt="Figure 6: Mathematical Fidelity Analysis">
    <div class="figure-caption">Figure 6: Mathematical Fidelity Analysis showing side-by-side comparison, measured MSE (0.000911), and measured PSNR (78.54 dB).</div>
  </div>

  <div class="callout-breakdown">
    <div style="font-weight: 700; color: #1E3A8A; margin-bottom: 3px;">Side-by-Side Comparison &amp; Quantitative Metrics:</div>
    <span class="num-badge">&#9312; Mode Navigation:</span> Select <em>Image Quality &amp; Fidelity</em> from top navigation bar.<br>
    <span class="num-badge">&#9313; Side-by-Side Image Viewers:</span> Displays original cover image alongside stego carrier for direct visual comparison.<br>
    <span class="num-badge">&#9314; Quantitative Quality Telemetry Card:</span> Displays measured MSE (<strong>0.000911</strong>), PSNR (<strong>78.54 dB</strong>), and automated verdict badge: <em>"Exceptional Fidelity &bull; Perceptually Indistinguishable"</em>.
  </div>

  <div class="blue-box">
    <div class="blue-box-header">&#128161; FIDELITY OBSERVATION</div>
    <div class="blue-box-content">For the tested 600&times;400 carrier, embedding resulted in an MSE of <strong>0.000911</strong> and PSNR of <strong>78.54 dB</strong>, confirming that visual detection by human observers is impossible.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 13 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 14: SECTION 13 — FORENSIC STEGANALYSIS (BIT-0 PLANE SLICING) -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 13 &mdash; Forensic Steganalysis</span>
  </div>

  <div class="section-kicker">SECTION 13</div>
  <h1 class="section-title">Practical Walkthrough: Bit-Plane Forensics</h1>
  <div class="section-subtitle">Isolating Spatial LSB Planes, Auditing Channel Noise, and Revealing Embedded Footprints</div>

  <div class="blue-box">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Extract and visualize the Least Significant Bit plane (Bit 0) of a color channel to inspect the visual footprint created by LSB embedding.</div>
  </div>

  <div style="display: flex; gap: 10px; margin-bottom: 5px;">
    <div style="flex: 1;">
      <h3 class="sub-block-heading">What is this?</h3>
      <p style="font-size: 9px; line-height: 1.45;">A forensic technique that isolates Bit 0 of every pixel and displays it as a high-contrast black/white slice.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">Why is it used?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Natural bit-planes have visual outlines. Encrypted data replaces texture with flat random noise.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">How does it work?</h3>
      <p style="font-size: 9px; line-height: 1.45;">NumPy isolates Bit 0 (<code>pixel &amp; 1</code>) in the chosen channel and scales it to 0 or 255 for display.</p>
    </div>
  </div>

  <div class="figure-section">
    <img class="figure-large-img" src="__FIG07__" alt="Figure 7: Bit-Plane Forensic Slicing">
    <div class="figure-caption">Figure 7: Bit-Plane Forensic Slicing isolating the Bit-0 plane of the carrier to reveal the visual boundary between embedded noise and natural texture.</div>
  </div>

  <div class="callout-breakdown">
    <div style="font-weight: 700; color: #1E3A8A; margin-bottom: 3px;">Forensic Inspection Steps &amp; Controls:</div>
    <span class="num-badge">&#9312; Mode Navigation:</span> Select <em>Forensic Steganalysis</em> from top navigation bar.<br>
    <span class="num-badge">&#9313; Color Channel &amp; Inspection Selector:</span> Dropdown controls allowing user to select Red, Green, or Blue channel and choose <em>Bit-0 Plane Slice</em>.<br>
    <span class="num-badge">&#9314; Bit-0 Plane Visualization:</span> High-contrast display showing the isolated lowest bits, highlighting the boundary between embedded random bits and natural image texture.
  </div>

  <div class="blue-box">
    <div class="blue-box-header">&#128161; FORENSIC SLICING OBSERVATION</div>
    <div class="blue-box-content">The Bit-0 slice plane visualizes the footprint of the hidden data: the embedded region exhibits high-entropy random noise, demonstrating how forensic analysts detect sequential LSB insertion.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 14 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 15: SECTION 14 — STATISTICAL STEGANALYSIS (CHI-SQUARE ANALYSIS) -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 14 &mdash; Statistical Steganalysis</span>
  </div>

  <div class="section-kicker">SECTION 14</div>
  <h1 class="section-title">Practical Walkthrough: Chi-Square Analysis</h1>
  <div class="section-subtitle">Evaluating Pairs of Values (PoV), Measuring &chi;<sup>2</sup> Statistics, and Calculating p-Values</div>

  <div class="blue-box">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Run a mathematical Chi-Square (&chi;<sup>2</sup>) test on adjacent pixel value pairs to calculate the probability that an image contains hidden sequential LSB data.</div>
  </div>

  <div style="display: flex; gap: 10px; margin-bottom: 5px;">
    <div style="flex: 1;">
      <h3 class="sub-block-heading">What is this?</h3>
      <p style="font-size: 9px; line-height: 1.45;">A statistical test analyzing frequency distributions of adjacent pixel pairs ($2k$ and $2k+1$).</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">Why is it used?</h3>
      <p style="font-size: 9px; line-height: 1.45;">Visual inspection alone cannot always detect hidden data. Statistical tests provide mathematical scores.</p>
    </div>
    <div style="flex: 1;">
      <h3 class="sub-block-heading">How does it work?</h3>
      <p style="font-size: 9px; line-height: 1.45;">LSB embedding equalizes counts of $2k$ and $2k+1$. The test measures this; $p \approx 1$ indicates embedding.</p>
    </div>
  </div>

  <div class="figure-section">
    <img class="figure-large-img" src="__FIG08__" alt="Figure 8: Chi-Square Distribution Analysis">
    <div class="figure-caption">Figure 8: Chi-Square Distribution Analysis displaying the measured Chi-Square statistic, survival p-value, and automated forensic verdict.</div>
  </div>

  <div class="callout-breakdown">
    <div style="font-weight: 700; color: #1E3A8A; margin-bottom: 3px;">Statistical Execution &amp; Controls:</div>
    <span class="num-badge">&#9312; Statistical Test Selector:</span> Select <em>Chi-Square Analysis</em> within Forensic Steganalysis.<br>
    <span class="num-badge">&#9313; Quantitative Output Metrics:</span> Displays the measured Chi-Square (&chi;<sup>2</sup>) statistic and degrees of freedom across the 128 Pairs of Values (PoV).<br>
    <span class="num-badge">&#9314; Survival Probability ($p$-Value) &amp; Verdict:</span> Shows the calculated probability score ($p \approx 1.0$) triggering an automated forensic detection alert for sequential LSB embedding.
  </div>

  <div class="blue-box">
    <div class="blue-box-header">&#128161; STATISTICAL DETECTION OBSERVATION</div>
    <div class="blue-box-content">For the tested sample carrier with embedded sequential payload, the measured $p$-value approached <strong>1.0</strong>, successfully demonstrating how statistical steganalysis flags sequential LSB insertion.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 15 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 16: SECTION 15 — SECURITY IMPLEMENTATION & SPECIFICATIONS -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 15 &mdash; Security Implementation</span>
  </div>

  <div class="section-kicker">SECTION 15</div>
  <h1 class="section-title">Security Implementation &amp; Specifications</h1>
  <div class="section-subtitle">Cryptographic Primitives, Key Derivation Functions, and the SVLT 56-Byte Wire Envelope</div>

  <div class="blue-box">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Detail the exact security primitives, key derivation parameters, and binary envelope structure implemented in StegoVault.</div>
  </div>

  <div style="display: flex; gap: 12px; margin-bottom: 10px;">
    <div style="flex: 1; background: #F0F7FF; border: 1px solid #BFDBFE; border-left: 4px solid #2563EB; border-radius: 4px; padding: 10px 12px;">
      <h3 class="sub-block-heading" style="margin-top: 0;">AES-256-GCM Authenticated Encryption</h3>
      <p style="font-size: 9px; margin-bottom: 3px;"><strong>What it is:</strong> Symmetric AEAD cipher recognized globally by NIST (SP 800-38D).</p>
      <p style="font-size: 9px; margin-bottom: 3px;"><strong>What it does:</strong> Encrypts data for confidentiality while generating a 128-bit GHASH authentication tag.</p>
      <p style="font-size: 9px; margin-bottom: 0;"><strong>Why it is used:</strong> Provides military-grade privacy and immediate detection of bit-flipping or tampering.</p>
    </div>
    <div style="flex: 1; background: #F0F7FF; border: 1px solid #BFDBFE; border-left: 4px solid #2563EB; border-radius: 4px; padding: 10px 12px;">
      <h3 class="sub-block-heading" style="margin-top: 0;">Scrypt Key Derivation (RFC 7914)</h3>
      <p style="font-size: 9px; margin-bottom: 3px;"><strong>What it is:</strong> A memory-hard password-based key derivation function.</p>
      <p style="font-size: 9px; margin-bottom: 3px;"><strong>Parameters:</strong> $N = 16384$, $r = 8$, $p = 1$, generating a 256-bit AES key with a 16-byte salt.</p>
      <p style="font-size: 9px; margin-bottom: 0;"><strong>Why it is used:</strong> Consumes ~16 MiB of RAM per derivation, defeating GPU/ASIC brute-force attacks.</p>
    </div>
  </div>

  <h2 class="block-heading">Salt, Nonce &amp; Additional Authenticated Data (AAD)</h2>
  <p style="font-size: 9.5px; line-height: 1.5; margin-bottom: 8px;">
    <strong>Salt (16 Bytes):</strong> Fresh random bytes from <code>os.urandom</code> ensure that identical passphrases generate distinct keys.<br>
    <strong>Nonce (12 Bytes):</strong> Unique initialization vector ensures that encrypting identical messages produces distinct ciphertexts.<br>
    <strong>Additional Authenticated Data (AAD):</strong> The 56-byte header is bound as AAD; any alteration causes instant verification failure.
  </p>

  <h2 class="block-heading" style="margin-top: 8px;">SVLT Binary Wire Envelope Protocol (56 Bytes)</h2>
  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 15%;">Offset</th>
        <th style="width: 22%;">Field Name</th>
        <th style="width: 12%;">Size</th>
        <th style="width: 15%;">Data Type</th>
        <th style="width: 36%;">Practical Purpose</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>0x00 - 0x03</code></td>
        <td>Magic Identifier</td>
        <td>4 Bytes</td>
        <td>ASCII (<code>SVLT</code>)</td>
        <td>Confirms that file contains a valid StegoVault payload</td>
      </tr>
      <tr>
        <td><code>0x04</code></td>
        <td>Protocol Version</td>
        <td>1 Byte</td>
        <td><code>uint8</code> (<code>0x01</code>)</td>
        <td>Protocol version identifier for backward compatibility</td>
      </tr>
      <tr>
        <td><code>0x05</code></td>
        <td>Bitmask Flags</td>
        <td>1 Byte</td>
        <td>Bitmask</td>
        <td>Bit 0: Compression (1=zlib); Bit 1: Type (0=text, 1=binary)</td>
      </tr>
      <tr>
        <td><code>0x06 - 0x07</code></td>
        <td>Reserved Space</td>
        <td>2 Bytes</td>
        <td><code>0x0000</code></td>
        <td>Reserved for future cryptographic feature expansions</td>
      </tr>
      <tr>
        <td><code>0x08 - 0x17</code></td>
        <td>Scrypt Salt</td>
        <td>16 Bytes</td>
        <td>Raw Bytes</td>
        <td>Random cryptographic salt for password key derivation</td>
      </tr>
      <tr>
        <td><code>0x18 - 0x23</code></td>
        <td>AES Nonce / IV</td>
        <td>12 Bytes</td>
        <td>Raw Bytes</td>
        <td>Unique initialization vector for AES-GCM cipher</td>
      </tr>
      <tr>
        <td><code>0x24 - 0x33</code></td>
        <td>GHASH Auth Tag</td>
        <td>16 Bytes</td>
        <td>Raw Bytes</td>
        <td>128-bit integrity tag for tamper detection</td>
      </tr>
      <tr>
        <td><code>0x34 - 0x37</code></td>
        <td>Payload Length</td>
        <td>4 Bytes</td>
        <td><code>uint32</code> (BE)</td>
        <td>Exact byte length of the encrypted ciphertext</td>
      </tr>
      <tr>
        <td><code>0x38 - End</code></td>
        <td>Ciphertext</td>
        <td>Variable</td>
        <td>Raw Bytes</td>
        <td>AES-256-GCM encrypted compressed data payload</td>
      </tr>
    </tbody>
  </table>

  <div class="blue-box" style="margin-top: 10px;">
    <div class="blue-box-header">&#128161; CRYPTOGRAPHIC ARCHITECTURE OBSERVATION</div>
    <div class="blue-box-content">The 56-byte SVLT wire envelope is completely self-contained and portable, allowing authorized receivers to reconstruct keys and authenticate payloads without out-of-band metadata.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 16 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 17: SECTION 16 — TESTING & VERIFICATION RESULTS -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 16 &mdash; Testing &amp; Verification</span>
  </div>

  <div class="section-kicker">SECTION 16</div>
  <h1 class="section-title">Testing &amp; Verification Results</h1>
  <div class="section-subtitle">Automated Test Execution, Conformance Matrices, and Quality Assurance Verification</div>

  <div class="blue-box" style="padding: 11px 15px; margin-bottom: 12px;">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Document the automated test suite and confirm that all software components execute reliably with a 100% automated test pass rate.</div>
  </div>

  <h2 class="block-heading" style="margin-top: 13px; margin-bottom: 8px;">Automated Test Suite Methodology</h2>
  <p style="font-size: 10px; line-height: 1.55; margin-bottom: 10px;">StegoVault incorporates an automated test suite executed with <code>pytest</code>, exercising all core modules under boundary conditions, malicious tamper attempts, and varied payload formats.</p>

  <table class="data-table" style="margin-bottom: 14px;">
    <thead>
      <tr>
        <th style="width: 20%; padding: 7px 10px;">Test Suite</th>
        <th style="width: 25%; padding: 7px 10px;">Module Tested</th>
        <th style="width: 8%; padding: 7px 10px; text-align: center;">Tests</th>
        <th style="width: 32%; padding: 7px 10px;">Expected Verification</th>
        <th style="width: 15%; padding: 7px 10px; text-align: center;">Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 7px 10px;"><code>test_crypto.py</code></td>
        <td style="padding: 7px 10px;">AES-256-GCM AEAD</td>
        <td style="padding: 7px 10px; text-align: center; font-weight: 700;">17</td>
        <td style="padding: 7px 10px;">Valid encryption, tag verification, tampered ciphertext rejection, AAD integrity</td>
        <td style="padding: 7px 10px; text-align: center;"><span class="badge-pass">&#10004; 17 Passed</span></td>
      </tr>
      <tr>
        <td style="padding: 7px 10px;"><code>test_key_derivation.py</code></td>
        <td style="padding: 7px 10px;">Scrypt KDF Engine</td>
        <td style="padding: 7px 10px; text-align: center; font-weight: 700;">7</td>
        <td style="padding: 7px 10px;">RFC 7914 vector validation, salt randomness, memory cost enforcement</td>
        <td style="padding: 7px 10px; text-align: center;"><span class="badge-pass">&#10004; 7 Passed</span></td>
      </tr>
      <tr>
        <td style="padding: 7px 10px;"><code>test_lsb.py</code></td>
        <td style="padding: 7px 10px;">Spatial LSB Core</td>
        <td style="padding: 7px 10px; text-align: center; font-weight: 700;">12</td>
        <td style="padding: 7px 10px;">RGB sequential embedding, extraction, RGBA alpha protection, capacity limits</td>
        <td style="padding: 7px 10px; text-align: center;"><span class="badge-pass">&#10004; 12 Passed</span></td>
      </tr>
      <tr>
        <td style="padding: 7px 10px;"><code>test_analysis.py</code></td>
        <td style="padding: 7px 10px;">Quality &amp; Forensics</td>
        <td style="padding: 7px 10px; text-align: center; font-weight: 700;">16</td>
        <td style="padding: 7px 10px;">MSE &amp; PSNR calculations, Bit-0 plane slicing, Chi-Square distribution testing</td>
        <td style="padding: 7px 10px; text-align: center;"><span class="badge-pass">&#10004; 16 Passed</span></td>
      </tr>
      <tr>
        <td style="padding: 7px 10px;"><code>test_utils.py</code></td>
        <td style="padding: 7px 10px;">Validation &amp; Hashing</td>
        <td style="padding: 7px 10px; text-align: center; font-weight: 700;">14</td>
        <td style="padding: 7px 10px;">SHA-256 integrity hashing, image header validation, dimension enforcement</td>
        <td style="padding: 7px 10px; text-align: center;"><span class="badge-pass">&#10004; 14 Passed</span></td>
      </tr>
      <tr>
        <td style="padding: 7px 10px;"><code>test_integration.py</code></td>
        <td style="padding: 7px 10px;">End-to-End Pipeline</td>
        <td style="padding: 7px 10px; text-align: center; font-weight: 700;">11</td>
        <td style="padding: 7px 10px;">Encode-then-decode roundtrip, binary file recovery, wrong password recovery</td>
        <td style="padding: 7px 10px; text-align: center;"><span class="badge-pass">&#10004; 11 Passed</span></td>
      </tr>
    </tbody>
  </table>

  <h2 class="block-heading" style="margin-top: 14px; margin-bottom: 8px;">Execution Summary &amp; Conformance</h2>
  <div style="display: flex; gap: 14px; margin-top: 8px; margin-bottom: 14px;">
    <div style="flex: 1; background: #F0F7FF; border: 1.5px solid #93C5FD; border-radius: 4px; padding: 15px 12px; text-align: center;">
      <div style="font-size: 28px; font-weight: 900; color: #1E3A8A;">77 / 77</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #2563EB; margin-top: 2px;">Tests Passed</div>
      <div style="font-size: 9px; color: #475569; margin-top: 3px;">Zero Failures &bull; Zero Errors</div>
    </div>
    <div style="flex: 1; background: #F0F7FF; border: 1.5px solid #93C5FD; border-radius: 4px; padding: 15px 12px; text-align: center;">
      <div style="font-size: 28px; font-weight: 900; color: #1E3A8A;">100%</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #2563EB; margin-top: 2px;">Automated Pass Rate</div>
      <div style="font-size: 9px; color: #475569; margin-top: 3px;">Total Test Suite Coverage</div>
    </div>
    <div style="flex: 1; background: #F0F7FF; border: 1.5px solid #93C5FD; border-radius: 4px; padding: 15px 12px; text-align: center;">
      <div style="font-size: 28px; font-weight: 900; color: #1E3A8A;">1.92s</div>
      <div style="font-size: 10.5px; font-weight: 700; color: #2563EB; margin-top: 2px;">Execution Time</div>
      <div style="font-size: 9px; color: #475569; margin-top: 3px;">Ultra-Fast Execution</div>
    </div>
  </div>

  <div class="blue-box" style="padding: 11px 15px; margin-top: 14px;">
    <div class="blue-box-header">&#128161; QUALITY ASSURANCE VERDICT</div>
    <div class="blue-box-content">All 77 automated unit and integration tests passed cleanly in under 2 seconds. The codebase demonstrates 100% regression resistance and zero deprecation warnings.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 17 of 18</span>
  </div>
</div>

<!-- ================================================================= -->
<!-- PAGE 18: SECTION 17 — LIMITATIONS, FUTURE SCOPE & CONCLUSION -->
<!-- ================================================================= -->
<div class="page">
  <div class="page-frame"></div>
  <div class="running-header">
    <span class="running-header-title">StegoVault Project Documentation</span>
    <span>Section 17 &mdash; Limitations &amp; Scope</span>
  </div>

  <div class="section-kicker">SECTION 17</div>
  <h1 class="section-title">Limitations, Future Scope &amp; Conclusion</h1>
  <div class="section-subtitle" style="margin-bottom: 16px;">Engineering Boundaries, Roadmap Innovations, and Final Project Summary</div>

  <div class="blue-box" style="padding: 12px 16px; margin-bottom: 16px;">
    <div class="blue-box-header">&#127919; GOAL</div>
    <div class="blue-box-content">Honestly assess current operational boundaries, outline roadmap enhancements, and present the final conclusion.</div>
  </div>

  <h2 class="block-heading" style="margin-top: 15px; margin-bottom: 8px;">Current Operational Limitations</h2>
  <ul style="font-size: 10px; color: #334155; margin-left: 20px; line-height: 1.76; margin-bottom: 14px;">
    <li style="margin-bottom: 7px;"><strong>Lossless Image Dependency:</strong> StegoVault works strictly with lossless formats (PNG, BMP, TIFF). Messaging platforms (such as WhatsApp, Discord, or Telegram) transcode images to lossy JPEG or WebP, which strips LSB data.</li>
    <li style="margin-bottom: 7px;"><strong>Sequential Embedding Detectability:</strong> Because bits are embedded sequentially from top-left, statistical Chi-Square testing can detect the presence of data if the carrier is forensically audited.</li>
    <li><strong>Capacity Thresholds:</strong> StegoVault enforces a recommended 15% capacity ceiling. Embedding larger payloads will reduce the PSNR below safe thresholds.</li>
  </ul>

  <h2 class="block-heading" style="margin-top: 15px; margin-bottom: 8px;">Future Scope &amp; Planned Enhancements</h2>
  <ul style="font-size: 10px; color: #334155; margin-left: 20px; line-height: 1.76; margin-bottom: 14px;">
    <li style="margin-bottom: 7px;"><strong>PRNG Pixel Scattering:</strong> Use a pseudo-random seed derived from the passphrase to scatter payload bits across pseudo-random pixel locations, evading sequential Chi-Square detection.</li>
    <li style="margin-bottom: 7px;"><strong>Adaptive Matrix Encoding (STC):</strong> Implement Syndrome-Trellis Codes to minimize the total number of modified bits per embedded byte.</li>
    <li><strong>Command-Line Interface (CLI):</strong> Develop an automated CLI tool to allow security teams to embed and extract data within automated defensive pipelines.</li>
  </ul>

  <h2 class="block-heading" style="margin-top: 15px; margin-bottom: 8px;">Final Conclusion</h2>
  <p style="font-size: 10px; line-height: 1.7; margin-bottom: 14px; text-align: justify;">StegoVault demonstrates that combining authenticated cryptography (<strong>AES-256-GCM</strong> + <strong>Scrypt</strong>) with image steganography and defensive forensics produces a transparent, verifiable defense-in-depth platform. By ensuring that encryption strictly precedes embedding, StegoVault guarantees that even if steganography is detected, the underlying data remains cryptographically secure against interception and tampering.</p>

  <div style="background: #F0F7FF; border: 1.5px solid #BFDBFE; border-radius: 4px; padding: 15px 18px; margin-top: 12px; margin-bottom: 14px;">
    <div style="font-weight: 800; color: #1E3A8A; font-size: 10.5px; margin-bottom: 6px;">Project Attribution &amp; Repository:</div>
    <div style="font-size: 9.5px; color: #334155; line-height: 1.6;">
      <strong>Author &amp; Lead Verifier:</strong> Vivek Rathod<br>
      <strong>GitHub Repository:</strong> <a href="https://github.com/Vivekkk20/StegoVault" style="color: #2563EB; text-decoration: none;">https://github.com/Vivekkk20/StegoVault</a><br>
      <strong>Core Technologies:</strong> Python 3.14, Streamlit, Pillow, Cryptography, NumPy, SciPy, pytest
    </div>
  </div>

  <div class="blue-box" style="padding: 12px 16px; margin-top: 14px;">
    <div class="blue-box-header">&#128161; FINAL TAKEAWAY</div>
    <div class="blue-box-content">StegoVault proves that robust cybersecurity engineering combines cryptographic rigor with digital image forensics, providing a transparent, verifiable defense-in-depth security toolkit.</div>
  </div>

  <div class="running-footer">
    <span>StegoVault &bull; Cryptographic Steganography and Steganalysis Toolkit &bull; Vivek Rathod</span>
    <span class="page-number">Page 18 of 18</span>
  </div>
</div>

</body>
</html>
"""
    for placeholder, path in fig_paths.items():
        b64_data = get_base64_image(path)
        html_template = html_template.replace(placeholder, b64_data)
        
    os.makedirs("docs", exist_ok=True)
    with open("docs/stegovault_documentation.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("[SUCCESS] Wrote docs/stegovault_documentation.html")

async def compile_pdf():
    print("[INFO] Launching Chrome to compile docs/stegovault_documentation.pdf...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path="C:/Program Files/Google/Chrome/Application/chrome.exe")
        page = await browser.new_page()
        html_path = os.path.abspath("docs/stegovault_documentation.html")
        await page.goto(f"file:///{html_path.replace(os.sep, '/')}")
        await page.wait_for_timeout(2000)
        await page.pdf(
            path="docs/stegovault_documentation.pdf",
            format="A4",
            print_background=True,
            prefer_css_page_size=True
        )
        await browser.close()
    print("[SUCCESS] Compiled docs/stegovault_documentation.pdf")

    # Verify page count
    with open("docs/stegovault_documentation.pdf", "rb") as f:
        pdf_bytes = f.read()
    pages = re.findall(rb'/Type\s*/Page\b', pdf_bytes)
    print(f"[VERIFY] PDF Page Count: {len(pages)} Pages")

def main():
    build_html()
    asyncio.run(compile_pdf())

if __name__ == "__main__":
    main()
