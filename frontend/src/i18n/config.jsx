import localesManifest from "../locales/manifest.json";

export const SUPPORTED_LANGUAGES = [
  { code: "fr", label: "French", nativeLabel: "Francais", formatLocale: "fr-FR" },
  { code: "en", label: "English", nativeLabel: "English", formatLocale: "en" },
];

export const DEFAULT_LANGUAGE = localesManifest.default || "fr";
export const AVAILABLE_LANGUAGE_CODES = new Set(
  (localesManifest.locales || []).map((language) => language.code)
);
export const SUPPORTED_LANGUAGE_CODES = new Set(
  SUPPORTED_LANGUAGES
    .map((language) => language.code)
    .filter((code) => AVAILABLE_LANGUAGE_CODES.has(code))
);
export const FORMAT_LOCALE_BY_LANGUAGE = new Map(
  SUPPORTED_LANGUAGES.map((language) => [language.code, language.formatLocale || language.code])
);
