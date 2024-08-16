export const formatDuration = (duration: string) => {
  const [h, m, s] = duration.split(":") || "";
  return Object.entries({ h, m, s })
    .reduce((acc, [n, v]) => {
      const f = parseInt(v);
      return f ? acc + `${f}${n}` : acc;
    }, "")
    .trim();
};
