export interface NavItemConfig {
  key: string;
  title?: string;
  disabled?: boolean;
  external?: boolean;
  label?: string;
  icon?: string;
  href?: string;
  items?: NavItemConfig[];
  // Matcher cannot be a function in order
  // to be able to use it on the server.
  // If you need to match multiple paths,
  // can extend it to accept multiple matchers.
  matcher?: { type: "startsWith" | "equals"; href: string };
}

export const navItems = [
  { key: "overview", title: "Overview", href: "/", icon: "chart-pie" },
  { key: "customers", title: "Customers", href: "/" },
  { key: "integrations", title: "Integrations", href: "/" },
  { key: "settings", title: "Settings", href: "/" },
  { key: "account", title: "Account", href: "/" },
  { key: "error", title: "Error", href: "/" },
] satisfies NavItemConfig[];
