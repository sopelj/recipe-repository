import { i18n } from "@/plugins/i18n";

export const formatDuration = (duration: string): string => {
  const [h, m, s] = duration.split(":") || "";
  return Object.entries({ h, m, s })
    .reduce((acc, [n, v]) => {
      const f = parseInt(v);
      return f ? acc + `${f}${n}` : acc;
    }, "")
    .trim();
};

export const formatLocalised = (time: string): string => {
  const [h, m, s] = i18n.global.t('times.hms').split(",");
  return formatDuration(time).replace("h", h).replace("m", m).replace("s", s);
};

export const formatISOTime = (time: string): string => `PT${formatDuration(time).replace(" ", "").toUpperCase()}`;
