package ca.uottawa.csi3540;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Locale;

@WebServlet(name = "CalculatriceServlet", urlPatterns = {"/calculatrice"})
public class CalculatriceServlet extends HttpServlet {

    private static final String SESSION_LAST_ACCESS = "last_access";

    private static final DateTimeFormatter DISPLAY_FMT =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
                    .withLocale(Locale.CANADA_FRENCH)
                    .withZone(ZoneId.systemDefault());

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        process(req, resp);
    }

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        process(req, resp);
    }

    private void process(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        req.setCharacterEncoding(StandardCharsets.UTF_8.name());
        resp.setCharacterEncoding(StandardCharsets.UTF_8.name());
        resp.setContentType("text/html; charset=UTF-8");

        HttpSession session = req.getSession(true);

        // Read previous last access (server-side session)
        String previousAccess = (String) session.getAttribute(SESSION_LAST_ACCESS);

        // Update session with current access time
        String now = DISPLAY_FMT.format(Instant.now());
        session.setAttribute(SESSION_LAST_ACCESS, now);

        String aRaw = req.getParameter("a");
        String bRaw = req.getParameter("b");
        String op = req.getParameter("op");

        String error = null;
        Double a = null, b = null, result = null;
        String symbol = "?";

        try {
            if (aRaw == null || bRaw == null || op == null) {
                throw new IllegalArgumentException("Paramètres manquants.");
            }

            a = Double.parseDouble(aRaw.trim());
            b = Double.parseDouble(bRaw.trim());

            switch (op) {
                case "add" -> { result = a + b; symbol = "+"; }
                case "sub" -> { result = a - b; symbol = "−"; }
                case "mul" -> { result = a * b; symbol = "×"; }
                case "div" -> {
                    symbol = "÷";
                    if (b == 0.0) {
                        throw new ArithmeticException("Division par zéro.");
                    }
                    result = a / b;
                }
                default -> throw new IllegalArgumentException("Opération invalide.");
            }
        } catch (NumberFormatException e) {
            error = "Entrée invalide : veuillez entrer des nombres valides (ex: 12.5).";
        } catch (ArithmeticException e) {
            error = e.getMessage();
        } catch (Exception e) {
            error = "Erreur : " + e.getMessage();
        }

        try (PrintWriter out = resp.getWriter()) {
            out.println("""
                <!doctype html>
                <html lang="fr">
                  <head>
                    <meta charset="UTF-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <title>Résultat — Calculatrice Servlet</title>
                    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
                  </head>
                  <body class="bg-neutral-950 text-neutral-100 antialiased">
                    <div class="min-h-screen flex flex-col">
                      <header class="border-b border-neutral-800">
                        <div class="max-w-4xl mx-auto px-6 h-20 flex items-center justify-between">
                          <div class="flex items-center gap-3">
                            <div>
                              <p class="font-semibold text-lg leading-none">Résultat (Servlet)</p>
                              <p class="text-xs text-neutral-400">HttpSession — état côté serveur</p>
                            </div>
                          </div>
                          <a href="index.html" class="text-sm text-neutral-300 hover:underline">Retour</a>
                        </div>
                      </header>

                      <main class="flex-1">
                        <div class="max-w-4xl mx-auto px-6 py-10">
                          <div class="rounded-3xl border border-neutral-800 bg-neutral-900/30 p-6 shadow-sm">
                """);

            if (error != null) {
                out.println("""
                    <div class="rounded-2xl border border-red-900/60 bg-red-950/40 p-4">
                      <p class="font-semibold text-red-200">Erreur</p>
                      <p class="text-sm text-red-200/80 mt-1">%s</p>
                    </div>
                """.formatted(escapeHtml(error)));
            } else {
                out.println("""
                    <div class="rounded-2xl border border-neutral-800 bg-neutral-950/40 p-4">
                      <p class="text-sm text-neutral-400">Calcul</p>
                      <p class="text-2xl font-semibold mt-1">%s %s %s = <span class="text-neutral-50">%s</span></p>
                    </div>
                """.formatted(
                        escapeHtml(formatNumber(a)),
                        escapeHtml(symbol),
                        escapeHtml(formatNumber(b)),
                        escapeHtml(formatNumber(result))
                ));
            }

            out.println("""
                    <div class="mt-6 grid gap-3 sm:grid-cols-2">
                      <div class="rounded-2xl border border-neutral-800 bg-neutral-950/40 p-4">
                        <p class="text-sm text-neutral-400">Dernier accès (précédent)</p>
                        <p class="mt-1">%s</p>
                      </div>
                      <div class="rounded-2xl border border-neutral-800 bg-neutral-950/40 p-4">
                        <p class="text-sm text-neutral-400">Accès actuel (stocké en session)</p>
                        <p class="mt-1">%s</p>
                      </div>
                    </div>

                    <div class="mt-6 flex gap-3 justify-center items-center">
                      <a href="index.html"
                         class="rounded-2xl border border-neutral-800 bg-neutral-100 px-5 py-3 text-sm font-semibold text-neutral-950 hover:bg-white transition">
                        Nouveau calcul
                      </a>
                    </div>
                """.formatted(
                    previousAccess == null ? "<span class='text-neutral-500'>(Aucun — première visite)</span>" : escapeHtml(previousAccess),
                    escapeHtml(now),
                    escapeHtml(aRaw == null ? "" : aRaw),
                    escapeHtml(op == null ? "" : op),
                    escapeHtml(bRaw == null ? "" : bRaw)
            ));

            out.println("""
                          </div>
                        </div>
                      </main>

                      <footer class="border-t border-neutral-800">
                        <div class="max-w-4xl mx-auto px-6 py-6 text-sm text-neutral-500">
                          © 2026 — CSI3540A · Calculatrice Servlet
                        </div>
                      </footer>
                    </div>
                  </body>
                </html>
                """);
        }
    }

    private static String escapeHtml(String s) {
        if (s == null) return "";
        return s.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\"", "&quot;")
                .replace("'", "&#39;");
    }

    private static String formatNumber(Double x) {
        if (x == null) return "";
        // Cleaner display: 2.0 -> "2"
        if (Math.abs(x - Math.rint(x)) < 1e-10) return Long.toString(Math.round(x));
        return x.toString();
    }
}
