import { i18n } from "@/plugins/i18n";

const timeIntervals = [
  ["years", 3600 * 24 * 365],
  ["months", 3600 * 24 * 30],
  ["weeks", 3600 * 24 * 7],
  ["days", 3600 * 24],
  ["hours", 3600],
  ["minutes", 60],
  ["seconds", 1],
] as const;

/**
 * Display the diff between a date string and now.
 */
export const formatTimeSince = (time: string): string => {
  const date = new Date(time);
  const formatter = new Intl.RelativeTimeFormat(i18n.global.locale.value);
  const diff = (date.getTime() - Date.now()) / 1000;

  for (const [type, seconds] of timeIntervals) {
    if (seconds < Math.abs(diff)) {
      return formatter.format(Math.round(diff / seconds), type);
    }
  }
  return formatter.format(diff, "years");
};

/**
 * Format a hh:mm:ss duration with only specified values.
 */
export const formatDuration = (duration: string): string => {
  const [h, m, s] = duration.split(":") || "";
  return Object.entries({ h, m, s })
    .reduce((acc, [n, v]) => {
      const f = parseInt(v);
      return f ? acc + `${f}${n}` : acc;
    }, "")
    .trim();
};

/**
 * Same as formatDuration, but translate h,m,s for certain locales.
 */
export const formatLocalised = (time: string): string => {
  const [h, m, s] = i18n.global.t("times.hms").split(",");
  return formatDuration(time).replace("h", h).replace("m", m).replace("s", s);
};

/**
 * Format hh:mm:ss duration string as ISO duration.
 */
export const formatISOTime = (time: string): string =>
  `PT${formatDuration(time).replace(" ", "").toUpperCase()}`;
