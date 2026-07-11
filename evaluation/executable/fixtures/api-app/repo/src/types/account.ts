export type AccountStatus = "active" | "pending" | "blocked" | string;
export type Account = { id: string; name: string; status: AccountStatus; updatedAt: string };
export type AccountUpdate = { name: string };
