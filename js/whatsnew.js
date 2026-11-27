// "What's new": release notes, newest first. Shown once in the pad after an update (main.js) and used for the
// update graphic for Discord (tools/whatsnew-card.html → node tools/whatsnew-card.mjs).
// New release: add an entry at the top, write the texts in English inside t() and add SR and DE in i18n-dict.js.
// Only list what the pad really does.
import { t, LOCALE } from "./i18n.js";
import { esc } from "./util.js";
import { APP_ICONS } from "./icons.js";

export const releases = () => [
  { v: "1.0", date: "2026-11-27", groups: [
    { icon: "pad", name: "UAE Pad", items: [
      t("The crew pad for Emirates Virtual, built on the same base as ASL Pad"),
      t("Timetable of November 2026: 952 passenger and cargo flights, 151 airports and every registration of the fleet"),
      t("Booking, SimBrief, VATSIM, logbook and all apps work like in ASL Pad – home base Dubai (OMDB)"),
    ] },
  ] },
];
export const latest = () => releases()[0];
// texts of the update graphic
export const cardTexts = () => ({ title: t("What's new"), live: t("All live now."), open: t("Open the pad on your iPad and fly."), sub: t("Crew pad for Emirates Virtual") });

export function relDate(r) {
  try { return new Intl.DateTimeFormat(LOCALE(), { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" }).format(new Date(r.date)); } catch { return r.date; }
}
export const groupIcon = (g, base = "") => g.icon === "pad" ? `<img src="${base}icons/icon.svg" alt="">` : APP_ICONS[g.icon] || "";

// the cards of one release (used in the pad and in the graphic)
export function groupsHtml(r, base = "") {
  return r.groups.map((g) => `<div class="wn-card"><div class="wn-h"><span class="wn-ic">${groupIcon(g, base)}</span><b>${esc(t(g.name))}</b></div>
    <ul>${g.items.map((i) => `<li>${esc(i)}</li>`).join("")}</ul></div>`).join("");
}
