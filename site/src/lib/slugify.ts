export function slugify(brand: string, model: string, build: string): string {
  const modelWords = new Set(model.toLowerCase().split(/\s+/));
  const buildNormalized = build.toLowerCase().replace(/[^a-z0-9 ]+/g, ' ');
  const buildWords = new Set(buildNormalized.split(/\s+/).filter(Boolean));

  const modelSubsetOfBuild = [...modelWords].every(w => buildWords.has(w));
  const text = modelSubsetOfBuild ? `${brand} ${build}` : `${brand} ${model} ${build}`;

  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}
