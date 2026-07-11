import type { Account } from "../../types/account";
export function AccountForm({ account }: { account: Account }) {
  return <form><label>Name<input defaultValue={account.name} /></label><p className="error">Something went wrong</p><button>Save</button></form>;
}
