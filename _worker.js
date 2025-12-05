const BOT_TOKEN = ENV_BOT_TOKEN;
const BOT_SECRET = ENV_BOT_SECRET;
const CHANNEL = "@alibodama";
const DOMAIN = "configforge-v2ray.pages.dev";

function uuid() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}

async function send(c, t, k = null) {
  await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({chat_id: c, text: t, parse_mode: "MarkdownV2", disable_web_page_preview: true, reply_markup: k})
  });
}

async function member(id) {
  try {
    const r = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/getChatMember?chat_id=${CHANNEL}&user_id=${id}`);
    const j = await r.json();
    return ["member","administrator","creator"].includes(j.result.status);
  } catch { return false }
}

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === "/register") {
      const r = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/setWebhook?url=https://${DOMAIN}/webhook&secret_token=${BOT_SECRET}`);
      return new Response(await r.text(), {headers: {"Content-Type":"application/json"}});
    }

    if (url.pathname === "/webhook" && request.method === "POST") {
      if (request.headers.get("X-Telegram-Bot-Api-Secret-Token") !== BOT_SECRET) return new Response("No");

      const u = await request.json();
      const msg = u.message || u.callback_query?.message;
      if (!msg) return new Response("OK");
      const userId = (u.message?.from || u.callback_query?.from).id;
      const chatId = msg.chat.id;
      const text = u.message?.text;
      const data = u.callback_query?.data;

      if (text === "/start") {
        await send(chatId, `*به Alibodama خوش اومدی!*

کانفیگ تست ۲۴ ساعته رایگان داری
بعد از عضویت در کانال → کانفیگ ۳۰ روزه نامحدود

youtube.com/@alibodama | t.me/alibodama`, {
          inline_keyboard: [[
            {text: "کانفیگ ۲۴ ساعته رایگان", callback_data: "test"},
            {text: "کانفیگ ۳۰ روزه (عضو شو)", callback_data: "premium"}
          ], [{text: "کانال Alibodama", url: "https://t.me/alibodama"}]]
        });
      }

      if (data === "test") {
        const cfg = `vless://${uuid()}@${DOMAIN}:443?encryption=none&security=tls&type=ws&host=${DOMAIN}&path=%2Fws#Alibodama-24H-Test`;
        await send(chatId, `کانفیگ تست ۲۴ ساعته

\`\`\`
${cfg}
\`\`\`

برند Alibodama`, null);
      }

      if (data === "premium") {
        if (!await member(userId)) {
          await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/answerCallbackQuery?callback_query_id=${u.callback_query.id}&text=اول عضو کانال شو!&show_alert=true`);
          return new Response("OK");
        }
        const cfg = `vless://${uuid()}@${DOMAIN}:443?encryption=none&security=tls&type=ws&host=${DOMAIN}&path=%2Fws#Alibodama-30Days-Premium`;
        await send(chatId, `عضویت تأیید شد!

کانفیگ ۳۰ روزه اختصاصی

\`\`\`
${cfg}
\`\`\`

Alibodama | t.me/alibodama`, null);
      }

      if (u.callback_query) await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/answerCallbackQuery?callback_query_id=${u.callback_query.id}`);

      return new Response("OK");
    }

    return new Response("Alibodama Bot");
  }
};
Add _worker.js for Telegram bot
