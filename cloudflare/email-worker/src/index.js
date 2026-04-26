const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function json(data, status = 200, origin = "*") {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "access-control-allow-origin": origin,
      "access-control-allow-methods": "POST, OPTIONS",
      "access-control-allow-headers": "content-type",
    },
  });
}

function allowedOrigin(request, env) {
  const origin = request.headers.get("origin");
  const allowed = (env.ALLOWED_ORIGINS || "")
    .split(",")
    .map((value) => value.trim())
    .filter(Boolean);
  if (!origin) return "*";
  return allowed.includes(origin) ? origin : "null";
}

async function parseEmail(request) {
  const contentType = request.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    const body = await request.json();
    return (body?.email || "").trim().toLowerCase();
  }
  if (contentType.includes("application/x-www-form-urlencoded")) {
    const form = await request.formData();
    return String(form.get("email") || "").trim().toLowerCase();
  }
  return "";
}

async function forwardToBeehiiv(email, env) {
  if (!env.BEEHIIV_SUBSCRIBE_URL) return;
  const payload = {
    email,
    reactivate_existing: true,
    send_welcome_email: true,
    utm_source: "avinoxlist",
  };

  const response = await fetch(env.BEEHIIV_SUBSCRIBE_URL, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      ...(env.BEEHIIV_API_KEY ? { authorization: `Bearer ${env.BEEHIIV_API_KEY}` } : {}),
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`Beehiiv API error (${response.status}): ${text.slice(0, 200)}`);
  }
}

export default {
  async fetch(request, env) {
    const origin = allowedOrigin(request, env);
    const { pathname } = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "access-control-allow-origin": origin,
          "access-control-allow-methods": "POST, OPTIONS",
          "access-control-allow-headers": "content-type",
        },
      });
    }
    if (pathname !== "/subscribe") return json({ error: "Not found" }, 404, origin);
    if (request.method !== "POST") return json({ error: "Method not allowed" }, 405, origin);

    const email = await parseEmail(request);
    if (!EMAIL_REGEX.test(email)) return json({ error: "Invalid email" }, 400, origin);

    try {
      if (env.EMAILS_DB) {
        await env.EMAILS_DB.prepare(
          "INSERT INTO subscribers (email, source, created_at) VALUES (?1, ?2, ?3) ON CONFLICT(email) DO NOTHING"
        )
          .bind(email, "avinoxlist", new Date().toISOString())
          .run();
      }

      await forwardToBeehiiv(email, env);
      return json({ ok: true }, 200, origin);
    } catch (error) {
      return json({ error: "Subscription failed" }, 502, origin);
    }
  },
};
