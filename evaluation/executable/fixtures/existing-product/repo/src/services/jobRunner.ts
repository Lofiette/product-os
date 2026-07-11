export async function runJob(input: string) {
  if (!input) throw new Error("missing input");
  return { status: "complete", output: input.toUpperCase() };
}
