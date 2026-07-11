export type ButtonProps = {
  children: string;
  variant?: "primary" | "secondary" | "danger";
  ariaLabel?: string;
};

export function Button({ children, variant = "primary", ariaLabel }: ButtonProps) {
  return <button data-ds="Button" data-variant={variant} aria-label={ariaLabel}>{children}</button>;
}
