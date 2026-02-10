#!/usr/bin/env python3
import os
import sys
from urllib.parse import parse_qs
from datetime import datetime

# -----------------------------
# Helpers
# -----------------------------
def parse_cookie_header(cookie_header: str) -> dict:
    cookies = {}
    if not cookie_header:
        return cookies

    parts = cookie_header.split(";")
    for p in parts:
        p = p.strip()
        if "=" in p:
            k, v = p.split("=", 1)
            cookies[k.strip()] = v.strip()
    return cookies


def html_escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


# -----------------------------
# Read request data (GET/POST)
# -----------------------------
method = os.environ.get("REQUEST_METHOD", "GET").upper()

raw = ""
if method == "GET":
    raw = os.environ.get("QUERY_STRING", "")
elif method == "POST":
    try:
        length = int(os.environ.get("CONTENT_LENGTH", "0"))
    except ValueError:
        length = 0
    raw = sys.stdin.read(length)

form = parse_qs(raw)

def get_value(key):
    return form.get(key, [None])[0]


# -----------------------------
# Cookie: last_access
# -----------------------------
cookie_header = os.environ.get("HTTP_COOKIE", "")
cookies = parse_cookie_header(cookie_header)

previous_access = cookies.get("last_access")

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# -----------------------------
# Read calculator fields
# -----------------------------
num1_raw = get_value("num1")
num2_raw = get_value("num2")
op = get_value("op")  # add/sub/mul/div

result = None
error = None
op_label = None

try:
    if num1_raw is None or num2_raw is None or op is None:
        error = "Missing input. Please fill in both numbers and select an operation."
    else:
        a = float(num1_raw)
        b = float(num2_raw)

        if op == "add":
            result = a + b
            op_label = "+"
        elif op == "sub":
            result = a - b
            op_label = "−"
        elif op == "mul":
            result = a * b
            op_label = "×"
        elif op == "div":
            op_label = "÷"
            if b == 0:
                error = "Division by zero is not allowed."
            else:
                result = a / b
        else:
            error = "Invalid operation."
except ValueError:
    error = "Invalid number format. Please enter valid numbers."


# -----------------------------
# Output headers (IMPORTANT)
# -----------------------------
print("Content-type: text/html")
print(f"Set-Cookie: last_access={now}; Path=/; SameSite=Lax")
print("")  # end headers


# -----------------------------
# Output HTML (Tailwind)
# -----------------------------
print(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Calculator — Result</title>

    <!-- Tailwind CSS (CDN, plain HTML) -->
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  </head>

  <body class="bg-neutral-950 text-neutral-100 antialiased">
    <div class="min-h-screen flex flex-col">
      <!-- Header -->
      <header class="border-b border-neutral-800">
        <div class="max-w-5xl mx-auto px-6 h-20 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div>
              <p class="font-semibold text-xl tracking-tight leading-none">
                Calculator
              </p>
              <p class="text-xs text-neutral-500 mt-1">
                CGI Version · Cookies for Last Access
              </p>
            </div>
          </div>

          <span class="text-sm text-neutral-400 hidden sm:block">
            CSI 3540 · Devoir 2
          </span>
        </div>
      </header>

      <!-- Main -->
      <main class="flex-1 flex items-center justify-center px-6 py-10">
        <section class="w-full max-w-xl">
          <div
            class="rounded-3xl border border-neutral-800 bg-neutral-900/40 shadow-2xl shadow-black/40 overflow-hidden"
          >
            <!-- Top -->
            <div class="p-6 border-b border-neutral-800">
              <div class="rounded-2xl bg-neutral-950 border border-neutral-800 px-5 py-5">
                <p class="text-xs text-neutral-500 tracking-wide">
                  Calculation Result
                </p>

                <div class="mt-4 flex items-end justify-between gap-6">
                  <div>
                    <p class="text-xs text-neutral-500">Expression</p>
                    <p class="mt-1 text-lg text-neutral-300">
                      {html_escape(num1_raw or "—")} <span class="text-neutral-500">{html_escape(op_label or " ")}</span> {html_escape(num2_raw or "—")}
                    </p>
                  </div>

                  <div class="text-right">
                    <p class="text-xs text-neutral-500">Result</p>
                    <p class="mt-1 text-3xl sm:text-4xl font-semibold tracking-tight text-neutral-100">
                      {"—" if result is None else html_escape(str(result))}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Body -->
            <div class="p-6 space-y-4">
""")

# Cookie info
if previous_access:
    print(f"""
              <div class="rounded-2xl border border-neutral-800 bg-neutral-950 px-4 py-4">
                <p class="text-sm text-neutral-300">
                  <span class="text-neutral-500">Last access (cookie):</span>
                  <b class="text-neutral-200">{html_escape(previous_access)}</b>
                </p>
              </div>
""")
else:
    print("""
              <div class="rounded-2xl border border-neutral-800 bg-neutral-950 px-4 py-4">
                <p class="text-sm text-neutral-300">
                  <span class="text-neutral-500">Last access (cookie):</span>
                  <b class="text-neutral-200">None (first visit)</b>
                </p>
              </div>
""")

print(f"""
              <div class="rounded-2xl border border-neutral-800 bg-neutral-950 px-4 py-4">
                <p class="text-sm text-neutral-300">
                  <span class="text-neutral-500">Current access:</span>
                  <b class="text-neutral-200">{html_escape(now)}</b>
                </p>
              </div>
""")

# Error block
if error:
    print(f"""
              <div class="rounded-2xl border border-red-500/30 bg-red-500/10 px-4 py-4">
                <p class="text-sm text-red-200">
                  <b>Error:</b> {html_escape(error)}
                </p>
              </div>
""")

# Back button
print("""
              <div class="pt-2 flex items-center justify-center">
                <a
                  href="/index.html"
                  class="inline-flex items-center justify-center rounded-2xl border border-neutral-800 bg-neutral-950 px-4 py-3 text-sm text-neutral-200 hover:bg-neutral-900 transition"
                >
                  ← Back to calculator
                </a>
              </div>
            </div>
          </div>

          <p class="mt-6 text-center text-xs text-neutral-600">
            Refresh after calculating to see the <span class="text-neutral-400">last_access</span> cookie update.
          </p>
        </section>
      </main>

      <!-- Footer -->
      <footer class="border-t border-neutral-800">
        <div class="max-w-5xl mx-auto px-6 py-6 text-sm text-neutral-500 flex items-center justify-between">
          <span>© 2026 — CSI3540A · Calculatrice</span>

          <span class="hidden sm:inline">
            Contact:
            <a href="mailto:aditya@adityabaindur.dev" class="hover:underline ml-1 text-neutral-300">
              aditya@adityabaindur.dev
            </a>
          </span>
        </div>
      </footer>
    </div>
  </body>
</html>
""")
