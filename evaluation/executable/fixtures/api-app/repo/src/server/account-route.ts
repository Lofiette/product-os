export async function updateAccount(request: Request) {
  const body = await request.json();
  const accountId = new URL(request.url).searchParams.get("id");
  return Response.json({ id: accountId, name: body.name, status: "active" });
}
