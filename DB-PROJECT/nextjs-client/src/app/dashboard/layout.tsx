"use client";
import PageLoader from "@/components/PageLoader";
import { useAuthGuard } from "@/hooks/useAuthGuard";
import * as React from "react";

export default function Layout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const { loading } = useAuthGuard();
  return loading ? <PageLoader /> : children;
}
