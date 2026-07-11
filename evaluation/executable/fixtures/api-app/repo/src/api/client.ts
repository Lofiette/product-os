export type ApiErrorBody = { detail?: string; code?: string };
export async function request(path: string) {
  const response = await fetch(`/api${path}`, { credentials: "same-origin" });
  if (!response.ok) {
    const body = (await response.json()) as ApiErrorBody;
    throw new Error(body.detail ?? `Request failed: ${response.status}`);
  }
  return response.json();
}
